# Elite Builds LLC — Banking Intelligence Analysis

Analysis of a Utah based residential construction firm. Data analysis with Q1 2026 market context to surface growth opportunities
---

## Repository Structure

```
.
├── scripts/
│   ├── task1_signal_engineering.py   # Task 1: Positive signal derivation
│   ├── task2_rag_dataset.py       # Task 2: RAG JSON generation
│   └── task3_prompt_engineering.py  # Task 3: System prompt + RM action plan
├── output/
│   └── customer_segments.json     # Final RAG-ready segmentation object
├── transactions.json             # Source banking data (20 transactions, Q1 2026)
├── README.md
├── Sympera_AI_Home_Assignment.pdf
└── eda.ipynb                   # Some eda to understand cash flows
```
---

## Quick Start

```bash
#Task 1 — Signal engineering report
python scripts/task1_signal_engineering.py
# Task 2 — Generate RAG dataset (writes output/customer_segments.json)
python scripts/task2_rag_dataset.py
# Task 3 — Print system prompt + bank product recommendation + RM Hook
python scripts/task3_prompt_engineering.py
```

## Task 1:Positive Signal Engineering
### Approach

Transactions are classified into revenue, operating, and strategic-growth
buckets. The resulting metrics are then compared against Q1 2026 industry
benchmarks to identify where Elite Builds diverges from the sector trend.

**Resilience Alpha** — evidence of outperforming the 15% material cost surge:
- `R-1` Margin Outperformance vs Industry — net operating margin vs 4% avg
- `R-2` Inventory Cost Containment Under Inflation — inventory/revenue ratio vs estimated ~46% industry pressure

**Growth Reinvestment** — separating strategic outflows from operational noise:
- `G-1` Capital Expansion — equipment downpayment as counter-cyclical capex
- `G-2` Digital Differentiation Spend — AutoCAD + Local SEO as pipeline investments
- `G-3` Liquidity Discipline Under Expansion — simultaneous capex + savings behaviour

### Console Output (stdout only — no file written)

Running `task1_signal_engineering.py` prints:
- **Financial Snapshot**: Total Revenue, Inventory/Operations/Equipment/Tech costs, Total Operating Expenses, Net Operating Profit, Net Operating Margin, Inventory/Revenue Ratio, Expense Velocity, Growth Reinvestment Ratio, Total Capital Deployed, Asset Turnover Ratio
- **Market Benchmark**: industry, material cost inflation %, avg net margin, credit risk flag
- **Signal Group 1 — Resilience Alpha**: R-1 and R-2 with interpreted narrative
- **Signal Group 2 — Growth Reinvestment**: G-1, G-2, and G-3 with interpreted narrative
- **Summary**: one-paragraph 'Resilient Growth' profile assessment

### Key Assumption

*Expense Velocity* is defined here as total operating expenses (Inventory +
Operations + Equipment + Tech/Growth) divided by client revenue. Saving entries are excluded
---

## Task 2: RAG Dataset Creation 
### Approach
The segmentation JSON is derived programmatically from the same metrics
computed in Task 1
**Segment design:**

- `behavioral`: quantitative metrics (monthly revenue, net margin, inventory/revenue ratio, expense velocity, growth reinvestment %, savings active flag, cash flow status, expense velocity flag) — primary retrieval anchors for RM queries like "show me low-risk growing construction clients"
- `demographics`: firmographic identifiers (business type, industry, location, revenue tier, employee signal) enabling sector-level filtering
- `psychographics`: qualitative signals derived from transaction behaviour (brand affinity from named software/marketing spend; lifestyle and risk profile; vendor strategy from supplier diversity; financial discipline from savings pattern)
- `growth_signals`: named benchmark-relative signals — key differentiators for cross-sell targeting
- `recommended_product`: single most relevant bank product derived from the profile
- `credit_risk_assessment`: `"low"`, `"medium"`, or `"high"` based on expense velocity and margin analysis

### Console Output + File Written

