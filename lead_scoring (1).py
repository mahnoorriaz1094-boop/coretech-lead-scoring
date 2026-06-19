"""
lead_scoring.py
----------------
Lead Scoring System for CoreTech Solutions.

Scores each lead from 0-100 based on five weighted factors:
    - Budget            (30 points max)
    - Timeline           (25 points max)
    - Urgency             (20 points max)
    - Company Size      (15 points max)
    - Lead Source        (10 points max)
                          -----------------
                          100 points max

Outputs, for each lead:
    - lead_score          : int (0-100)
    - priority            : "High" / "Medium" / "Low"
    - service_recommendation : str
    - explanation         : short human-readable justification

Usage:
    python lead_scoring.py coretech_leads.csv scored_leads.csv
"""

import sys
import pandas as pd


# ---------------------------------------------------------------------------
# 1. SCORING RULES
# ---------------------------------------------------------------------------
# Each rule below maps a raw field value to a sub-score. Weights were chosen
# to reflect typical B2B sales priorities: ability to pay (budget) and speed
# to close (timeline/urgency) matter most; company size and channel quality
# matter, but less.

BUDGET_BANDS = [
    # (min_inclusive, max_inclusive_or_None, points)
    (100000, None, 30),
    (50000, 99999, 25),
    (20000, 49999, 18),
    (10000, 19999, 12),
    (5000, 9999, 6),
    (0, 4999, 2),
]

TIMELINE_SCORES = {
    "Immediate (0-2 weeks)": 25,
    "Short-term (1 month)": 20,
    "1-3 months": 14,
    "3-6 months": 8,
    "6+ months / Exploring": 3,
}

URGENCY_SCORES = {
    "Critical": 20,
    "High": 15,
    "Medium": 9,
    "Low": 3,
}

COMPANY_SIZE_SCORES = {
    "500+": 15,
    "201-500": 12,
    "51-200": 9,
    "11-50": 5,
    "1-10": 2,
}

LEAD_SOURCE_SCORES = {
    "Referral": 10,
    "Partner Referral": 10,
    "Trade Show": 8,
    "Webinar": 7,
    "Website Form": 6,
    "LinkedIn": 6,
    "Organic Search": 5,
    "Email Campaign": 4,
    "Paid Ad": 3,
    "Cold Call": 2,
}

PRIORITY_THRESHOLDS = [
    (70, 100, "High"),
    (40, 69, "Medium"),
    (0, 39, "Low"),
]

# Service recommendation: maps the lead's stated interest into the
# standardized service catalog name, while flagging high-value leads
# for a bundled/enterprise offering.
SERVICE_CATALOG = {
    "Cloud Migration": "Cloud Migration & Managed Hosting Package",
    "Custom Software Development": "Custom Software Development Engagement",
    "IT Infrastructure Support": "Managed IT Infrastructure Support Plan",
    "Cybersecurity Audit": "Cybersecurity Audit & Hardening Package",
    "Data Analytics Platform": "Data Analytics & BI Platform Setup",
    "CRM Implementation": "CRM Implementation & Integration",
    "Website & E-commerce Development": "Website / E-commerce Development Package",
    "ERP Integration": "ERP Integration & Workflow Automation",
    "IT Helpdesk Outsourcing": "Outsourced IT Helpdesk Plan",
    "Mobile App Development": "Mobile App Development Engagement",
    "Network Setup & Support": "Network Setup & Support Package",
    "AI/Automation Consulting": "AI & Automation Consulting Engagement",
}


# ---------------------------------------------------------------------------
# 2. SCORING FUNCTIONS
# ---------------------------------------------------------------------------

def score_budget(budget: float) -> int:
    for lo, hi, pts in BUDGET_BANDS:
        if hi is None and budget >= lo:
            return pts
        if hi is not None and lo <= budget <= hi:
            return pts
    return 0


def score_timeline(timeline: str) -> int:
    return TIMELINE_SCORES.get(str(timeline).strip(), 0)


def score_urgency(urgency: str) -> int:
    return URGENCY_SCORES.get(str(urgency).strip(), 0)


