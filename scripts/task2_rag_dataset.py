"""
Task 2: RAG Dataset Creation & Summarize
Segments produced:
- behavioral: spending trends and cash-flow patterns
- demographics: firmographic profile
- brand : brand affinity and business lifestyle signals

Output constraint: < 300 tokens  
( can put more robust checek when building for this contraint in production )
Output file: ../output/customer_segments.json
"""

import json
import os
import sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from task1_signal_engineering import (
    load_transactions,
    compute_metrics,
    MARKET_CONTEXT,)


def build_segments(metrics) -> dict:
    """RAG-ready segmentation JSON from computed metrics."""

    # Financial metrics can be rounded off as very high precision is not required 
    margin= round(metrics.net_operating_margin_pct, 1)
    inv_ratio= round(metrics.inventory_revenue_ratio, 1)
    exp_velocity= round(metrics.expense_velocity, 1)
    growth_ratio= round(metrics.growth_reinvestment_ratio, 1)

    segment = {
        "client_id": "elite_builds_llc",
        "period": "2026-Q1",
        "behavioral": {
            "monthly_revenue_usd": int(metrics.total_revenue),
            "net_margin_pct": margin,
            "inventory_rev_ratio_pct": inv_ratio,
            "expense_velocity_pct": exp_velocity,
            "growth_reinvestment_pct": growth_ratio,
            "savings_active": metrics.total_savings_transfer > 0,
            "cash_flow_status": "positive",
            "expense_velocity_flag": "low",
        },
        "demographics": {
            "business_type": "SMB",
            "industry": "residential_construction",
            "location": "Utah, USA",
            "revenue_tier": "mid_market",
        },
        "psychographics": {
            "brand_affinity": ["AutoCAD", "local_SEO_marketing"],
            "lifestyle": "growth_oriented_operator",
            "risk_profile": "calculated_contrarian_investor",
            "financial_discipline": "high",
        },
        "growth_signals": {
            "resilience_alpha": f"margin_{margin}pct_vs_industry_4pct",
            "inventory_containment": f"{inv_ratio}pct_vs_est_industry_40pct",
            "growth_reinvestment": "equipment_capex_plus_tech_plus_savings",
        },
        "recommended_product": "business_growth_line_of_credit",
        "credit_risk_assessment": "low",
    }

    return segment


def count_tokens(obj: dict) -> int:
    """Rough token estimate: len(JSON string) / 4."""
    return len(json.dumps(obj, separators=(",", ":"))) // 4


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    txn_path = os.path.join(base_dir, "transactions.json")
    output_path = os.path.join(base_dir, "output", "customer_segments.json")

    transactions = load_transactions(txn_path)
    metrics = compute_metrics(transactions)
    segment = build_segments(metrics)

    estimated_tokens = count_tokens(segment)

    # Write output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(segment, f, indent=2)

    print("RAG Dataset Generation Complete")
    print(f" Output:           {output_path}")
    print(f" Estimated tokens: ~{estimated_tokens} (limit: 300)")
    print(f"Token budget used: {estimated_tokens / 300 * 100:.1f}%")

    if estimated_tokens > 300:
        print("WARNING: Output exceeds 300-token target.")
    else:
        print("Status: PASS — within 300-token budget")

    print("\nGenerated JSON:")
    print(json.dumps(segment, indent=2))

    return segment


if __name__ == "__main__":
    main()
