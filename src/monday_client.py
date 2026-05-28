"""
monday.com GraphQL API client.

Handles:
  - Querying existing items for deduplication on Application ID
  - Creating main items with all CSV column values
  - Creating 7 standard subitems per new item
  - Creating subitems on existing items that don't have them yet
  - Updating a specific subitem's Status + Notes columns
"""
import datetime
import json
import time
import urllib.request
import urllib.error
from typing import Optional

# ---------------------------------------------------------------------------
# Board schema constants (discovered via discover_board.py)
# ---------------------------------------------------------------------------

# Main item column IDs
COL_APPLICATION_ID   = "text_mm3scqhz"
COL_CLIENT_TYPE      = "dropdown_mm3smrx6"
COL_REQUESTED_SVC    = "text_mm3sf0q7"
COL_ESTIMATED_AUM    = "numeric_mm3smzd9"
COL_SUBMISSION_DATE  = "date_mm3sdsgk"
COL_DUE_DATE         = "date"
COL_STATUS           = "project_status"
COL_DESCRIPTION      = "text"

# Subitem column IDs
SUBCOL_STATUS        = "status"
SUBCOL_NOTES         = "long_text_mm3s8k7w"

# Groups
GROUP_TODO           = "new_group29179"
GROUP_COMPLETED      = "new_group43041"

# The 7 standard subitems every new item gets
STANDARD_SUBITEMS = [
    "Document Intake & Completeness Check",
    "Risk Assessment",
    "Onboarding Summary Generation",
    "AI Data Extraction & ClientHub Draft Creation",
    "KYC / AML Screening (ComplianceOne)",
    "Compliance Officer Review & Sign-Off",
    "Downstream System Sync (Salesforce & SharePoint)",
]

# Status label → monday.com status index mapping (from your board's status column)
# Risk Assessment subitem statuses
RISK_STATUS_LABELS = {
    "Low":    "Done",       # green
    "Medium": "Working on it",  # yellow/orange  
    "High":   "Stuck",     # red
}

# Onboarding complexity subitem statuses
COMPLEXITY_STATUS_LABELS = {
    "Standard": "Done",
    "Moderate": "Working on it",
    "Complex":  "Stuck",
}


def _parse_submission_date(date_str: str) -> str:
    """Convert MM/DD/YYYY → YYYY-MM-DD for monday.com date column."""
    parts = date_str.strip().split("/")
    if len(parts) == 3:
        month, day, year = parts
        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    return date_str


def calculate_due_date(submission_date_str: str) -> str:
    """Calculate due date 5 business days after submission date.
    Accepts MM/DD/YYYY or YYYY-MM-DD.
    Returns YYYY-MM-DD.
    """
    date_str = submission_date_str.strip()
    if "/" in date_str:
        parts = date_str.split("/")
        if len(parts) == 3:
            month, day, year = map(int, parts)
            start_date = datetime.date(year, month, day)
        else:
            raise ValueError(f"Invalid date format: {date_str}")
    elif "-" in date_str:
        parts = date_str.split("-")
        if len(parts) == 3:
            year, month, day = map(int, parts)
            start_date = datetime.date(year, month, day)
        else:
            raise ValueError(f"Invalid date format: {date_str}")
    else:
        raise ValueError(f"Invalid date format: {date_str}")

    current_date = start_date
    added = 0
    while added < 5:
        current_date += datetime.timedelta(days=1)
        if current_date.weekday() < 5:  # Monday to Friday
            added += 1
            
    return current_date.strftime("%Y-%m-%d")


