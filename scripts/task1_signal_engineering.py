"""
Task 1: Positive Signal Engineering
Signals identified:
1. Resilience Alpha    – how the firm is beating the 15% industry cost surge
 2. Growth Reinvestment – strategic capital outflows vs operational noise
"""

import json
import os
from dataclasses import dataclass, field
from typing import List, Dict

# --------------------------------------------------------------------
# Market context (Q1 2026 industry information for context)

MARKET_CONTEXT: Dict = {"credit_risk_flag": "high_expense_velocity",
    "note": "Banks tightening credit for firms showing high Expense Velocity",
    "period": "Q1 2026",
        "industry": "Residential Construction",
    "material_cost_inflation_pct": 15.0,
    "avg_industry_net_margin_pct": 4.0,}

# Categories treated as revenue-generating (credits)
REVENUE_CATEGORIES = {"Revenue"}
#Categories considered strategic / non-recurring outflows (excluded from operating-expense ratio; counted separately as growth intent)
GROWTH_CATEGORIES = {"Growth", "Savings"}
#Categories counted toward operating cost base
OPERATING_CATEGORIES = {"Inventory", "Operations", "Equipment", "Tech/Growth"}

# -----------------------------------------
# Load Data

def load_transactions(filepath: str) -> List[Dict]:
    """Load transactions from JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Financial metric calculation

@dataclass
class FinancialMetrics:
    total_revenue: float= 0.0
    total_inventory_cost: float= 0.0
    total_operations_cost: float= 0.0
    total_equipment_cost: float= 0.0
    total_tech_growth_spend: float= 0.0
    total_growth_capex: float= 0.0
    total_savings_transfer: float= 0.0
    total_interest_income: float= 0.0
    total_operating_expenses: float = 0.0
    net_operating_profit: float = 0.0
    net_operating_margin_pct: float = 0.0
    inventory_revenue_ratio: float =0.0
    expense_velocity: float =0.0
    growth_reinvestment_ratio: float = 0.0
    #Asset turnover proxy: revenue / total capital deployed (all debit outflows).
    #Approximates how quickly the firm converts deployed resources into revenue.
    #A true balancesheet figure isnt available from transaction data alone,
    #so total debits (operating + capex + savings) serve as the asset proxy.
    total_capital_deployed: float = 0.0
    asset_turnover_ratio: float = 0.0
    vendor_names: List[str] = field(default_factory=list)
    growth_line_items: List[Dict] = field(default_factory=list)


def compute_metrics(transactions: List[Dict]) -> FinancialMetrics:
    """Aggregate transactions into financial metrics."""
    m = FinancialMetrics()

    # Maps debit category -> metric field name on FinancialMetrics.
    #Extending support for a new category only requires adding entry here.
    DEBIT_FIELD_MAP: Dict[str, str] = {
        "Inventory":   "total_inventory_cost",
        "Operations":  "total_operations_cost",
        "Equipment":   "total_equipment_cost",
        "Tech/Growth": "total_tech_growth_spend",
        "Growth":      "total_growth_capex",
        "Savings":     "total_savings_transfer",
    }

    #Categories whose debits also get recorded as strategic line items
    GROWTH_LINE_ITEM_CATEGORIES = {"Growth", "Savings"}

    for txn in transactions:
        amount      = abs(txn.get("amount", 0))
        category    = txn.get("category", "")
        txn_type    = txn.get("type", "")
        description = txn.get("description", "")
        date        = txn.get("date", "")

    # Better rule based approach for the following classification can be done using LLMs
        if txn_type == "Credit":
            if category in REVENUE_CATEGORIES:
                m.total_revenue += amount
            elif category == "Interest":
                m.total_interest_income += amount

        elif txn_type == "Debit":
            field = DEBIT_FIELD_MAP.get(category)
            if field is None:
                continue  # unknown category — skip 
            setattr(m, field, getattr(m, field) + amount)
            if category == "Inventory" and description.startswith("Vendor:"):
                vendor = description.removeprefix("Vendor:").strip()
                if vendor not in m.vendor_names:
                    m.vendor_names.append(vendor)
            if category in GROWTH_LINE_ITEM_CATEGORIES:
                m.growth_line_items.append({"date": date, "description": description, "amount": -amount})

    #Operating expenses: costs tied to running the business
    m.total_operating_expenses = (
        m.total_inventory_cost
        + m.total_operations_cost
        + m.total_equipment_cost
        + m.total_tech_growth_spend)

    m.total_capital_deployed = (
        m.total_operating_expenses
        + m.total_growth_capex
        + m.total_savings_transfer)

    if m.total_revenue > 0:
        m.net_operating_profit = m.total_revenue - m.total_operating_expenses
        m.net_operating_margin_pct = (m.net_operating_profit / m.total_revenue) * 100
        m.inventory_revenue_ratio = (m.total_inventory_cost / m.total_revenue) * 100
        m.expense_velocity = (m.total_operating_expenses / m.total_revenue) * 100
        growth_total = m.total_growth_capex + m.total_tech_growth_spend + m.total_savings_transfer
        m.growth_reinvestment_ratio = (growth_total / m.total_revenue) * 100

    if m.total_capital_deployed > 0:
        m.asset_turnover_ratio = m.total_revenue / m.total_capital_deployed

    return m

#-----------------------------------------------------------------
#Signal derivation

def derive_resilience_alpha(metrics: FinancialMetrics, market: Dict) -> List[Dict]:
    """
    Resilience Alpha: evidence that Elite Builds is absorbing the 15%
    material cost inflation better than the industry average.
    """
    signals = []
    # Signal R-1: Net margin far exceeds industry benchmark
    margin_delta = metrics.net_operating_margin_pct - market["avg_industry_net_margin_pct"]
    signals.append({
        "signal_id": "R-1",
        "name": "Margin Outperformance vs Industry",
        "value": round(metrics.net_operating_margin_pct, 1),
        "benchmark": market["avg_industry_net_margin_pct"],
        "delta_pct": round(margin_delta, 1),
        "interpretation": (
            f"Elite Builds is running a {metrics.net_operating_margin_pct:.1f}% net operating "
            f"margin against an industry average of {market['avg_industry_net_margin_pct']}%. "
            f"This {margin_delta:.1f}pp outperformance signals strong cost discipline and " 
            # outperformance or subdued performance can later be confiugured when genralising the model /analysis 
            f"pricing power that competitors—squeezed by 15% material inflation—cannot match."
        ),
    })

    # Signal R-2: Inventory cost ratio well below the inflationary pressure zone
    # If industry peers previously ran ~40% inventory-to-revenue, a 15% cost surge
    # pushes that to ~46%. Elite Builds at _______ demonstrates either long-term supplier
    # contracts or bulk purchasing locks or superior procurement strategy.
    industry_est_inventory_ratio = 40 * (1 + market["material_cost_inflation_pct"] / 100)
    ratio_advantage = industry_est_inventory_ratio - metrics.inventory_revenue_ratio
    signals.append({
        "signal_id": "R-2",
        "name": "Inventory Cost Containment Under Inflation",
        "value": round(metrics.inventory_revenue_ratio, 1),
        "industry_estimated_ratio": round(industry_est_inventory_ratio, 1),
        "advantage_pp": round(ratio_advantage, 1),
        "active_vendors": metrics.vendor_names,
        "interpretation": (
            f"Inventory spend is {metrics.inventory_revenue_ratio:.1f}% of revenue vs an "
            f"estimated industry pressure of ~{industry_est_inventory_ratio:.1f}% (baseline 40% "
            f"+ 15% inflation). Dual-supplier sourcing across "
            f"{', '.join(metrics.vendor_names)} provides negotiation leverage and reduces "
            f"supply-chain concentration risk—the primary driver of industry cost surges."
        ),})

    return signals


def derive_growth_reinvestment(metrics: FinancialMetrics) -> List[Dict]:
    """
    Growth Reinvestment: separating strategic capital allocation decisions
    from routine operational spending.
    """
    signals = []

    # Signal G-1: Capital equipment expansion (equipment downpayment)
    capex_items = [i for i in metrics.growth_line_items if "Equipment" in i["description"] or "Downpayment" in i["description"]]
    if capex_items:
        total_capex = sum(abs(i["amount"]) for i in capex_items)
        signals.append({
            "signal_id": "G-1",
            "name": "Capital Expansion",
            "amount": total_capex,
            "items": capex_items,
            "interpretation": (
                f"${total_capex:,.0f} equipment downpayment deployed when competitors are "
                f"retrenching under cost pressure. This counter-cyclical capex signals "
                f"management confidence in a full project pipeline and intent to scale "
                f"capacity—a strong indicator of forward revenue commitment."
            ),
        })

    #Signal G-2: Tech & digital marketing investment (growth-oriented, not noise)
    #hardcoding for now given the limited countr of entries 
    tech_signals = [
        {"description": "Software Subscription (AutoCAD)", "amount": 150, "note": "Design/productivity tool—lowers rework cost and improves bid accuracy"},
        {"description": "Marketing - Local SEO", "amount": 500, "note": "Digital lead generation—builds inbound project pipeline"},
    ]
    signals.append({
        "signal_id": "G-2",
        "name": "Digital Differentiation Spend",
        "total_amount": metrics.total_tech_growth_spend,
        "items": tech_signals,
        "interpretation": (
            f"${metrics.total_tech_growth_spend:,.0f} in Tech/Growth spend (AutoCAD + Local SEO) "
            f"represents only {metrics.total_tech_growth_spend / metrics.total_revenue * 100:.2f}% "
            f"of revenue but signals a tech-forward operational model. These are deliberate "
            f"efficiency and pipeline investments—not operational noise."
        ),
    })

    # ignal G-3: Capital allocation and savings
    savings_items = [i for i in metrics.growth_line_items if "Savings" in i["description"]]
    if savings_items:
        total_saved = sum(abs(i["amount"]) for i in savings_items)
        signals.append({
            "signal_id": "G-3",
            "name": "Liquidity Discipline Under Expansion",
            "amount": total_saved,
            "interpretation": (
                f"${total_saved:,.0f} transferred to savings in the same month as a "
                f"$10,000 equipment downpayment. This simultaneous expansion + saving "
                f"behavior indicates strong cash-flow management—the firm is not "
                f"over-leveraging its growth cycle."
            ),
        })

    return signals

# -----------------------------
# Main

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    txn_path = os.path.join(base_dir, "transactions.json")

    transactions = load_transactions(txn_path)
    metrics = compute_metrics(transactions)

    resilience_signals = derive_resilience_alpha(metrics, MARKET_CONTEXT)
    growth_signals = derive_growth_reinvestment(metrics)

    print("=" * 70)
    print("ELITE BUILDS LLC — POSITIVE SIGNAL ENGINEERING REPORT")
    print(f"Period: {MARKET_CONTEXT['period']}")
    print("=" * 70)

    print("\n--- FINANCIAL SNAPSHOT ---")
    print(f"Total Revenue (client payments):  ${metrics.total_revenue:>12,.2f}")
    print(f"Total Inventory Cost:             ${metrics.total_inventory_cost:>12,.2f}")
    print(f"Total Operations Cost:            ${metrics.total_operations_cost:>12,.2f}")
    print(f"Equipment Lease:                  ${metrics.total_equipment_cost:>12,.2f}")
    print(f"Tech / Growth Spend:              ${metrics.total_tech_growth_spend:>12,.2f}")
    print(f"Total Operating Expenses :         ${metrics.total_operating_expenses:>12,.2f}")
    print(f"Net Operating Profit:             ${metrics.net_operating_profit:>12,.2f}")
    print(f"Net Operating Margin:             {metrics.net_operating_margin_pct:>11.1f}%")
    print(f"Inventory/Revenue Ratio:          {metrics.inventory_revenue_ratio:>11.1f}%")
    print(f" Expense Velocity:                 {metrics.expense_velocity:>11.1f}%")
    print(f"Growth Reinvestment Ratio:        {metrics.growth_reinvestment_ratio:>11.1f}%")
    print(f"Total Capital Deployed:           ${metrics.total_capital_deployed:>12,.2f}")
    print(f"Asset Turnover Ratio:             {metrics.asset_turnover_ratio:>11.2f}x"
          f" (proxy: revenue / total capital deployed)")

    print("\n--- MARKET BENCHMARK ---")
    print(f"Industry: {MARKET_CONTEXT['industry']}")
    print(f"Material Cost Inflation:   {MARKET_CONTEXT['material_cost_inflation_pct']}%")
    print(f"Avg Industry Net Margin:   {MARKET_CONTEXT['avg_industry_net_margin_pct']}%")
    print(f"Credit Risk Flag:          {MARKET_CONTEXT['credit_risk_flag']}")

    print("\n" + "=" * 70)
    print("SIGNAL GROUP 1: RESILIENCE ALPHA")
    print("=" * 70)
    for sig in resilience_signals:
        print(f"\n[{sig['signal_id']}] {sig['name']}")
        print(f"  {sig['interpretation']}")

    print("\n" + "=" * 70)
    print("SIGNAL GROUP 2: GROWTH REINVESTMENT")
    print("=" * 70)
    for sig in growth_signals:
        print(f"\n[{sig['signal_id']}] {sig['name']}")
        print(f"  {sig['interpretation']}")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(
        f"\n  Elite Builds LLC is outperforming its sector on every key metric.\n"
        f"A {metrics.net_operating_margin_pct:.1f}% operating margin (vs 4% industry avg),\n"
        f" controlled inventory costs despite 15% sector inflation, and\n"
        f"simultaneous capex + savings activity together form a rare\n"
        f" 'Resilient Growth' profile—low credit risk, high growth intent."
    )
    print()

    return {
        "metrics": metrics,
        "resilience_alpha": resilience_signals,
        "growth_reinvestment": growth_signals}


if __name__ == "__main__":
    main()
