Forward Deployed Engineer Take-Home
Assignment

Crestview Capital Group — AI-Powered Client Onboarding
Transformation

Estimated Preparation Time: 4-6 hours | Interview: 60 min (~30 min presentation &
demonstration + Panel Q&A)

Overview

This assignment simulates a hypothetical FDE engagement where you'll analyze a complex
enterprise scenario, design a strategic transformation proposal, and build a working AI-powered
proof of concept. You will present your strategic proposal and demonstrate your technical
prototype to a panel of interviewers, walking through your approach to both the business and
technical challenges..

The Scenario

Crestview Capital Group is a large global investment management firm (~4,800 employees,
$340B in assets under management, and an existing monday.com customer. They've engaged
monday.com's Forward Deployed Engineering program to embed an FDE — you — for a
6-month on-site engagement to transform their client onboarding operations using monday.com
and AI.

Your Account Executive has provided the following scenario materials. Review all three to build
a complete picture of the engagement before beginning your work.

Scenario Materials

Material 1: Internal Account Brief

Prepared by: Maya Torres, Account Executive | Last Updated: January 2026

Account Overview

Crestview Capital Group is a Top 25 global investment management firm headquartered in New
York. They manage assets for institutional clients (pension funds, endowments, sovereign
wealth funds), high-net-worth individuals, and corporate entities. Their business spans equity,
fixed income, alternatives, and multi-asset strategies.

monday.com Relationship

Detail

Current Seats

Current ARR

Expansion Opportunity

Value

1,500 (IT and PMO — project management)

$650K

600+ seats across Client Operations,
Compliance, and Relationship Management

Executive Sponsor

Claire Nakamura, COO

Crestview's COO secured leadership buy-in for a "digital operations" initiative and specifically
requested an embedded FDE rather than a traditional consulting engagement. monday.com is
currently used only by IT and PMO for project management — Client Operations, Compliance,
and Relationship Management have no existing monday.com footprint. This engagement is a
greenfield deployment into those departments. If the client onboarding pilot delivers measurable
results, Crestview plans to expand monday.com across all three groups (additional 600+ seats)
with a multi-year enterprise commitment.

Key Stakeholders

Name

Claire Nakamura

Title

COO

Role in Engagement

Executive sponsor; owns the
digital operations mandate

David Holloway

Managing Director, Client
Operations

Owns the onboarding
process and operations team

Priya Sharma

Chief Compliance Officer

Regulatory authority; owns
KYC/AML and compliance
reviews

Name

Title

Role in Engagement

Marcus Leung

VP, Technology

Owns infrastructure, security,
and system integrations

Known Context

-  Crestview attempted to automate parts of their onboarding process 10 months ago using
a robotic process automation (RPA) vendor. The implementation was brittle — it broke
whenever form layouts changed, couldn't handle exceptions, and created more work for
the operations team than it saved. David Holloway led that initiative and is cautious
about technology promises as a result.

-  Crestview has an enterprise Microsoft 365 / CoPilot agreement. The technology team

has been exploring whether existing AI tools could be leveraged for operational
workflows rather than introducing new vendor dependencies.

-  Relationship managers are under significant pressure — they spend the majority of their
time on onboarding paperwork instead of serving clients. Two senior RMs left in the past
quarter, citing administrative burden as a factor. The Head of Wealth Management has
made reducing RM administrative workload a top priority.

Material 2: Discovery Session Transcript

Recorded: January 14, 2026 | Attendees: Maya Torres (monday.com AE), Claire Nakamura
(COO), David Holloway (MD, Client Operations), Priya Sharma (Chief Compliance Officer),
Marcus Leung (VP, Technology)

Maya: Thank you all for making time today. As we discussed, monday.com is committing one of
our Forward Deployed Engineers to work on-site with your team for the next six months. I want
to make sure we give them the full picture before they start. Claire, do you want to set the
stage?

Claire: Of course. So the board reviewed our operational efficiency metrics last quarter and the
message was clear — our client onboarding process is too slow, too manual, and it's costing us
business. We had a prospective institutional client last quarter — a $200 million allocation —
and they went with a competitor because our onboarding process took four weeks and the
competitor did it in five days. That's unacceptable. We need to modernize how we bring clients
onto the platform, and I believe monday.com combined with AI can be the backbone of that
transformation. I specifically asked for an embedded engineer because I'm done with
consultants who hand us a playbook and leave.

Maya: That's exactly the FDE model. David, can you walk us through how onboarding works
today?

David: Sure. So when a new client decides to invest with us, whether it's an institutional
investor like a pension fund or a high-net-worth individual, there's a series of steps before we
can actually manage their money. First, the relationship manager collects the client's information
— who they are, what they want to invest in, how much, their risk tolerance, their tax situation.
For institutional clients, we also need board resolutions, authorized signatory lists, and their
investment policy documents. All of that comes in as a mix of emails, PDFs, scanned forms, and
sometimes physical paper.

Maya: And what happens once you have the information?

David: Our operations team manually enters it into ClientHub — that's our client management
system. They're reading PDFs, pulling out names and dates and dollar amounts, and typing it all
in by hand. Then the package goes to compliance for review.

Priya: That's where my team comes in. Every new client goes through what's called Know Your
Customer — KYC — and anti-money laundering screening. Basically, we need to verify the
client's identity, understand where their money comes from, and screen them against global
sanctions and watchlists. For straightforward clients — say, a U.S.-based pension fund with a
clean track record — this takes about an hour. But for complex cases — international entities,
multi-layered ownership structures, politically connected individuals — a single review can take
my team an entire day.

David: And while compliance is reviewing, everything stops. The relationship manager can't
move forward, the client is waiting, and we're losing goodwill. Right now, we have a backlog of
80-plus compliance reviews at any given time.

Claire: The real pain is that about 60% of what our team does during onboarding is pure data
handling — reading documents, copying information between systems, sending status update
emails. These are smart, experienced people doing clerical work. I want them focused on client
relationships and complex judgment calls, not data entry.

Maya: What systems are involved today?

Marcus: We have five that matter. ClientHub is our core client management system — it's
custom-built, about 12 years old. The API exists but it's poorly maintained and the
documentation is thin. Salesforce is our CRM — that's where relationship managers track their
pipeline and client interactions. SharePoint stores all our documents — onboarding packages,
compliance reports, signed agreements. Outlook handles all communication. And

ComplianceOne is our screening platform for KYC and sanctions checks — it has an API but
we've never integrated it with anything else.

David: The problem is none of these talk to each other. When a relationship manager gets
documents from a client, they email them to operations. Operations manually uploads them to
SharePoint, manually enters the data into ClientHub, then manually creates a compliance
review request. Compliance does their screening in ComplianceOne, writes up findings in a
Word document, and emails it back. Then operations updates ClientHub again. Every handoff is
a manual copy-paste between systems.

Maya: Let's talk about AI. Claire, you mentioned this in our earlier conversations. What's the
vision?

Claire: I want AI handling the repetitive parts of this process. Reading a 30-page investment
policy document and extracting the key information? That should take seconds, not an hour.
Screening a new client against sanctions databases and flagging potential issues? Automated.
Generating a summary of where each client stands in the onboarding pipeline and what's
needed next? Real-time, not a weekly spreadsheet that's outdated by the time someone reads
it. And longer term, I've been reading about AI agents — systems that can orchestrate
multi-step workflows autonomously. I want to understand what's realistic and what's hype.

David: I'll be honest — I'm cautiously optimistic at best. Last year we brought in an RPA vendor
to automate the data entry piece. It was supposed to read incoming documents and populate
ClientHub automatically. It worked in the demo. In production, it broke every time a client sent
documents in a slightly different format. My team spent more time fixing the bot's mistakes than
they would have spent entering the data manually. We pulled the plug after three months.

Claire: Which is why we have an engineer embedded this time, not a vendor running scripts
remotely.

David: Fair. But I need to see that whatever we build actually handles the messiness of real
client documents, not just the clean demo data.

Priya: I want to add something important. Compliance is a regulated function. Our regulators —
the SEC, FINRA, and international equivalents — require us to demonstrate that our client due
diligence is thorough, documented, and defensible. If an AI system is making risk assessments
or flagging clients, I need to know how it arrives at those conclusions. A black box that says "this
client is low risk" without explanation isn't something I can defend in an audit. I need
transparency, I need audit trails, and I need human review on any compliance-related decision.

Marcus: From a technology perspective, I have two concerns. First, data security. Client
information — names, addresses, net worth, investment details — is highly sensitive. If we're
sending that to external AI services, I need to understand the architecture. What data leaves our

network? Where does it go? How is it secured? Second, sustainability. When the FDE leaves in
six months, my team of four needs to be able to support whatever was built. If it requires
specialized AI engineering expertise we don't have, it won't survive.

Maya: Marcus, you mentioned Crestview has a Microsoft CoPilot agreement?

Marcus: Yes. We rolled out CoPilot across the firm last year — mostly for email drafting and
document summarization so far. My team has been wondering whether we could use CoPilot or
other AI tools we're already licensing to interact with monday.com directly. We heard something
about a protocol that lets AI assistants work with external platforms — connects them securely?

Maya: You're thinking of MCP — the Model Context Protocol. monday.com supports it, and it
allows tools like CoPilot, Claude, or ChatGPT to read and write monday.com data directly. That's
absolutely something the FDE can help architect and evaluate for your team.

Claire: Using tools we already pay for to get more out of monday.com — that's a straightforward
conversation with our CFO.

Maya: Let me ask each of you — what does success look like at the end of six months?

Claire: I want to cut our average onboarding time from 23 days to under a week. I want a
working AI-assisted workflow in production — not a proof of concept, something handling real
client onboardings. And I want a clear story for the board about how this scales across the firm.

David: I want my team's time back. Right now, 70% of their day is data handling. If we can flip
that — 70% on actual client service and problem-solving, 30% on administration — that
changes everything. And whatever we build needs to handle edge cases gracefully, not just the
happy path.

Priya: I need compliance accuracy to go up, not down. I want fewer audit findings, not more. If
AI is touching compliance workflows, I need explainability, audit trails, and human sign-off built
into the design. Do that, and I'm an advocate. Skip it, and I'll shut it down.

Marcus: I need clean architecture that my team can maintain. Documentation, standard tooling,
and solutions that leverage our existing Microsoft investment. If it works and it's supportable, I'll
champion the budget for expansion.

Claire: One more thing. If this works for client onboarding, I want the playbook for the rest of our
operations. Our head of portfolio operations has already asked me when it's their turn. So think
about how this scales from day one.

Maya: Understood. The FDE will start on-site February 3rd, beginning with two weeks of deep
discovery. Thank you all.

Material 3: Client Operations — Key Metrics

Source: Crestview Capital Group Operations Dashboard, Q4 2025

Metric

Current

Industry Benchmark  Target

Average Onboarding
Time (New Clients)

Compliance Review
Backlog

Client Onboarding
NPS

Onboarding
Abandonment Rate

Annual Revenue at
Risk (Lost/Delayed
Onboarding)

23 business days

8 business days

5 business days

85 pending reviews  —

24

18%

~$12M

52

5%

—

< 10

55+

< 5%

< $2M

Your Assignment

Part 1: Strategic Transformation Proposal

Prepare and present a strategic proposal for the Crestview client onboarding transformation.
Your audience is Claire Nakamura (COO) and the Crestview leadership team.

Your proposal should address:

1.  Problem Analysis & Business Case — Synthesize the scenario materials to articulate
Crestview's core challenges and connect operational problems to business outcomes.
2.  Solution Architecture — Design an end-to-end solution leveraging monday.com as the

operational backbone. Include:

-  High-level architecture of your monday.com solution
-

Integration architecture with Crestview's existing systems

-  AI capabilities — be specific about what AI approaches you would use, how they
work technically, and why you chose. Be sure to address stakeholder concerns.

-  How you would leverage Crestview's existing technology investments (M365,

CoPilot)

