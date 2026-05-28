# Monday Client Intake Pipeline

AI-assisted pipeline for processing Crestview client applications into monday.com.

## What it does

1. Loads applications from `crestview_client_applications.csv`.
2. Creates or updates monday.com items and subitems.
3. Runs AI risk assessment and onboarding summary generation.
4. Writes results to `output/results.json`.

## Setup

```bash
uv sync
```

Create a `.env` file from `.env.example` and fill in the required values

````

## Run

```bash
uv run python main.py
````

## Notes

- The pipeline expects Python 3.12+
- It skips records already marked `Done` on monday.com when matching results exist locally
