"""
Pydantic data models for structured LLM output.
Used with langchain-google-genai's with_structured_output().
"""
from typing import Literal
from pydantic import BaseModel, Field


class RiskAssessment(BaseModel):
    """Stage 1 — AI risk assessment output for the compliance team."""

    risk_level: Literal["Low", "Medium", "High"] = Field(
        description="Overall risk classification for this client application."
    )
    risk_score: int = Field(
        ge=1, le=100,
        description="Numeric risk score from 1 (lowest risk) to 100 (highest risk)."
    )
    compliance_flags: list[str] = Field(
        description=(
            "Specific compliance concerns identified, e.g. 'PEP', 'Offshore Entity', "
            "'Nominee Directors', 'Incomplete KYC', 'Thin Source-of-Funds Documentation', "
            "'Pressure Tactics', 'Third-Party Introducer'. Empty list if none."
        )
    )
    compliance_reasoning: str = Field(
        description=(
            "Detailed, audit-defensible explanation of the risk assessment. "
            "Must explain which specific information or patterns informed each flag and the overall risk level. "
            "Should be suitable for review by a compliance officer and regulators."
        )
    )
    recommended_actions: list[str] = Field(
        description=(
            "Ordered list of recommended next steps for the compliance team, "
            "e.g. 'Request certified beneficial ownership documentation', 'Conduct PEP screening'."
        )
    )
    requires_enhanced_due_diligence: bool = Field(
        description="True if this client requires Enhanced Due Diligence (EDD) beyond standard KYC."
    )


class OnboardingSummary(BaseModel):
    """Stage 2 — Operational onboarding summary informed by the risk assessment."""

    client_overview: str = Field(
        description=(
            "Plain-language description of who this client is: entity type, background, "
            "source of wealth, and relationship context. 2-4 sentences."
        )
    )
    service_requirements: str = Field(
        description=(
            "What services the client is requesting, their investment mandate, "
            "and any special operational requirements (e.g. phased onboarding, ESG exclusions, trust structures)."
        )
    )
    complexity_rating: Literal["Standard", "Moderate", "Complex"] = Field(
        description="Overall operational complexity of onboarding this client."
    )
    estimated_onboarding_days: int = Field(
        ge=1,
        description="Estimated number of business days to complete onboarding given risk level and complexity."
    )
    key_considerations: list[str] = Field(
        description=(
            "Important things the operations team must be aware of, "
            "including risk-driven requirements (e.g. 'Enhanced due diligence required before account activation')."
        )
    )
    next_steps: list[str] = Field(
        description=(
            "Ordered, actionable list of immediate next steps for the operations team. "
            "Must reflect risk assessment findings — e.g. high risk clients should have compliance steps first."
        )
    )
    priority: Literal["Low", "Medium", "High", "Critical"] = Field(
        description=(
            "Operational priority for this onboarding. Critical = high-risk or largest AUM. "
            "Must be consistent with the risk_level from the risk assessment."
        )
    )
