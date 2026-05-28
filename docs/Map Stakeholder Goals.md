# Strategic Stakeholder Matrix: Crestview Capital Group

## Client Onboarding AI Transformation | Forward Deployed Engineering Program

This matrix maps the distinct goals, pain points, technical constraints, and definitions of success for the executive stakeholders at Crestview Capital Group. As an embedded Forward Deployed Engineer (FDE), aligning the automated solution to these parameters is critical for securing multi-department expansion buy-in.

---

### 1. Claire Nakamura — Chief Operating Officer (COO)

- **Role in Engagement:** Executive Sponsor & Owner of the Digital Operations Mandate.
- **Core Business Context:** Driving firm-wide operational efficiency following critical board reviews. Recently lost a $200M institutional allocation to a competitor due to a prolonged 4-week onboarding cycle.
- **Key Pain Points:**
  - Onboarding process is too slow, overly manual, and directly costing the firm revenue.
  - ~60% of current onboarding activity consists of pure clerical data handling (reading documents, manual transcription, status tracking emails).
  - High executive fatigue with traditional consulting models that deliver passive playbooks rather than operational software.
- **Strategic Goals:**
  - Compress average client onboarding cycle times from **23 business days down to under 5 business days**.
  - Establish an operational blueprint and playbook that can scale across other bottlenecked departments, specifically **Portfolio Operations**.
- **Success Criteria for FDE:** A fully functional, production-ready, AI-assisted onboarding workflow handling live data by the conclusion of the 6-month engagement.

---

### 2. David Holloway — Managing Director, Client Operations

- **Role in Engagement:** Operational Process Owner & Business Unit Leader.
- **Core Business Context:** Manages the frontline team executing data entry and client handoffs. Relationship managers are under severe stress, resulting in the loss of two senior RMs last quarter due to administrative burnout.
- **Key Pain Points:**
  - Highly skeptical of automated solutions due to a failed Robotic Process Automation (RPA) initiative 10 months prior. The RPA bot broke on minor document layout changes, mismanaged exceptions, and escalated the manual troubleshooting workload.
  - Frontend team spends **70% of their day on manual administration** rather than high-value client advisory.
  - Complete operational standstill during compliance handoffs, leading to a constant backlog of **80+ pending compliance reviews**.
- **Strategic Goals:**
  - Ingest messy, highly un-structured multi-format client data (emails, PDFs, scanned forms, physical papers) without pipeline failure.
  - Reclaim team capacity and invert operational time allocation to **70% Client Service / 30% Administration**.
- **Success Criteria for FDE:** A resilient pipeline that seamlessly handles complex edge cases, un-structured data variation, and eliminates the compliance handoff bottleneck.

---

### 3. Priya Sharma — Chief Compliance Officer (CCO)

- **Role in Engagement:** Regulatory Authority & Compliance Process Owner.
- **Core Business Context:** Governs a highly regulated function under strict oversight from the SEC, FINRA, and international regulatory authorities.
- **Key Pain Points:**
  - "Black box" AI systems are completely unacceptable. Any compliance assessment or automated flagging must be thoroughly explainable and defensible during a regulatory audit.
  - Complex client structures (offshore corporations, multi-layered holding entities, Politically Exposed Persons) require exhaustive due diligence and cannot be autonomously processed.
- **Strategic Goals:**
  - Protect the firm against money laundering (AML), sanctions violations, and Know Your Customer (KYC) compliance failures.
  - Boost the overall accuracy of risk screening while actively burning down the pending compliance backlog.
- **Success Criteria for FDE:** An un-compromised **Human-in-the-Loop (HITL)** architecture where AI generates complete audit trails, risk reasoning summaries, and structured citations, leaving final risk sign-off to a certified compliance officer.

---

### 4. Marcus Leung — VP, Technology

- **Role in Engagement:** Infrastructure, Security, & System Integration Owner.
- **Core Business Context:** Controls a lean team of four IT engineers responsible for maintaining a legacy, custom-built, 12-year-old core system (ClientHub) alongside modern SaaS layers (Salesforce, SharePoint).
- **Key Pain Points:**
  - ClientHub's API is poorly documented and brittle.
  - Existing tech stack operates in silos—none of the 5 core platforms (ClientHub, Salesforce, SharePoint, ComplianceOne, Outlook) natively integrate, forcing manual copy-paste handoffs.
  - Massive security concerns regarding data leakage of sensitive PII (names, addresses, net worth, corporate resolutions) to external LLM providers.
- **Strategic Goals:**
  - Maintain strict enterprise perimeter security and guarantee that client data is not utilized for external model training.
  - Maximize existing software licensing investments (Enterprise Microsoft 365 & Copilot agreements).
  - Ensure long-term technical sustainability—the final system must be easily supported by his 4-person team without requiring niche AI engineering specializations.
- **Success Criteria for FDE:** Clean, documented architecture utilizing standard enterprise integration patterns, utilizing the **Model Context Protocol (MCP)** to securely tie Microsoft Copilot/LLMs into monday.com.

---

## Operational Alignment & Feature Mapping

| Stakeholder                   | Target Metric / KPI                                                 | Required System Feature / Guardrail                                                                                                                                                                                                                                                  |
| :---------------------------- | :------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Claire Nakamura (COO)**     | • Onboarding Time: < 5 Days<br>• Zero Lost Allocations              | • **monday.com Workflow Backbone:** End-to-end tracking of client journeys.<br>• **Scalable Workspace Architecture:** Modular board design ready to replicate for Portfolio Operations.                                                                                              |
| **David Holloway (Ops)**      | • 70% Client Service / 30% Admin<br>• Backlog: < 10 pending reviews | • **Robust LLM Parsing Pipeline:** High-tolerance ingestion engine that reads messy PDFs/scans.<br>• **Automated Workspace Alerts:** Real-time push notifications removing manual email dependencies.                                                                                |
| **Priya Sharma (Compliance)** | • Zero Audit Findings<br>• Elevated Screening Accuracy              | • **Explainable AI Guardrails:** Mandatory generation of a `compliance_reasoning` text field for every risk tier allocation.<br>• **HITL Enforcement:** Strict column permissions preventing status mutation to "Onboarded" without manual compliance override.                      |
| **Marcus Leung (IT)**         | • Zero Data Leakage Events<br>• Post-FDE Support Autonomy           | • **Secure API Gateway & MCP Integration:** Connecting Copilot to monday.com natively and securely via Model Context Protocol.<br>• **Comprehensive Documentation:** Full technical runtime runbooks that answer what data leaves the network, where it goes, and how it is secured. |

---

### Edge Cases to Call Out in the Proposal

- Use an explicit human-in-the-loop compliance gate for offshore entities, PEP-adjacent cases, and incomplete source-of-funds packages.
- Treat brittle legacy integrations as a risk area and position monday.com as the workflow layer rather than a replacement for ClientHub, Salesforce, SharePoint, or ComplianceOne.
- Emphasize that the AI output must be explainable, traceable, and suitable for audit review rather than opaque automated decision-making.