3.  Implementation Roadmap — A phased 6-month plan including:

-  How you would sequence discovery, design, build, and rollout
-  Success metrics aligned to each stakeholder's definition of success
-  Risk analysis and mitigation strategies

4.  Scaling & Product Strategy — How would this solution extend to portfolio operations
and other departments? What product feedback or feature requests would you bring
back to monday.com's product team?

Format:

-  Presentation slides or any format that effectively communicates your proposal to an

executive audience – be concise!

-  You will present this portion in approximately 15-20 minutes

Part 2: Technical Proof of Concept — Intelligent Client Intake
Processing

Claire was intrigued by the AI capabilities in your proposal and has asked to see a working
demonstration. Using the sample data provided below, build a proof of concept that
demonstrates AI-powered client intake processing.

Your POC should demonstrate:

1.  Risk Assessment — Process each client application through an AI model to assess its

risk level and flag any compliance concerns. The model should provide explicit
reasoning for each assessment — not just a label, but an explanation of what patterns or
information informed the judgment. This is the capability Priya's compliance team would
need to trust and act on.

2.  Onboarding Summary Generation — For each application, generate a concise
onboarding summary suitable for the operations team. Each summary should
incorporate the risk assessment context and provide an actionable overview: who is this
client, what do they need, what's the complexity, and what should happen next.
3.  Structured Output — Your pipeline should produce clear, structured results (e.g.,

JSON, CSV, or formatted console output) that could be consumed by a downstream
system or written to a monday.com board.

