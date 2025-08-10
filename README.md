# 📊 PromptBadge — AI-Assisted Badge Assignment from Business Data

An AI-powered pipeline that ingests **structured business performance data** (CSV or SQL), applies transparent **scoring rules stored in YAML**, assigns a **priority badge** (Top / Medium / Low), and generates **LLM-written performance summaries**.

> ⚠️ Demo only — uses public or synthetic data. No confidential or proprietary data included.

---

## 🔍 Overview

**PromptBadge** combines:
- **Structured data analysis** — using sales, revenue, and customer KPIs
- **Prompt engineering** — generating AI-written performance summaries
- **Config-driven scoring** — rules and thresholds stored in **YAML files** for easy updates

This setup allows you to change scoring logic **without editing code**.

---

## ✨ Key Features

- Load data from **CSV or SQL query**
- Score each entity using **configurable rules in YAML**
- Assign **visual priority badges** using [Shields.io](https://shields.io)
- Generate **AI summaries** linked to real metrics
- Save **full prompts and model responses** for audit and reproducibility

---

## ⚙️ Example Scoring Logic (stored in YAML)

In **PromptBadge**, scoring rules are stored in a `config/scoring.yml` file.  
**YAML** (short for *YAML Ain’t Markup Language*) is a **human-readable format** for structured data, often used for configuration files.

**Example `config/scoring.yml`:**
```yaml
rules:
  sales_units:
    bins:
      - [500, 8]
      - [300, 6]
      - [100, 4]
      - [0, -1]
  revenue:
    bins:
      - [1000000, 4]
      - [500000, 3]
      - [100000, 2]
      - [0, -1]
  new_clients:
    bins:
      - [50, 3]
      - [20, 2]
      - [1, 1]
      - [0, -1]
  repeat_orders:
    bins:
      - [200, 3]
      - [50, 2]
      - [1, 1]
      - [0, -1]
  visited_last_year:
    true: 1
  strategic_region:
    values: ["APAC", "EMEA", "NAM"]
    points: 2
  missing_account_manager:
    when_false_has_manager: -1

badges:
  top:    {min: 18, max: 28}
  medium: {min: 13, max: 17}
  low:    {min: 0, max: 12}
```
### 🧪 Prompt Engineering
### System Prompt
```
You are a business analyst. Given structured performance metrics for an account or region, 
write a 3–4 sentence summary and one-sentence recommendation. 
Reference actual numbers; if data is missing, say so.
```
### User Prompt Template
```
ENTITY: {{name}} (id={{entity_id}})
METRICS:
- Sales (units): {{sales_units}}
- Revenue: {{revenue}}
- New Clients: {{new_clients}}
- Repeat Orders: {{repeat_orders}}
- Region: {{region}}
- Market Visits (last year): {{market_visits}}

SCORING:
- Rule hits: {{rule_hits}}
- Total score: {{score}} → Badge: {{badge}}
```
### 📂 Repo Structure
```
promptbadge/
├─ README.md
├─ config/
│  └─ scoring.yml         # scoring rules and badge thresholds
├─ data/
│  ├─ raw/                # synthetic/public CSV or SQL exports
│  └─ processed/          # cleaned tables
├─ src/
│  ├─ query.py            # load CSV/SQL
│  ├─ scoring.py          # apply rules from YAML
│  ├─ prompts.py          # prompt templates
│  ├─ llm.py              # LLM API wrapper
│  └─ export.py           # save badges, summaries, prompts
├─ artifacts/
│  ├─ prompts/            # saved prompts for audit
│  └─ responses/          # saved model outputs
└─ requirements.txt
```
### 🚀 Getting Started
### 1. Install dependencies
```
pip install -r requirements.txt
```
### 2.Edit scoring rules in YAML

Open `config/scoring.yml` and change thresholds, weights, or badge ranges.

### 2.Run the pipeline
```
python -m src.query --input data/raw/business_data.csv --out data/processed/facts.parquet
python -m src.scoring --in data/processed/facts.parquet --config config/scoring.yml --out data/processed/scored.parquet
python -m src.export --in data/processed/scored.parquet --out reports/badges.csv --save-prompts --save-responses
```
### 🛠️ Technologies
- Python — data processing with pandas/DuckDB
- YAML — human-readable configuration files
- OpenAI API — AI-generated summaries
- Shields.io — badge rendering

### 🔎 Transparency
- Prompts & responses saved for reproducibility
- Uses synthetic or anonymized business data
- Rules stored outside code for flexibility

### 👩‍💻 Author
### Dana Brooks
📧 danatallent@yahoo.com
🔗 LinkedIn

“Turning structured business data + prompts into actionable, traceable signals.”
