"""Check current board state."""
import os
from dotenv import load_dotenv
from src.monday_client import MondayClient

load_dotenv()
m = MondayClient(os.environ["MONDAY_API_TOKEN"], os.environ["MONDAY_BOARD_ID"])

result = m._request("""
{
  boards(ids: [5097242760]) {
    items_page(limit: 500) {
      items {
        id name
        column_values(ids: ["text_mm3scqhz"]) { id text }
        subitems { id name column_values { id text } }
      }
    }
  }
}
""")
items = result["data"]["boards"][0]["items_page"]["items"]
print(f"Total items on board: {len(items)}")
for item in items:
    app_id = next((cv["text"] for cv in item["column_values"] if cv["id"] == "text_mm3scqhz"), "N/A")
    subs = item.get("subitems", [])
    print(f"  {app_id:20s} | {item['name'][:35]:35s} | subitems={len(subs)}")
    for si in subs:
        status_val = next((cv["text"] for cv in si["column_values"] if cv["id"] == "status"), "")
        print(f"      [{('✓' if status_val else ' ')}] {si['name'][:50]:50s} status={status_val!r}")
