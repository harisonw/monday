"""
LangChain LCEL pipeline — two-stage AI processing.

Stage 1: Risk Assessment  (prompt → Gemini → RiskAssessment)
Stage 2: Onboarding Summary (prompt + risk context → Gemini → OnboardingSummary)
"""
import time
from langchain_google_genai import ChatGoogleGenerativeAI

from src.models import RiskAssessment, OnboardingSummary
from src.prompts import RISK_PROMPT, SUMMARY_PROMPT


def build_llm(model: str, api_key: str) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=api_key,
        temperature=0.1,  # low temp for consistent, deterministic compliance output
    )


def run_risk_assessment(llm: ChatGoogleGenerativeAI, app: dict, config: dict = None) -> RiskAssessment:
    """
    Stage 1: Run risk assessment on a single application.
    Returns a validated RiskAssessment Pydantic object.
    """
    run_config = config.copy() if config else {}
    if "callbacks" in run_config and run_config["callbacks"]:
        run_config.setdefault("metadata", {})
        run_config["metadata"].update({
            "langfuse_trace_name": "Client Intake - Risk Assessment",
            "langfuse_session_id": app["application_id"],
            "langfuse_tags": ["crestview", "risk-assessment"],
        })
    chain = RISK_PROMPT | llm.with_structured_output(RiskAssessment, method="json_schema")
    return chain.invoke({
        "application_id":    app["application_id"],
        "client_name":       app["client_name"],
        "client_type":       app["client_type"],
        "requested_services": app["requested_services"],
        "estimated_aum":     app["estimated_aum"],
        "submission_date":   app["submission_date"],
        "status":            app["status"],
        "description":       app["description"],
    }, config=run_config)


def run_onboarding_summary(
    llm: ChatGoogleGenerativeAI,
    app: dict,
    risk: RiskAssessment,
    config: dict = None,
) -> OnboardingSummary:
    """
    Stage 2: Run onboarding summary using application data + risk context.
    The risk assessment output feeds directly into this prompt — sequential dependency.
    Returns a validated OnboardingSummary Pydantic object.
    """
    run_config = config.copy() if config else {}
    if "callbacks" in run_config and run_config["callbacks"]:
        run_config.setdefault("metadata", {})
        run_config["metadata"].update({
            "langfuse_trace_name": "Client Intake - Onboarding Summary",
            "langfuse_session_id": app["application_id"],
            "langfuse_tags": ["crestview", "onboarding-summary"],
        })
    chain = SUMMARY_PROMPT | llm.with_structured_output(OnboardingSummary, method="json_schema")
    return chain.invoke({
        "application_id":    app["application_id"],
        "client_name":       app["client_name"],
        "client_type":       app["client_type"],
        "requested_services": app["requested_services"],
        "estimated_aum":     app["estimated_aum"],
        "submission_date":   app["submission_date"],
        "description":       app["description"],
        # Risk context from Stage 1
        "risk_level":                     risk.risk_level,
        "risk_score":                     risk.risk_score,
        "compliance_flags":               ", ".join(risk.compliance_flags) if risk.compliance_flags else "None identified",
        "requires_enhanced_due_diligence": str(risk.requires_enhanced_due_diligence),
        "compliance_reasoning":           risk.compliance_reasoning,
        "recommended_actions":            "\n".join(f"- {a}" for a in risk.recommended_actions),
    }, config=run_config)


def process_application(
    llm: ChatGoogleGenerativeAI,
    app: dict,
    rate_limit_delay: float = 1.5,
    max_retries: int = 2,
    callbacks: list = None,
) -> tuple[RiskAssessment, OnboardingSummary]:
    """
    Run the full two-stage pipeline for a single application.
    Returns (RiskAssessment, OnboardingSummary).
    Raises RuntimeError if all retries exhausted.
    """
    langfuse_client = None
    if callbacks:
        try:
            from langfuse import get_client, propagate_attributes
            langfuse_client = get_client()
        except ImportError:
            pass

    if langfuse_client:
        try:
            with propagate_attributes(
                session_id=app["application_id"],
                tags=["crestview", "intake-pipeline"]
            ):
                with langfuse_client.start_as_current_observation(
                    name="Client Intake Pipeline",
                    as_type="span"
                ):
                    return _run_pipeline(llm, app, rate_limit_delay, max_retries, callbacks)
        except Exception:
            # Fallback to standard un-traced execution if tracing setup fails
            pass

    return _run_pipeline(llm, app, rate_limit_delay, max_retries, callbacks)


def _run_pipeline(
    llm: ChatGoogleGenerativeAI,
    app: dict,
    rate_limit_delay: float,
    max_retries: int,
    callbacks: list,
) -> tuple[RiskAssessment, OnboardingSummary]:
    config = {"callbacks": callbacks} if callbacks else {}
    for attempt in range(max_retries + 1):
        try:
            risk = run_risk_assessment(llm, app, config=config)
            time.sleep(rate_limit_delay)
            summary = run_onboarding_summary(llm, app, risk, config=config)
            time.sleep(rate_limit_delay)
            return risk, summary
        except Exception as e:
            if attempt < max_retries:
                wait = 3 * (attempt + 1)
                time.sleep(wait)
                continue
            raise RuntimeError(
                f"Pipeline failed for {app['application_id']} after {max_retries + 1} attempts: {e}"
            ) from e