4.  End-to-End Pipeline — Demonstrate the complete flow: raw application data in → AI
processing → structured, enriched output. The risk assessment should inform the
onboarding summary — these are stages in a pipeline, not independent tasks.

monday.com Integration (Recommended Extension):
If time allows, create a board in a monday.com trial account that models a client onboarding
workflow and populate it with your AI-processed results. This demonstrates the full vision but is
not required — if you run short on time, be prepared to walk through how you would integrate
your pipeline with monday.com and discuss the API approach.

Technical Guidelines:

-  Write your solution in Python, Node.js/TypeScript, or another modern programming

language

-  You may interact with monday.com via the GraphQL API directly, via the monday MCP
with an AI-enabled tool (e.g., Cursor, Claude Desktop), or a combination of approaches
Integrate with at least one AI model provider (e.g., OpenAI, Anthropic, Google Gemini, or
similar) — free tier access is sufficient for this exercise

-

-  Your code should be runnable, demonstrate the complete pipeline and include

appropriate error handling

You will demonstrate this POC live (~10-12 minutes) and should be prepared to:

-  Walk through your code and explain the architecture
-  Discuss your prompt engineering approach and how you iterated on it
-  Explain how you would harden this for production use at Crestview
-  Discuss the limitations and failure modes of your AI integration