def score_company_size(size: str) -> int:
    return COMPANY_SIZE_SCORES.get(str(size).strip(), 0)


def score_lead_source(source: str) -> int:
    return LEAD_SOURCE_SCORES.get(str(source).strip(), 0)


def get_priority(score: int) -> str:
    for lo, hi, label in PRIORITY_THRESHOLDS:
        if lo <= score <= hi:
            return label
    return "Low"


def recommend_service(interested_service: str, score: int) -> str:
    base = SERVICE_CATALOG.get(
        str(interested_service).strip(),
        "General IT Consulting Package"
    )
    if score >= 70:
        return f"{base} (Enterprise/Priority Track)"
    return base


def build_explanation(row: pd.Series, b: int, t: int, u: int, c: int, s: int, total: int, priority: str) -> str:
    """Builds a short, human-readable explanation for the score."""
    drivers = []

    if b >= 25:
        drivers.append(f"strong budget (${row['budget_usd']:,.0f})")
    elif b <= 6:
        drivers.append(f"low budget (${row['budget_usd']:,.0f})")

    if t >= 20:
        drivers.append(f"fast timeline ({row['timeline']})")
    elif t <= 8:
        drivers.append(f"long/unclear timeline ({row['timeline']})")

    if u >= 15:
        drivers.append(f"{row['urgency'].lower()} urgency")
    elif u <= 3:
        drivers.append("low urgency")

    if c >= 12:
        drivers.append(f"large company ({row['company_size']} employees)")
    elif c <= 2:
        drivers.append(f"very small company ({row['company_size']} employees)")

    if s >= 8:
        drivers.append(f"high-quality source ({row['lead_source']})")
    elif s <= 3:
        drivers.append(f"low-intent source ({row['lead_source']})")

    if not drivers:
        drivers.append("balanced, average signals across all factors")

    driver_text = "; ".join(drivers)
    return f"Score {total}/100 ({priority} priority) — driven by {driver_text}."


# ---------------------------------------------------------------------------
# 3. MAIN SCORING PIPELINE
# ---------------------------------------------------------------------------

def score_leads(df: pd.DataFrame) -> pd.DataFrame:
    """Takes a raw leads DataFrame and returns it enriched with scoring columns."""
    df = df.copy()

    budget_pts = df["budget_usd"].apply(score_budget)
    timeline_pts = df["timeline"].apply(score_timeline)
    urgency_pts = df["urgency"].apply(score_urgency)
    size_pts = df["company_size"].apply(score_company_size)
    source_pts = df["lead_source"].apply(score_lead_source)

    df["budget_score"] = budget_pts
    df["timeline_score"] = timeline_pts
    df["urgency_score"] = urgency_pts
    df["company_size_score"] = size_pts
    df["lead_source_score"] = source_pts

    df["lead_score"] = (
        budget_pts + timeline_pts + urgency_pts + size_pts + source_pts
    ).clip(0, 100)

    df["priority"] = df["lead_score"].apply(get_priority)

    df["service_recommendation"] = [
        recommend_service(row["interested_service"], row["lead_score"])
        for _, row in df.iterrows()
    ]

    df["explanation"] = [
        build_explanation(
            row,
            row["budget_score"], row["timeline_score"], row["urgency_score"],
            row["company_size_score"], row["lead_source_score"],
            row["lead_score"], row["priority"]
        )
        for _, row in df.iterrows()
    ]

    return df


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "coretech_leads.csv"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "scored_leads.csv"

    df = pd.read_csv(input_path)
    scored = score_leads(df)
    scored = scored.sort_values("lead_score", ascending=False)
    scored.to_csv(output_path, index=False)

    print(f"Scored {len(scored)} leads -> {output_path}")
    print("\nPriority breakdown:")
    print(scored["priority"].value_counts().to_string())
    print(f"\nAverage lead score: {scored['lead_score'].mean():.1f}")
    print("\nTop 5 leads:")
    print(scored[["lead_id", "company", "lead_score", "priority"]].head(5).to_string(index=False))


if __name__ == "__main__":
    main()
