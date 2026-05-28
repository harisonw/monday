- **The Problem:** Crestview’s client onboarding process is entirely manual, fragmented across five legacy systems, and takes 23 business days. This inefficiency cost them a $200M client account, puts $12M in annual revenue at risk, and has caused relationship manager burnout. A previous attempt to automate using an RPA vendor failed spectacularly because it was too brittle.

- **The Goal:** Design an AI-powered onboarding solution using monday.com as the operational core. The objective is to slash onboarding times to under 5 business days while maintaining strict regulatory compliance, explainability, and enterprise data security.

- **Your Deliverables:** You must prepare a **Strategic Transformation Proposal** presentation (15–20 mins) and a **Live Technical Proof of Concept (POC)** code demonstration (10–12 mins) showing an end-to-end AI pipeline processing 15 realistic client applications.

---

## Concise Step-by-Step Execution Plan

```
┌──────────────────────────┐     ┌──────────────────────────┐     ┌──────────────────────────┐
│ PHASE 1: Data & Needs    │ ──> │ PHASE 2: Technical POC   │ ──> │ PHASE 3: Strategy & Presentation
└──────────────────────────┘     └──────────────────────────┘     └──────────────────────────┘

```

### Phase 1: Analyze Stakeholders & Dataset (Estimated Time: 45 Mins)

- [x] **1.1 Map Stakeholder Goals:** Align your narrative to address each executive's specific anxieties: Claire wants speed/ROI; David requires exception handling; Priya demands compliance explainability/human-in-the-loop; Marcus wants low-maintenance architecture leveraging their existing Microsoft 365/CoPilot licensing.

- [x] **1.2 Ingest Case Data:** Copy the 15 client rows provided at the end of the document into a local file named `crestview_client_applications.csv`. Notice the deliberate variance in risk profiles—ranging from straightforward public pension funds to high-risk offshore corporate shells and Politically Exposed Persons (PEPs).

- [x] **1.3 Validate Dataset Structure:** Confirm the CSV headers, the expected 15 application records, and field consistency before building the pipeline.

- [ ] **1.4 Capture Edge Cases:** Note applications that will need special handling in the POC, such as PEPs, offshore entities, recently formed entities, offshore trusts, thin source-of-funds documentation, or incomplete records.

### Phase 2: Build the Technical POC (Estimated Time: 2 Hours)

- [x] **2.1 Setup Project & Pipeline:** Create a Python or Node.js application to read the client application CSV.

- [x] **2.2 Engineer the AI Prompting Layer:** Integrate an LLM provider (e.g., Gemini, OpenAI, or Anthropic). Write strict prompt templates instructing the LLM to output structured data (ideally JSON) containing:
  - `risk_level` (Low, Medium, High).
  - `compliance_reasoning` (explicit, defensible audit trails addressing Priya's needs).
  - `onboarding_summary` (actionable, operational summary for David's team).

- [x] **2.3 Establish Sequential Dependency:** Ensure the execution pipeline is sequential, meaning the risk assessment context actively feeds into and dictates the final onboarding summary. Include clean try/catch exception handling.

- [x] **2.4 Incorporate monday.com Integration:** Build out a trial monday.com board containing columns for Risk Level, Reasoning, and Summary. Map your AI pipeline's JSON output directly to this board using the monday.com GraphQL API or Model Context Protocol (MCP).

- [x] **2.5 Run End-to-End Test:** Process the 15 applications and verify the output is stable, explainable, sequentially consistent, and presentation-ready.

### Phase 3: Craft the Strategic Proposal (Estimated Time: 1.5 Hours)

- [x] **3.1 Structure the Slide Deck:** Prepare highly scannable, executive-ready slides covering the requested 4 pillars:

1.  **Business Case:** Link operational bottlenecks directly to the $12M revenue-at-risk metric and the lost $200M allocation.

2.  **Solution Architecture:** Draw a blueprint showing monday.com as the collaborative fabric orchestrating Salesforce, SharePoint, and ComplianceOne. Clearly show how Microsoft CoPilot securely communicates with monday.com via the Model Context Protocol (MCP).

3.  **Implementation Roadmap:** Outline a 6-month phased schedule (Discovery $\rightarrow$ Design $\rightarrow$ Build $\rightarrow$ Rollout) detailing specific milestones, KPIs, and risk-mitigation tactics.

4.  **Scaling & Product Strategy:** Propose how this foundational blueprint easily ports over to Portfolio Operations next. Highlight feature requests to bring back to the internal monday.com product team.

- [ ] **3.2 Draft Speaker Notes:** Write concise talking points for each slide so the 15–20 minute pitch stays tight and executive-focused.
- [ ] **3.3 Rehearse Architecture Story:** Practice explaining the system flow, security posture, and compliance controls in plain language.

### Phase 4: Document AI Usage & Rehearse (Estimated Time: 45 Mins)

- [x] **4.1 Log AI Meta-Process:** Compile structured notes detailing how you utilized external AI assistants to write code, refine prompts, or build the architecture. Document explicit examples of prompt iterations, failures, and human course-corrections so you can explain how you evaluated output quality. See [docs/ai-meta-process.md](docs/ai-meta-process.md).

- [ ] **4.2 Rehearse the Delivery:** Dry-run the 15–20 minute strategic pitch followed immediately by a slick 10–12 minute live code execution. Be ready to handle live code tweaks, architecture trade-off discussions, or edge-case questions from the panel.
- [ ] **4.3 Final Readiness Check:** Confirm the deck, demo, and supporting notes are aligned before presenting.
