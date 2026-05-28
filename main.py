"""
Crestview Capital Group — AI-Powered Client Intake Pipeline
===========================================================

Three-step pipeline:
  STEP 1 — Ingest CSV to monday.com board (dedup on Application ID, create subitems)
  STEP 2 — AI Risk Assessment per new record → update "Risk Assessment" subitem
  STEP 3 — AI Onboarding Summary per new record → update "Onboarding Summary Generation" subitem

Also saves all results to output/results.json.
"""
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

from src.csv_loader import load_applications
from src.monday_client import MondayClient, RISK_STATUS_LABELS, COMPLEXITY_STATUS_LABELS, calculate_due_date
from src.pipeline import build_llm, process_application
from src.console_output import (
    console,
    print_header,
    print_step,
    print_ingest_result,
    print_application_result,
    print_summary_table,
    make_progress,
)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
GOOGLE_MODEL   = os.environ.get("GOOGLE_MODEL", "gemini-2.0-flash")
MONDAY_TOKEN   = os.environ.get("MONDAY_API_TOKEN", "")
MONDAY_BOARD   = os.environ.get("MONDAY_BOARD_ID", "")
MONDAY_URL     = os.environ.get("MONDAY_API_URL", "https://api.monday.com/v2")

CSV_PATH    = Path("crestview_client_applications.csv")
OUTPUT_PATH = Path("output/results.json")


def _format_risk_notes(risk) -> str:
    """Format RiskAssessment as a readable Notes string for the monday.com subitem."""
    flags = ", ".join(risk.compliance_flags) if risk.compliance_flags else "None identified"
    actions = "\n".join(f"  {i+1}. {a}" for i, a in enumerate(risk.recommended_actions))
    return (
        f"RISK LEVEL: {risk.risk_level} (Score: {risk.risk_score}/100)\n"
        f"Enhanced Due Diligence Required: {'YES' if risk.requires_enhanced_due_diligence else 'No'}\n\n"
        f"COMPLIANCE FLAGS:\n{flags}\n\n"
        f"REASONING:\n{risk.compliance_reasoning}\n\n"
        f"RECOMMENDED ACTIONS:\n{actions}"
    )


def _format_summary_notes(summary) -> str:
    """Format OnboardingSummary as a readable Notes string for the monday.com subitem."""
    considerations = "\n".join(f"  - {c}" for c in summary.key_considerations)
    next_steps = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(summary.next_steps))
    return (
        f"COMPLEXITY: {summary.complexity_rating} | PRIORITY: {summary.priority} | EST. DAYS: {summary.estimated_onboarding_days}\n\n"
        f"CLIENT OVERVIEW:\n{summary.client_overview}\n\n"
        f"SERVICE REQUIREMENTS:\n{summary.service_requirements}\n\n"
        f"KEY CONSIDERATIONS:\n{considerations}\n\n"
        f"NEXT STEPS:\n{next_steps}"
    )


def validate_env():
    missing = []
    if not GOOGLE_API_KEY:
        missing.append("GOOGLE_API_KEY")
    if not MONDAY_TOKEN:
        missing.append("MONDAY_API_TOKEN")
    if not MONDAY_BOARD:
        missing.append("MONDAY_BOARD_ID")
    if missing:
        console.print(f"[red]Missing environment variables: {', '.join(missing)}[/red]")
        sys.exit(1)


