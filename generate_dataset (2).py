"""
generate_dataset.py
--------------------
Generates coretech_leads.csv — a sample dataset of 60 inbound/outbound leads
for CoreTech Solutions (a fictional B2B IT services / software company).

Run:
    python generate_dataset.py

Output:
    coretech_leads.csv  (60 rows, 11 columns)
"""

import csv
import random

random.seed(42)

first_names = ["Ayesha", "Bilal", "Sara", "Hamza", "Mariam", "Usman", "Hina", "Ali",
               "Zainab", "Omar", "Fatima", "Saad", "Nida", "Kamran", "Sana", "Asad",
               "Rabia", "Faraz", "Iqra", "Noman", "Mehak", "Tariq", "Areeba", "Waqas",
               "Sadia", "Imran", "Laraib", "Junaid", "Maham", "Salman", "Aiza", "Rizwan",
               "Komal", "Adeel", "Shazia", "Farhan", "Nimra", "Kashif", "Anosha", "Yasir",
               "Sumaiya", "Bilawal", "Mehwish", "Danish", "Hafsa", "Shahzad", "Amna",
               "Naveed", "Saira", "Furqan", "Madiha", "Zeeshan", "Rida", "Asim",
               "Tooba", "Ahsan", "Hira", "Babar", "Maira"]

last_names = ["Khan", "Ahmed", "Raza", "Malik", "Hussain", "Sheikh", "Iqbal", "Qureshi",
              "Butt", "Chaudhry", "Mahmood", "Aziz", "Farooq", "Javed", "Akhtar",
              "Saeed", "Riaz", "Anwar", "Latif", "Siddiqui"]

companies = [
    "NextGen Retailers", "Skyline Logistics", "BrightPath Edu", "Vertex Manufacturing",
    "Coastal Foods Co", "PrimeHealth Clinics", "Urban Builders Group", "DataSphere Analytics",
    "GreenLeaf Agro", "Metro Transit Systems", "Falcon Security Services", "Horizon Textiles",
    "BlueWave Telecom", "Apex Financial Group", "Silverline Hospitality", "Crescent Energy",
    "Pinnacle Real Estate", "Quantum Robotics", "EverGreen Packaging", "Stellar Media House",
    "TrustBank Microfinance", "Bright Future School Network", "Orbit E-commerce",
    "Ironclad Manufacturing", "CityLink Insurance", "FreshMart Supermarkets",
    "NovaTech Software", "Harvest Valley Farms", "Royal Garments Ltd", "ClearView Optics",
    "Summit Construction", "Lighthouse Legal Services", "RapidShip Couriers",
    "GoldenAge Pharma", "BlueOcean Seafoods", "Pioneer Auto Parts", "Crystal Hotels Group",
    "Unity Healthcare", "Falconwing Airlines", "TechNest Startups", "Maple Dairy Co",
    "RedBrick Realty", "Skyward Aviation", "GreenField Dairy", "Vantage Consulting",
    "BrightSpark Electronics", "Coral Bay Resorts", "Northstar Logistics", "PureWater Utilities",
    "Everest Trading Co", "SunRise Solar Energy", "Citywide Pharmacy Chain", "Blossom Bakery Chain",
    "IronGate Security", "Velocity Sports Gear", "Cedar Valley Furniture", "Hilltop Dairy Farms",
    "Quantum Leap Education", "TrueNorth Insurance", "Patriot Defense Supplies", "BlueSky Airlines Cargo"
]

industries = ["Retail", "Logistics", "Education", "Manufacturing", "Food & Beverage",
              "Healthcare", "Construction", "Technology", "Agriculture", "Transportation",
              "Security", "Textiles", "Telecom", "Finance", "Hospitality", "Energy",
              "Real Estate", "Robotics", "Packaging", "Media", "Insurance", "Pharma",
              "Aviation", "E-commerce"]

lead_sources = ["Referral", "Website Form", "Cold Call", "LinkedIn", "Trade Show",
                "Webinar", "Paid Ad", "Partner Referral", "Email Campaign", "Organic Search"]

services = ["Cloud Migration", "Custom Software Development", "IT Infrastructure Support",
            "Cybersecurity Audit", "Data Analytics Platform", "CRM Implementation",
            "Website & E-commerce Development", "ERP Integration", "IT Helpdesk Outsourcing",
            "Mobile App Development", "Network Setup & Support", "AI/Automation Consulting"]

timelines = ["Immediate (0-2 weeks)", "Short-term (1 month)", "1-3 months", "3-6 months", "6+ months / Exploring"]
company_sizes = ["1-10", "11-50", "51-200", "201-500", "500+"]
urgency_levels = ["Critical", "High", "Medium", "Low"]

rows = []
used_names = set()

for i in range(1, 61):
    while True:
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        name = f"{fn} {ln}"
        if name not in used_names:
            used_names.add(name)
            break

    company = companies[i - 1] if i <= len(companies) else f"{random.choice(companies)} {i}"
    industry = random.choice(industries)
    email = f"{fn.lower()}.{ln.lower()}@{company.lower().replace(' ', '').replace(',', '')[:14]}.com"
    phone = f"+92-3{random.randint(0,4)}{random.randint(0,9)}-{random.randint(1000000,9999999)}"

    source = random.choice(lead_sources)
    company_size = random.choices(company_sizes, weights=[10, 20, 30, 25, 15])[0]
    timeline = random.choices(timelines, weights=[15, 20, 25, 20, 20])[0]
    urgency = random.choices(urgency_levels, weights=[15, 30, 35, 20])[0]
    service = random.choice(services)

    # Budget loosely correlated with company size for realism
    base_budget = {"1-10": (2000, 15000), "11-50": (8000, 40000), "51-200": (25000, 90000),
                   "201-500": (60000, 180000), "500+": (120000, 400000)}[company_size]
    budget = random.randint(base_budget[0], base_budget[1])
    budget = round(budget / 500) * 500  # round to nearest 500

    notes_pool = [
        "Met at industry event, expressed strong interest.",
        "Requested a follow-up demo next week.",
        "Comparing us against two other vendors.",
        "Decision maker confirmed budget internally.",
        "Currently using a competitor, exploring switch.",
        "Referred by an existing client.",
        "Downloaded whitepaper, opened all follow-up emails.",
        "Asked detailed technical questions on call.",
        "Mentioned internal approval still pending.",
        "Reached out directly asking for a quote.",
        "Attended webinar and asked about pricing tiers.",
        "Has urgent compliance deadline driving the project.",
        "Early-stage research, no clear timeline yet.",
        "CFO involved in early conversations.",
        "Wants a pilot project before full rollout.",
    ]
    notes = random.choice(notes_pool)

    rows.append({
        "lead_id": f"L{i:03d}",
        "name": name,
        "company": company,
        "industry": industry,
        "email": email,
        "phone": phone,
        "lead_source": source,
        "company_size": company_size,
        "budget_usd": budget,
        "timeline": timeline,
        "urgency": urgency,
        "interested_service": service,
        "notes": notes,
    })

fieldnames = ["lead_id", "name", "company", "industry", "email", "phone", "lead_source",
              "company_size", "budget_usd", "timeline", "urgency", "interested_service", "notes"]

with open("coretech_leads.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} leads -> coretech_leads.csv")