AI-Assisted Development

A core expectation of the Forward Deployed Engineer role is the expert use of AI tools to
accelerate delivery and solve complex problems. Throughout your preparation:

-  Use AI tools extensively — We expect you to leverage tools such as Claude, ChatGPT,
Cursor, GitHub Copilot, or similar throughout your work. This includes synthesizing the
scenario materials, designing your architecture, writing code, and preparing your
presentation.

-  Document your approach — Keep notes on how you used AI, including specific

examples of prompts, iterations, and where AI was most or least effective.

-  Be prepared for a deep discussion — We won't just ask "did you use AI?" — we'll

explore how you think about AI as a tool. What was your prompting strategy? How did
you evaluate output quality? Where did you need to intervene or course-correct?

-  Demonstrate expertise, not just usage — We're evaluating your ability to leverage AI
tools at a level you could teach to and implement for an enterprise customer's team.

Deliverables & Presentation

During your interview, you will deliver:

1.  Strategic Transformation Proposal (~15-20 min) — Present your proposal as if Claire
Nakamura and the Crestview leadership team are in the room. Demonstrate your ability
to communicate complex technical concepts with strategic clarity to an executive
audience.

2.  Technical POC Demonstration (~10-15 min) — Walk through your working prototype.

Show the end-to-end pipeline, explain the code, and discuss the AI integration.

3.  Panel Q&A (~20 min) — The panel will explore your strategic thinking, technical depth,

AI expertise, and approach to stakeholder management.

Presentation Format:

-  Slides recommended for Part 1; Part 2 is a live code demonstration
-  Be prepared to make modifications, answer technical questions, or run queries live if

asked

-  Be ready to discuss trade-offs, alternative approaches, and what you would do differently

with more time

Sample Data: Client Applications for POC

Copy the data below into a file named crestview_client_applications.csv. This
dataset represents a batch of new client applications awaiting intake processing.