def main():
    print_header()
    validate_env()

    monday = MondayClient(MONDAY_TOKEN, MONDAY_BOARD, MONDAY_URL)
    llm    = build_llm(GOOGLE_MODEL, GOOGLE_API_KEY)

    console.print(f"Model: {GOOGLE_MODEL}  |  Board: {MONDAY_BOARD}")
    console.print(f"CSV:   {CSV_PATH}\n")

    # -----------------------------------------------------------------------
    # STEP 1 — INGEST
    # -----------------------------------------------------------------------
    print_step(1, "INGEST — CSV -> monday.com Board")

    applications = load_applications(CSV_PATH)
    console.print(f"Loaded {len(applications)} applications from CSV")

    console.print("Querying board for existing items...")
    existing = monday.get_existing_items()
    console.print(f"Found {len(existing)} existing items on board")

    created_count  = 0
    skipped_count  = 0
    subitems_added = 0

    # Enrich each application with its board item metadata
    for i, app in enumerate(applications):
        app_id = app["application_id"]
        console.print(f"  [{i+1:02d}/{len(applications)}] {app_id} — ", end="")

        if app_id in existing:
            info = existing[app_id]
            app["_item_id"]  = info["item_id"]
            app["_subitems"] = info["subitems"]

            # Proactively ensure existing items have the correct Due date
            due_date = calculate_due_date(app["submission_date"])
            console.print(f"EXISTS — setting Due date to {due_date}... ", end="")
            monday.update_main_item_due_date(info["item_id"], due_date)

            if not info["has_subitems"]:
                console.print(f"adding subitems...")
                subitem_ids = monday.create_subitems(info["item_id"])
                app["_subitems"] = subitem_ids
                subitems_added += 1
            else:
                console.print(f"skipping subitem creation")
            skipped_count += 1
        else:
            console.print(f"NEW — creating item + subitems...")
            item_id = monday.create_item(app)
            time.sleep(1.0)
            subitem_ids = monday.create_subitems(item_id)
            app["_item_id"]  = item_id
            app["_subitems"] = subitem_ids
            created_count += 1
            subitems_added += 1
            time.sleep(1.0)  # breathe between items

    print_ingest_result(created_count, skipped_count, subitems_added)

    # -----------------------------------------------------------------------
    # STEP 2 + 3 — AI PROCESSING
    # -----------------------------------------------------------------------
    print_step(2, "AI PROCESSING — Risk Assessment + Onboarding Summary (Gemini)")
    console.print("Running two-stage LangChain pipeline for all applications...\n")

    # Load previous results to carry over skipped records
    previous_results: dict[str, dict] = {}
    if OUTPUT_PATH.exists():
        try:
            with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
                prev_data = json.load(f)
                for res in prev_data:
                    if isinstance(res, dict) and "application_id" in res and "error" not in res:
                        previous_results[res["application_id"]] = res
        except Exception as e:
            console.print(f"[yellow]Could not read previous results.json: {e}[/yellow]")

    # Cache subitem board ID — fetch once from the first available subitem
    subitem_board_id: str | None = None
    for app in applications:
        risk_id = app.get("_subitems", {}).get("Risk Assessment")
        if risk_id:
            subitem_board_id = monday.get_subitem_board_id(risk_id)
            console.print(f"Subitem board ID: {subitem_board_id}\n")
            break

    all_results: list[dict] = []
    errors: list[str] = []

    for idx, app in enumerate(applications, 1):
        app_id = app["application_id"]
        console.print(f"[{idx:02d}/{len(applications)}] Processing {app_id} — {app['client_name']}...")

        # Skip if already marked Done on Monday board
        is_risk_done = False
        is_summary_done = False
        if app_id in existing:
            subitems_info = existing[app_id].get("subitems_info", {})
            is_risk_done = subitems_info.get("Risk Assessment", {}).get("status") == "Done"
            is_summary_done = subitems_info.get("Onboarding Summary Generation", {}).get("status") == "Done"

        if is_risk_done and is_summary_done:
            if app_id in previous_results:
                prev = previous_results[app_id]
                all_results.append(prev)
                console.print(f"  [SKIPPED] Already marked Done on board — kept previous results from results.json (Risk: {prev['risk_assessment']['risk_level']}, Complexity: {prev['onboarding_summary']['complexity_rating']})")
                continue
            else:
                console.print(f"  [INFO] Marked Done on board but not in results.json — running AI processing...")

        try:
            # Stage 1 & 2: LLM pipeline
            risk, summary = process_application(llm, app)

            # Update "Risk Assessment" subitem
            risk_id = app["_subitems"].get("Risk Assessment")
            if risk_id and subitem_board_id:
                console.print(f"  -> Updating Risk Assessment subitem (status=Done)...")
                monday.update_subitem(
                    subitem_id=risk_id,
                    subitem_board_id=subitem_board_id,
                    status_label="Done",
                    notes=_format_risk_notes(risk),
                )

            # Update "Onboarding Summary Generation" subitem
            summary_id = app["_subitems"].get("Onboarding Summary Generation")
            if summary_id and subitem_board_id:
                console.print(f"  -> Updating Onboarding Summary subitem (status=Done)...")
                monday.update_subitem(
                    subitem_id=summary_id,
                    subitem_board_id=subitem_board_id,
                    status_label="Done",
                    notes=_format_summary_notes(summary),
                )

            # Print rich panel
            print_application_result(app, risk, summary, idx, len(applications))

            all_results.append({
                "application_id":     app["application_id"],
                "client_name":        app["client_name"],
                "client_type":        app["client_type"],
                "estimated_aum":      app["estimated_aum"],
                "submission_date":    app["submission_date"],
                "due_date":           calculate_due_date(app["submission_date"]),
                "risk_assessment":    risk.model_dump(),
                "onboarding_summary": summary.model_dump(),
                "monday_item_id":     app.get("_item_id"),
                "monday_subitems": {
                    "risk_assessment_id":    app["_subitems"].get("Risk Assessment"),
                    "onboarding_summary_id": app["_subitems"].get("Onboarding Summary Generation"),
                },
            })

        except Exception as e:
            error_msg = f"{app['application_id']}: {e}"
            errors.append(error_msg)
            console.print(f"  [FAILED] {error_msg}")
            all_results.append({
                "application_id": app["application_id"],
                "client_name":    app["client_name"],
                "error":          str(e),
            })

    # -----------------------------------------------------------------------
    # Save results.json
    # -----------------------------------------------------------------------
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    console.print(f"\nResults saved to {OUTPUT_PATH}")

    if errors:
        console.print(f"\n{len(errors)} application(s) failed:")
        for e in errors:
            console.print(f"  - {e}")

    # Final summary table
    print_summary_table(all_results)
    console.print("Done.\n")


if __name__ == "__main__":
    main()