class MondayClient:
    def __init__(self, api_token: str, board_id: str, api_url: str = "https://api.monday.com/v2"):
        self.api_url = api_url
        self.board_id = board_id
        self.headers = {
            "Authorization": api_token,
            "Content-Type": "application/json",
            "API-Version": "2024-01",
        }

    # ------------------------------------------------------------------
    # Core request helper
    # ------------------------------------------------------------------

    def _request(self, query: str, variables: Optional[dict] = None, retries: int = 5) -> dict:
        """Execute a GraphQL request with retry on 429 (rate limit) and 503 (unavailable)."""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        RETRYABLE = {429, 503, 502, 504}

        for attempt in range(retries):
            try:
                data = json.dumps(payload).encode()
                req = urllib.request.Request(self.api_url, data=data, headers=self.headers)
                with urllib.request.urlopen(req, timeout=30) as resp:
                    result = json.loads(resp.read().decode())
                    if "errors" in result:
                        raise RuntimeError(f"GraphQL errors: {result['errors']}")
                    return result
            except urllib.error.HTTPError as e:
                if e.code in RETRYABLE and attempt < retries - 1:
                    wait = 2 ** attempt  # 1, 2, 4, 8, 16s
                    print(f"    [HTTP {e.code}] Retrying in {wait}s (attempt {attempt+1}/{retries})...")
                    time.sleep(wait)
                    continue
                raise
        raise RuntimeError("Max retries exceeded")

    # ------------------------------------------------------------------
    # Step 1 helpers — Ingestion
    # ------------------------------------------------------------------

    def get_existing_items(self) -> dict[str, dict]:
        """
        Return a mapping of application_id → {item_id, has_subitems}
        for all items currently on the board.
        """
        query = """
        query ($boardId: ID!) {
          boards(ids: [$boardId]) {
            items_page(limit: 500) {
              items {
                id
                name
                column_values(ids: ["text_mm3scqhz"]) { id text }
                subitems {
                  id
                  name
                  column_values(ids: ["status"]) { id text }
                }
              }
            }
          }
        }
        """
        result = self._request(query, {"boardId": self.board_id})
        items = result["data"]["boards"][0]["items_page"]["items"]

        existing: dict[str, dict] = {}
        for item in items:
            app_id = None
            for cv in item["column_values"]:
                if cv["id"] == COL_APPLICATION_ID and cv["text"]:
                    app_id = cv["text"].strip()
            if app_id:
                subitems_info = {}
                for si in item.get("subitems", []):
                    status = ""
                    for scv in si.get("column_values", []):
                        if scv["id"] == "status" and scv.get("text"):
                            status = scv["text"].strip()
                    subitems_info[si["name"]] = {
                        "id": si["id"],
                        "status": status,
                    }
                existing[app_id] = {
                    "item_id": item["id"],
                    "has_subitems": len(item.get("subitems", [])) > 0,
                    "subitems": {si["name"]: si["id"] for si in item.get("subitems", [])},
                    "subitems_info": subitems_info,
                }
        return existing

    def create_item(self, app: dict) -> str:
        """Create a main board item from a CSV application row. Returns item_id."""
        submission_date = _parse_submission_date(app["submission_date"])
        due_date = calculate_due_date(app["submission_date"])

        column_values = {
            COL_APPLICATION_ID: app["application_id"],
            COL_CLIENT_TYPE:    {"labels": [app["client_type"]]},
            COL_REQUESTED_SVC:  app["requested_services"],
            COL_ESTIMATED_AUM:  app["estimated_aum"],
            COL_SUBMISSION_DATE: {"date": submission_date},
            COL_DUE_DATE:       {"date": due_date},
            COL_STATUS:         {"label": "Working on it"},
            COL_DESCRIPTION:    app["description"],
        }

        mutation = """
        mutation ($boardId: ID!, $groupId: String!, $itemName: String!, $columnVals: JSON!) {
          create_item(
            board_id: $boardId
            group_id: $groupId
            item_name: $itemName
            column_values: $columnVals
          ) { id }
        }
        """
        result = self._request(mutation, {
            "boardId":    self.board_id,
            "groupId":    GROUP_TODO,
            "itemName":   app["client_name"],
            "columnVals": json.dumps(column_values),
        })
        return result["data"]["create_item"]["id"]

    def create_subitems(self, parent_item_id: str) -> dict[str, str]:
        """
        Create all 7 standard subitems under a parent item.
        Returns mapping of subitem_name → subitem_id.
        """
        subitem_ids: dict[str, str] = {}
        mutation = """
        mutation ($parentId: ID!, $itemName: String!) {
          create_subitem(parent_item_id: $parentId, item_name: $itemName) { id }
        }
        """
        for name in STANDARD_SUBITEMS:
            result = self._request(mutation, {
                "parentId": parent_item_id,
                "itemName": name,
            })
            subitem_ids[name] = result["data"]["create_subitem"]["id"]
            time.sleep(0.8)  # avoid burst 503s on subitem creates
        return subitem_ids

    # ------------------------------------------------------------------
    # Steps 2 & 3 helpers — Update subitem
    # ------------------------------------------------------------------

    def update_subitem(self, subitem_id: str, subitem_board_id: str, status_label: str, notes: str) -> None:
        """Update the Status and Notes columns of a specific subitem."""
        column_values = {
            SUBCOL_STATUS: {"label": status_label},
            SUBCOL_NOTES:  {"text": notes},
        }
        mutation = """
        mutation ($itemId: ID!, $boardId: ID!, $columnVals: JSON!) {
          change_multiple_column_values(
            item_id: $itemId
            board_id: $boardId
            column_values: $columnVals
          ) { id }
        }
        """
        self._request(mutation, {
            "itemId":     subitem_id,
            "boardId":    subitem_board_id,
            "columnVals": json.dumps(column_values),
        })

    def get_subitem_board_id(self, subitem_id: str) -> str:
        """Get the board ID of a subitem (subitems live on their own board in monday.com)."""
        query = """
        query ($itemId: ID!) {
          items(ids: [$itemId]) {
            board { id }
          }
        }
        """
        result = self._request(query, {"itemId": subitem_id})
        return result["data"]["items"][0]["board"]["id"]

    def update_main_item_due_date(self, item_id: str, due_date: str) -> None:
        """Update the Due date column of a main board item."""
        column_values = {
            COL_DUE_DATE: {"date": due_date},
        }
        mutation = """
        mutation ($itemId: ID!, $boardId: ID!, $columnVals: JSON!) {
          change_multiple_column_values(
            item_id: $itemId
            board_id: $boardId
            column_values: $columnVals
          ) { id }
        }
        """
        self._request(mutation, {
            "itemId":     item_id,
            "boardId":    self.board_id,
            "columnVals": json.dumps(column_values),
        })
