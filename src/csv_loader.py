"""
CSV ingestion — reads crestview_client_applications.csv and returns
a validated list of application dicts.
"""
import csv
from pathlib import Path


REQUIRED_FIELDS = {
    "application_id",
    "client_name",
    "client_type",
    "requested_services",
    "estimated_aum",
    "submission_date",
    "status",
    "description",
}


def load_applications(csv_path: str | Path) -> list[dict]:
    """
    Read the CSV and return a list of dicts with typed values.
    Raises ValueError if required fields are missing or the file is empty.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    rows: list[dict] = []
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)

        # Validate headers
        headers = set(reader.fieldnames or [])
        missing = REQUIRED_FIELDS - headers
        if missing:
            raise ValueError(f"CSV missing required columns: {missing}")

        for row in reader:
            rows.append({
                "application_id":    row["application_id"].strip(),
                "client_name":       row["client_name"].strip(),
                "client_type":       row["client_type"].strip(),
                "requested_services": row["requested_services"].strip(),
                "estimated_aum":     int(row["estimated_aum"].strip()),
                "submission_date":   row["submission_date"].strip(),   # MM/DD/YYYY
                "status":            row["status"].strip(),
                "description":       row["description"].strip(),
            })

    if not rows:
        raise ValueError("CSV file contains no application rows.")

    return rows
