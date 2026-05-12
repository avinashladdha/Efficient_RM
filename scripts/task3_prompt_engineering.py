"""
Task 3: Prompt Engineering & RM Action Plan

Documents:
  1. The exact System Prompt used to generate the Task 2 RAG summary
  2. Bank product recommendation rationale
  3. The 2-sentence RM Hook for the Relationship Manager

This script prints all three components and writes them to stdout so they
can be reviewed, audited, and included in the README.
"""

# ---------------------------------------------------------------------------
# System Prompt
# (Persona-based; designed to generate the customer_segments.json from Task 2)
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """
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
""".strip()

# ---------------------------------------------------------------------------
# Bank Product Recommendation
# ---------------------------------------------------------------------------

PRODUCT_RECOMMENDATION = {
    "product": "Business Growth Line of Credit",
    "rationale": [
        "Elite Builds is actively deploying capex (equipment downpayment) "
        "while maintaining positive cash flow — a pattern that signals "
        "near-term working capital needs to sustain the expansion.",

        "A revolving line of credit provides flexible liquidity to bridge "
        "payment gaps between project milestones (client deposits vs. vendor "
        "invoices) without disrupting the firm's savings discipline.",

        "Low expense velocity and 53%+ operating margin make this a "
        "creditworthy candidate — low risk for the bank, high value for the client.",

        "Secondary opportunity: Equipment Financing for the new machinery "
        "being purchased, preserving the firm's cash reserves while supporting "
        "capacity growth.",
    ],
    "secondary_product": "Equipment Term Loan / Financing",
}

# ---------------------------------------------------------------------------
# RM Hook (2 sentences, for direct use in a client conversation)
# ---------------------------------------------------------------------------

RM_HOOK = (
    "Elite Builds LLC is outperforming every peer in its sector — "
    "running a 53% operating margin while the rest of the industry "
    "scrapes by at 4%, even with 15% material cost inflation working against them. "
    "I want to make sure we're positioned as their growth partner, "
    "not just their bank — a Business Growth Line of Credit right now "
    "would let them move faster on their next project without touching "
    "the savings discipline that sets them apart."
)

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def main():
    separator = "=" * 70

    print(separator)
    print("TASK 3: PROMPT ENGINEERING & RM ACTION PLAN")
    print(separator)

    print("\n--- SYSTEM PROMPT (exact, used to generate Task 2 output) ---\n")
    print(SYSTEM_PROMPT)

    print(f"\n{separator}")
    print("BANK PRODUCT RECOMMENDATION")
    print(separator)
    print(f"\nPrimary Product: {PRODUCT_RECOMMENDATION['product']}")
    print(f"Secondary Product: {PRODUCT_RECOMMENDATION['secondary_product']}")
    print("\nRationale:")
    for i, point in enumerate(PRODUCT_RECOMMENDATION["rationale"], 1):
        print(f"  {i}. {point}")

    print(f"\n{separator}")
    print("RM HOOK (2-sentence opener for the client conversation)")
    print(separator)
    print(f"\n{RM_HOOK}\n")


if __name__ == "__main__":
    main()
