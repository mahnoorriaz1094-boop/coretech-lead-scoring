# CoreTech Lead Scoring System

A rule-based lead scoring system for **CoreTech Solutions**, a B2B IT services company.
It takes raw inbound/outbound lead data and outputs a **0–100 score**, a **priority label**
(High / Medium / Low), a **recommended service**, and a **short explanation** for each lead.

##  Project Structure

```
.
├── coretech_leads.csv              # Raw dataset (60 sample leads)
├── scored_leads.csv                # Output: leads with scores, priority, recommendations
├── lead_scoring.py                 # Core scoring engine (importable Python module)
├── generate_dataset.py             # Script used to generate coretech_leads.csv
├── CoreTech_Lead_Scoring.ipynb     # Colab/Jupyter notebook — full walkthrough
└── README.md
```

##  Dataset

`coretech_leads.csv` contains **60 sample leads** with the following columns:

| Column | Description |
|---|---|
| `lead_id` | Unique lead identifier |
| `name`, `company`, `industry` | Contact and company info |
| `email`, `phone` | Contact details |
| `lead_source` | How the lead came in (Referral, Cold Call, Website Form, etc.) |
| `company_size` | Employee count band (1-10, 11-50, 51-200, 201-500, 500+) |
| `budget_usd` | Lead's stated/estimated budget |
| `timeline` | How soon they want to start |
| `urgency` | Self-reported urgency level (Critical/High/Medium/Low) |
| `interested_service` | Service the lead is inquiring about |
| `notes` | Free-text sales notes |

##  Scoring Model

Each lead is scored out of **100 points**, built from five weighted factors:

| Factor | Max Points | Logic |
|---|---|---|
| **Budget** | 30 | Banded: ≥$100k → 30, $50k–99k → 25, $20k–49k → 18, $10k–19k → 12, $5k–9k → 6, <$5k → 2 |
| **Timeline** | 25 | Immediate (0–2 wks) → 25, down to 6+ months/exploring → 3 |
| **Urgency** | 20 | Critical → 20, High → 15, Medium → 9, Low → 3 |
| **Company Size** | 15 | 500+ → 15, down to 1–10 → 2 |
| **Lead Source** | 10 | Referral/Partner Referral → 10, down to Cold Call → 2 |

**Priority labels:**
-  **High**: 70–100
-  **Medium**: 40–69
-  **Low**: 0–39

**Service recommendation:** maps the lead's stated interest to a standardized service
package; leads scoring 70+ are flagged for an "Enterprise/Priority Track."

**Explanation:** a short auto-generated sentence citing the 2–4 strongest signals
(e.g. *"Score 93/100 (High priority) — driven by strong budget ($172,500); fast
timeline (Immediate); critical urgency; large company (201-500 employees)."*)

All weights/thresholds live in clearly labeled dictionaries at the top of
`lead_scoring.py`, so the model is easy to tune without touching the scoring logic.

##  How to Run

### Option A — Google Colab (recommended)
1. Open [Google Colab](https://colab.research.google.com).
2. Upload `CoreTech_Lead_Scoring.ipynb` (File → Upload notebook).
3. Run all cells (Runtime → Run all). **No CSV upload needed** — the dataset is
   embedded in the notebook's first code cell and written to disk automatically.

### Option B — Locally / command line
```bash
pip install pandas matplotlib
python lead_scoring.py coretech_leads.csv scored_leads.csv
```

This prints a priority breakdown and writes the full scored dataset to `scored_leads.csv`.

### Regenerating the sample dataset
```bash
python generate_dataset.py
```

## Example Output

| lead_id | company | lead_score | priority | service_recommendation |
|---|---|---|---|---|
| L017 | Pinnacle Real Estate | 93 | High | Cloud Migration & Managed Hosting Package (Enterprise/Priority Track) |
| L042 | RedBrick Realty | 93 | High | ERP Integration & Workflow Automation (Enterprise/Priority Track) |
| L031 | Summit Construction | 16 | Low | Outsourced IT Helpdesk Plan |

##  Tech Stack
- Python 3
- pandas
- matplotlib (for charts in the notebook)

##  Notes
This is a **rule-based / heuristic** scoring model — ideal for early-stage lead
qualification before historical conversion data exists. If win/loss outcomes become
available later, this can be extended into a supervised ML model (e.g. logistic
regression) using the same underlying features.