None

application_id,client_name,client_type,requested_services,estimated_aum,submiss
ion_date,status,description
APP-2026-0301,Greenfield State Pension Fund,Institutional,Equity and Fixed
Income Management,750000000,01/06/2026,New,"State pension fund seeking to
allocate $750M across domestic equity and investment-grade fixed income
strategies. Standard institutional documentation package received including
board resolution, investment policy statement, and authorized signatory list.
Existing relationship with our fixed income team through a prior sub-advisory
arrangement. Requesting standard onboarding timeline."
APP-2026-0302,Margaret and Theodore Ashworth,High-Net-Worth Individual,Wealth
Management,28000000,01/07/2026,New,"Retired couple referred by existing client.
U.S.-based, primary residence in Connecticut. Assets from a combination of
executive compensation, real estate sales, and inheritance. Seeking

discretionary portfolio management with an income focus and moderate risk
tolerance. Standard documentation provided. Straightforward case."
APP-2026-0303,Apex Global Holdings Ltd,Corporate,Multi-Asset
Management,500000000,01/08/2026,New,"Corporate entity registered in an offshore
jurisdiction seeking to open a managed account for multi-asset investment.
Ownership structure involves three layers of intermediate holding companies
across multiple jurisdictions. Beneficial ownership is difficult to determine
from submitted documentation — the listed directors appear to be nominee
directors from a corporate services firm rather than actual principals. Source
of funds documentation references 'diversified business interests' but provides
no supporting detail. Client is requesting expedited processing and has pushed
back on repeated requests for additional ownership and source-of-funds
documentation."
APP-2026-0304,Pacific Northwest Teachers Retirement System,Institutional,Fixed
Income and Real Assets,1200000000,01/09/2026,New,"Public pension fund seeking
to allocate $1.2B across investment-grade fixed income and real asset
strategies. Full documentation package received. Investment committee approval
confirmed. Dedicated relationship manager already assigned. Client has a
10-year track record with a competing firm and is transitioning assets.
Requesting a phased onboarding — $400M initial, remainder over 6 months.
Compliance review expected to be straightforward."
APP-2026-0305,James Okafor,High-Net-Worth Individual,Wealth Management and
Trust Services,42000000,01/10/2026,New,"U.S. citizen currently on a multi-year
overseas work assignment for a multinational energy company. Source of wealth
is executive compensation and stock options from 18-year career. Seeking wealth
management services including a generation-skipping trust and two irrevocable
life insurance trusts. Multiple entity structures will be involved. Requesting
coordination with his estate planning attorney. Moderate complexity due to
international residency and trust structures."
APP-2026-0306,Brightpath University Endowment,Institutional,Equity and
Alternatives,320000000,01/10/2026,New,"University endowment seeking to allocate
$320M across domestic equity, international equity, and alternative strategies
(hedge fund allocation). Investment committee documentation provided. Endowment
has specific ESG exclusion requirements — no fossil fuels, no private prisons,
no tobacco. Board resolution pending final signature. Requesting that
onboarding begin in parallel with the final approval to meet a Q2 funding
deadline."
APP-2026-0307,Velocity Venture Partners LLC,Corporate,Alternative
Investments,85000000,01/12/2026,New,"Venture capital firm seeking to place $85M
in our alternative investment strategies on behalf of their fund's limited
partners. General partner is a former senior government official who left
office 14 months ago — compliance pre-screening recommended due to politically
exposed person (PEP) status. Fund documentation lists investors from multiple
countries across several regions. KYC documentation is partially complete —
missing certified copies of fund formation documents and an updated list of
limited partners."

