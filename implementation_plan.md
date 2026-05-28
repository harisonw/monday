# Technical POC: AI-Powered Client Intake Pipeline

Build an end-to-end Python pipeline that reads 15 client applications from CSV, runs a two-stage AI assessment (risk → onboarding summary) using LangChain + Google Gemini, and pushes structured results to a monday.com board via the Monday MCP.

## User Review Required

> [!IMPORTANT]
> **Monday MCP access** — Your `.env` currently has `MONDAY_API_TOKEN=` and `MONDAY_BOARD_ID=` blank. Before we can write to the board, you'll need to:
> 1. Generate a monday.com API token from your profile (**Avatar → Developers → My Access Tokens**)
> 2. Grab the Board ID from the URL of your "Crestview Capital Group Onboarding" board (visible in the screenshot — looks like a numeric ID in the URL)
> 3. Paste both into `.env`

> [!IMPORTANT]
> **Monday MCP integration** — You mentioned wanting to use the Monday MCP. Two approaches:
> - **Option A (Recommended for POC):** Use the **monday.com GraphQL API directly** via `requests` in Python for deterministic, scriptable board writes — this is what the POC code will do by default.
> - **Option B (Monday MCP via Antigravity):** Configure the hosted Monday MCP server (`https://mcp.monday.com/mcp`) in your Antigravity MCP config so *I* can read/write your board interactively during development and demos.
> - We can do **both** — the code uses the GraphQL API, and we separately configure the MCP so you can also interact with the board via AI tooling during the presentation.

> [!WARNING]
> **Google AI Studio API Key** — Your `.env` has a key set. Confirm it's active and has quota for `gemini-flash-latest`. The POC will make ~30 API calls (2 per application × 15 apps).

## Open Questions

1. **Board columns** — From your screenshot, the board has: Task, Owner, Status, Due date, Files, Notes, Last updated, Priority. Do you want us to **add custom columns** to the board (Risk Level, Compliance Reasoning, Onboarding Summary, AUM, Client Type) or create a **new board** specifically for the POC intake pipeline?

2. **Gemini model** — Your `.env` says `gemini-flash-latest`. Do you want to stick with Flash (faster/cheaper) or use `gemini-2.0-pro` (more thorough reasoning for compliance)? Flash is fine for the POC demo.

3. **Output format** — The task spec asks for "JSON, CSV, or formatted console output". Plan is to do **all three**: rich console output during the demo, JSON artifacts for inspection, and monday.com board write. Sound good?

---

## Proposed Changes

### Project Structure

```
monday/
├── .env                          # API keys (already exists)
├── .env.example                  # Template (already exists)
├── crestview_client_applications.csv  # Input data (already exists)
├── pyproject.toml                # Dependencies (UPDATE)
├── main.py                       # Entry point (REWRITE)
├── src/
│   ├── __init__.py
│   ├── models.py                 # Pydantic data models
│   ├── prompts.py                # LangChain prompt templates
│   ├── pipeline.py               # LCEL chains (risk → summary)
│   ├── csv_loader.py             # CSV ingestion
│   ├── monday_client.py          # monday.com GraphQL API client
│   └── console_output.py         # Rich terminal output formatting
├── output/                       # Generated artifacts
│   └── (pipeline_results.json)   # Written at runtime
└── docs/                         # Existing docs (unchanged)
```

---

### Dependencies

#### [MODIFY] [pyproject.toml](file:///wsl.localhost/Ubuntu/home/harison/projects/monday/pyproject.toml)

Add required packages:

```toml
dependencies = [
    "langchain>=1.3.2",
    "langchain-google-genai>=4.2.3",
    "python-dotenv>=1.1.0",
    "pydantic>=2.11.0",
    "requests>=2.32.0",
    "rich>=14.0.0",
]
```

- `python-dotenv` — load `.env` for API keys
- `pydantic` — structured output models (already a langchain dep, but pin explicitly)
- `requests` — HTTP calls to monday.com GraphQL API
- `rich` — beautiful console output for the live demo

---

### Data Models

#### [NEW] [models.py](file:///wsl.localhost/Ubuntu/home/harison/projects/monday/src/models.py)

Pydantic models used for **structured LLM output** via `with_structured_output()`:

```python
class RiskAssessment(BaseModel):
    """Stage 1 output — AI risk assessment for compliance team."""
    risk_level: Literal["Low", "Medium", "High"]
    risk_score: int  # 1-100
    compliance_flags: list[str]  # e.g., ["PEP", "Offshore Entity", "Incomplete KYC"]
    compliance_reasoning: str  # Detailed, auditable explanation
    recommended_actions: list[str]  # Next steps for compliance team
    requires_enhanced_due_diligence: bool

class OnboardingSummary(BaseModel):
    """Stage 2 output — operational summary informed by risk context."""
    client_overview: str  # Who is this client, plain language
    service_requirements: str  # What they need
    complexity_rating: Literal["Standard", "Moderate", "Complex"]
    estimated_onboarding_days: int
    key_considerations: list[str]  # What the ops team should know
    next_steps: list[str]  # Ordered action items
    priority: Literal["Low", "Medium", "High", "Critical"]

class ClientIntakeResult(BaseModel):
    """Combined output per application — full pipeline result."""
    application_id: str
    client_name: str
    client_type: str
    estimated_aum: int
    risk_assessment: RiskAssessment
    onboarding_summary: OnboardingSummary
```

> [!TIP]
> Using `with_structured_output(RiskAssessment, method="json_schema")` guarantees the LLM returns valid, parseable Pydantic objects — no regex extraction or fragile JSON parsing needed.