Running `task2_rag_dataset.py` prints:
- Output file path, estimated token count, % of 300-token budget used, and pass/fail status
- Full generated JSON to stdout

### Output: `output/customer_segments.json`

---

## Task 3: Prompt Engineering & RM Action Plan

### System Prompt

The following system prompt was used to generate the Task 2 segmentation
output. It applies persona-based instruction (Senior Banking Intelligence
Analyst) and enforces structural and token constraints.

```
You are a Senior Banking Intelligence Analyst at a commercial bank.
Your specialization is SMB segmentation analysis for Relationship Managers (RMs)
who need concise, actionable intelligence to drive product conversations.

TASK:
Analyze the provided transaction data and market context, then output a
single, valid JSON object representing the customer segmentation profile.

OUTPUT RULES:
- Return ONLY valid JSON. No markdown, no explanations, no preamble.
- Total output must be UNDER 300 tokens.
- Use snake_case for all keys.
- All numeric values must be rounded to 1 decimal place.

REQUIRED SEGMENTS — include all four top-level keys:
1. "behavioral"     : spending trends, margin, expense velocity, cash-flow status
2. "demographics"   : business type, industry, location, revenue tier
3. "psychographics" : brand_affinity (list), lifestyle, risk_profile, vendor_strategy
4. "growth_signals" : named signals referencing market benchmarks

ALSO INCLUDE:
- "recommended_product" : the single most relevant bank product (string)
- "credit_risk_assessment" : "low", "medium", or "high"

TONE & STYLE:
- Analytical and precise — no marketing language
- Values must be data-derived, not generic
- Signal names must reference specific transaction evidence

MARKET CONTEXT PROVIDED:
- Period: Q1 2026, Residential Construction sector
- Industry material cost inflation: 15%
- Average industry net margin: 4%
- Banks flagging firms with high "Expense Velocity" as credit risk
```

### Bank Product Recommendation

**Primary:** Business Growth Line of Credit
**Secondary:** Equipment Term Loan / Financing

Rationale:
1. Active capex deployment alongside positive cash flow signals near-term working capital needs to sustain expansion.
2. A revolving line bridges payment gaps between project milestones.
3. Low expense velocity and 53%+ operating margin make this a creditworthy candidate.
4.Secondary opportunity: Equipment Financing preserves cash reserves while supporting capacity growth.

### Console Output (stdout only — no file written)

Running `task3_prompt_engineering.py` prints:
- The exact system prompt used to generate the Task 2 RAG output
- Bank Product Recommendation (primary product, secondary product, and 4-point rationale)
- RM Hook (2-sentence opener for the client conversation)

### RM Hook

> *"Elite Builds LLC is outperforming every peer in its sector — running a
> 53% operating margin while the rest of the industry scrapes by at 4%, even
> with 15% material cost inflation working against them. I want to make sure
> we're positioned as their growth partner, not just their bank — a Business
> Growth Line of Credit right now would let them move faster on their next
> project without touching the savings discipline that sets them apart."*

---

## Assumptions

1. **Operating expense scope**: Inventory, Operations, Equipment lease, and
   Tech/Growth are counted as operating costs. Savings transfers and the
   Growth capex downpayment are treated as capital allocation, not operating
   drag — consistent with how banks assess Expense Velocity.

2. **Industry inventory baseline**: 35% inventory-to-revenue ratio is used as
   the pre-inflation construction industry baseline (standard mid-market range).
   Under 15% material inflation this rises to ~40.2%, used as the benchmark
   for Signal R-2.

3. **Revenue basis**: Client payment credits only (Revenue category).
   Interest income ($120) is tracked separately and excluded from margin
   calculations to avoid distortion.

4. **Single-month snapshot**: All analysis is based on the 20 March 2026
   transactions provided. Trends and seasonality cannot be confirmed without
   additional periods; signals are flagged as cross-sectional observations.

5. **Token counting**: Estimated as `len(compact_JSON_string) / 4`, which
   is a standard rough approximation. Actual token count may vary slightly
   by tokenizer.
