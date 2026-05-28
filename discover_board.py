"""Temporary board discovery script — identifies column IDs, groups, and subitem schema."""
import json
import os
import urllib.request
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["MONDAY_API_TOKEN"]
BOARD_ID = os.environ["MONDAY_BOARD_ID"]
API_URL = os.environ.get("MONDAY_API_URL", "https://api.monday.com/v2")

HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json",
    "API-Version": "2024-01",
}


def gql(query: str) -> dict:
    payload = json.dumps({"query": query}).encode()
    req = urllib.request.Request(API_URL, data=payload, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


# --- 1. Board columns & groups ---
board_meta = gql(f"""
{{
  boards(ids: [{BOARD_ID}]) {{
    name
    columns {{ id title type }}
    groups {{ id title }}
  }}
}}
""")

board = board_meta["data"]["boards"][0]
print(f"\n{'='*60}")
print(f"BOARD: {board['name']}")
print(f"{'='*60}")

print("\n--- GROUPS ---")
for g in board["groups"]:
    print(f"  id={g['id']!r}  title={g['title']!r}")

print("\n--- MAIN ITEM COLUMNS ---")
for c in board["columns"]:
    print(f"  id={c['id']!r:30s} type={c['type']!r:25s} title={c['title']!r}")

# --- 2. Sample items with column values ---
items_data = gql(f"""
{{
  boards(ids: [{BOARD_ID}]) {{
    items_page(limit: 3) {{
      items {{
        id
        name
        group {{ id title }}
        column_values {{ id text value }}
        subitems {{
          id
          name
          board {{ columns {{ id title type }} }}
          column_values {{ id text value }}
        }}
      }}
    }}
  }}
}}
""")

items = items_data["data"]["boards"][0]["items_page"]["items"]
print(f"\n--- SAMPLE ITEMS (first {len(items)}) ---")
for item in items:
    print(f"\n  Item: {item['name']!r}  (id={item['id']})  group={item['group']['title']!r}")
    print("  Column values:")
    for cv in item["column_values"]:
        if cv["text"] or cv["value"]:
            print(f"    col_id={cv['id']!r:30s} text={cv['text']!r}")

    if item["subitems"]:
        print(f"  Subitems ({len(item['subitems'])}):")
        # Print subitem column schema once (from first item)
        if item["subitems"] and item == items[0]:
            print("  Subitem columns:")
            for sc in item["subitems"][0]["board"]["columns"]:
                print(f"    id={sc['id']!r:30s} type={sc['type']!r:25s} title={sc['title']!r}")
        for si in item["subitems"]:
            print(f"    - {si['name']!r}  (id={si['id']})")
            for cv in si["column_values"]:
                if cv["text"] or cv["value"]:
                    print(f"        col_id={cv['id']!r:30s} text={cv['text']!r}")
    else:
        print("  No subitems found on this item.")

print(f"\n{'='*60}")
print("Discovery complete.")