APP-2026-0308,Linda Vasquez,High-Net-Worth Individual,Wealth
Management,9500000,01/13/2026,New,"Individual client referred through our
branch in San Francisco. Recently divorced, assets are from the divorce
settlement. Seeking conservative portfolio management with a focus on capital
preservation. All standard documentation provided. Straightforward onboarding
expected."
APP-2026-0309,Northern Lights Sovereign Wealth Fund,Institutional,Multi-Asset
Management,2000000000,01/14/2026,New,"Large sovereign wealth fund seeking to
allocate $2B across global equity, fixed income, and real asset strategies.
Extensive due diligence documentation provided. The fund has its own compliance
requirements and is requesting reciprocal KYC — they want to review our
compliance practices as part of their due diligence on us. Requesting a
dedicated onboarding team and weekly status calls. Largest potential new client
relationship this quarter."
APP-2026-0310,Heritage Family Office,Family Office,Comprehensive Wealth
Management,175000000,01/15/2026,New,"Multi-generational family office managing
wealth for 14 family members across three generations. Assets are distributed
across trusts, LLCs, individual accounts, and a family foundation. Requesting
consolidated reporting across all entities, tax-lot accounting, and
coordination with three external advisors (tax attorney, estate planner, and
insurance broker). Previous firm relationship ended due to dissatisfaction with
reporting capabilities. Complex onboarding with an estimated 22 separate
accounts to be established."
APP-2026-0311,Eastbridge Trading Group Ltd,Corporate,Fixed Income
Management,45000000,01/16/2026,New,"Recently incorporated trading company
seeking to invest $45M in short-duration fixed income as a cash management
strategy. Company was formed just 8 months ago with limited operating history.
Beneficial owner is also the sole director. Source of funds is described as
'trading profits' but supporting documentation is minimal — no audited
financials or bank statements provided. Client insists on a compressed
onboarding timeline and has expressed frustration with documentation
requirements. Relationship manager flagged this for compliance pre-review."
APP-2026-0312,Midwest Municipal Workers Union,Institutional,Fixed Income
Management,180000000,01/17/2026,New,"Municipal workers union pension fund
seeking conservative fixed income management for $180M. Full documentation
package received including trust agreement, investment policy statement, and
board resolution. Union has 12,000 members. Investment policy mandates
investment-grade only, no derivatives. Straightforward institutional
onboarding. Client's current manager is retiring and they are transitioning all
assets."
APP-2026-0313,Robert and Diane Mercer-Hastings,High-Net-Worth Individual,Wealth
Management and Estate Planning,67000000,01/18/2026,New,"Husband and wife — he
is CEO of a publicly traded healthcare company; she is a partner at a law firm.
Assets include concentrated stock position ($40M in employer stock), real
estate portfolio, and cash from recent stock sales. Seeking diversification
strategy for the concentrated position, comprehensive wealth management, and
estate planning coordination. Application notes potential 10b5-1 plan

involvement. Requires coordination with corporate counsel on trading window
restrictions."
APP-2026-0314,Global Impact Partners Foundation,Institutional,Impact Investing
and ESG,95000000,01/19/2026,New,"Private foundation focused on climate and
social justice seeking $95M allocation to impact investment strategies.
Requires detailed impact reporting aligned with UN Sustainable Development
Goals. Board has approved investment but requires quarterly narrative reports
on measurable outcomes in addition to financial performance. Foundation is
evaluating three firms simultaneously — onboarding speed and reporting
capabilities are key differentiators in their decision."
APP-2026-0315,R. Ashford (via Introducer),High-Net-Worth Individual,Wealth
Management,120000000,01/20/2026,New,"Individual client with no prior
relationship with Crestview. Initial contact was made through an unaffiliated
third-party introducer who is not a known contact of the firm. Source of wealth
listed as 'private investments and real estate development' with no supporting
documentation provided. Client is requesting that the account be opened in the
name of an offshore trust rather than in their personal name. Has requested
that all communications be routed through their advisor rather than directly to
the client. Declined a standard introductory call with the relationship
manager. No documentation has been submitted beyond the initial application
form."

Resources

-  monday.com Academy — https://monday.com/academy
-  monday.com Knowledge Base — https://support.monday.com
-  monday.com API Reference — https://developer.monday.com/api-reference/
-  API Playground — https://developer.monday.com/api-reference/docs/api-playground
-  monday GraphQL JS SDK npm package -

https://www.npmjs.com/package/@mondaydotcomorg/api

-  monday MCP — https://monday.com/w/mcp
-  monday MCP Setup Guide —

https://support.monday.com/hc/en-us/articles/28588158981266

-  monday vibe — https://developer.monday.com/apps/docs/monday-vibe

Questions?

Feel free to reach out if you have any questions about the assignment.

Good luck from the monday.com team!


