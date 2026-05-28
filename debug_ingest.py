"""Debug ingest: test the progress through each phase step by step."""
import json
import os
import time
from dotenv import load_dotenv
from src.csv_loader import load_applications
from src.monday_client import MondayClient, RISK_STATUS_LABELS, COMPLEXITY_STATUS_LABELS

load_dotenv()
MONDAY_TOKEN = os.environ["MONDAY_API_TOKEN"]
MONDAY_BOARD = os.environ["MONDAY_BOARD_ID"]
MONDAY_URL   = os.environ.get("MONDAY_API_URL", "https://api.monday.com/v2")

monday = MondayClient(MONDAY_TOKEN, MONDAY_BOARD, MONDAY_URL)
applications = load_applications("crestview_client_applications.csv")
print(f"Loaded {len(applications)} apps")

existing = monday.get_existing_items()
print(f"Found {len(existing)} existing items: {list(existing.keys())}")

# Test creating subitems for APP-0302 which has no subitems
app_0302 = existing.get("APP-2026-0302")
if app_0302:
    print(f"\nAPP-0302 item_id={app_0302['item_id']} has_subitems={app_0302['has_subitems']}")
    if not app_0302["has_subitems"]:
        print("Creating subitems for APP-0302...")
        subitem_ids = monday.create_subitems(app_0302["item_id"])
        print(f"Created subitems: {subitem_ids}")

# Test creating a brand new item for APP-0304
app_0304 = next(a for a in applications if a["application_id"] == "APP-2026-0304")
if "APP-2026-0304" not in existing:
    print(f"\nCreating new item for APP-2026-0304...")
    item_id = monday.create_item(app_0304)
    print(f"Created item_id={item_id}")
    time.sleep(0.5)
    subitem_ids = monday.create_subitems(item_id)
    print(f"Created subitems: {list(subitem_ids.keys())}")

    # Test getting subitem board ID
    risk_subitem_id = subitem_ids.get("Risk Assessment")
    if risk_subitem_id:
        sb_id = monday.get_subitem_board_id(risk_subitem_id)
        print(f"Subitem board ID: {sb_id}")
else:
    print(f"\nAPP-2026-0304 already exists, skipping creation test")
