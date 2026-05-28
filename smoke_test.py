"""Quick import and CSV smoke test."""
from src.models import RiskAssessment, OnboardingSummary
from src.prompts import RISK_PROMPT, SUMMARY_PROMPT
from src.csv_loader import load_applications
from src.monday_client import MondayClient
from src.pipeline import build_llm
from src.console_output import console

apps = load_applications("crestview_client_applications.csv")
print(f"All imports OK — {len(apps)} applications loaded from CSV")
print(f"First: {apps[0]['application_id']} — {apps[0]['client_name']}")
print(f"Last:  {apps[-1]['application_id']} — {apps[-1]['client_name']}")