---

### Prompt Engineering

#### [NEW] [prompts.py](file:///wsl.localhost/Ubuntu/home/harison/projects/monday/src/prompts.py)

Two carefully engineered prompt templates:

**Stage 1 — Risk Assessment Prompt:**
- Role: Senior KYC/AML compliance analyst at a global investment firm
- Context: Application data (all fields from CSV)
- Instructions: Assess risk level, flag compliance concerns (PEP, offshore structures, thin documentation, shell companies, nominee directors), provide explicit reasoning suitable for regulatory audit
- Key requirement: *Explain what patterns/information informed the judgment* (per Priya's needs)

**Stage 2 — Onboarding Summary Prompt:**
- Role: Senior client operations manager
- Context: Application data **+ the risk assessment output from Stage 1**
- Instructions: Generate an actionable operations summary — who, what, complexity, timeline, next steps
- Key requirement: *Risk assessment context actively informs the summary* (sequential dependency)

---

### Pipeline Architecture

#### [NEW] [pipeline.py](file:///wsl.localhost/Ubuntu/home/harison/projects/monday/src/pipeline.py)

Built using **LangChain Expression Language (LCEL)** with the pipe operator:

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────────┐     ┌──────────────────┐
│  CSV Row     │ ──→ │ Risk Assessment  │ ──→ │ Onboarding Summary  │ ──→ │ Combined Result  │
│  (raw data)  │     │ Chain            │     │ Chain               │     │ (ClientIntakeResult)
└─────────────┘     │ prompt1 | llm |  │     │ prompt2 | llm |     │     └──────────────────┘
                    │ structured_output│     │ structured_output   │
                    └──────────────────┘     └─────────────────────┘
```

**Sequential dependency enforced:** The onboarding summary prompt template includes `{risk_level}`, `{compliance_flags}`, `{compliance_reasoning}`, and `{recommended_actions}` — directly from the Stage 1 output. This is not two independent calls; Stage 2 *depends on* Stage 1.

**Error handling:**
- `try/except` around each application with retry logic (up to 2 retries per app)
- If an application fails after retries, log the error and continue processing remaining apps
- Rate limiting between API calls to respect quotas

---

### Monday.com Integration

#### [NEW] [monday_client.py](file:///wsl.localhost/Ubuntu/home/harison/projects/monday/src/monday_client.py)

GraphQL API client that:

1. **Validates board access** — queries the board to confirm it exists and reads column IDs
2. **Creates items** — one item per processed application with column values:

| monday.com Column | Source | Column Type |
|:---|:---|:---|
| Item Name | `client_name` | Default name column |
| Status | Maps from `risk_level` → color-coded status labels | Status |
| Client Type | `client_type` | Text |
| AUM | `estimated_aum` formatted as currency | Numbers |
| Risk Level | `risk_level` (Low/Medium/High) | Status (green/yellow/red) |
| Compliance Flags | Joined `compliance_flags` | Long Text |
| Compliance Reasoning | `compliance_reasoning` | Long Text |
| Onboarding Summary | `client_overview` + `next_steps` | Long Text |
| Priority | `priority` from onboarding summary | Status |
| Est. Onboarding Days | `estimated_onboarding_days` | Numbers |
| Complexity | `complexity_rating` | Status |

3. **Supports group assignment** — High-risk items go to a "Requires Review" group; Low/Medium go to "To-Do"

---

### Console Output

#### [NEW] [console_output.py](file:///wsl.localhost/Ubuntu/home/harison/projects/monday/src/console_output.py)

Using the `rich` library for a **visually impressive demo**:
- Progress bar while processing applications
- Color-coded risk level panels (🟢 Low, 🟡 Medium, 🔴 High)
- Table summary of all 15 applications at the end
- Expandable detail view per application

---

### Entry Point

#### [MODIFY] [main.py](file:///wsl.localhost/Ubuntu/home/harison/projects/monday/main.py)

Orchestrates the full pipeline:

```python
async def main():
    # 1. Load environment & initialize LLM
    # 2. Read CSV → list of application dicts
    # 3. For each application:
    #    a. Run risk assessment chain → RiskAssessment
    #    b. Run onboarding summary chain (with risk context) → OnboardingSummary
    #    c. Combine into ClientIntakeResult
    #    d. Display rich console output
    # 4. Write all results to output/pipeline_results.json
    # 5. Push all results to monday.com board
    # 6. Print final summary table
```

---

## Verification Plan

### Automated Tests

```bash
# 1. Install dependencies
cd /home/harison/projects/monday && uv sync

# 2. Run the full pipeline
uv run python main.py

# 3. Verify output file exists and contains 15 results
cat output/pipeline_results.json | python -m json.tool | head -50
```

### Manual Verification

- **Console output**: Confirm all 15 applications processed with visible risk levels
- **Risk accuracy check**: Verify high-risk flags on known suspicious applications:
  - APP-0303 (Apex Global Holdings) → **High** (offshore, nominee directors, opaque ownership)
  - APP-0307 (Velocity Venture Partners) → **High** (PEP, incomplete KYC)
  - APP-0311 (Eastbridge Trading Group) → **High** (new entity, thin docs, pressure tactics)
  - APP-0315 (R. Ashford) → **High** (third-party introducer, offshore trust, declined calls, no docs)
- **Sequential dependency**: Confirm onboarding summaries reference the risk findings (e.g., "Enhanced due diligence required before proceeding" for high-risk clients)
- **Monday.com board**: Open the board and verify all 15 items appear with correct column values and group assignments
