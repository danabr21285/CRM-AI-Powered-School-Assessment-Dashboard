# 📊 PromptBadge — AI-Assisted Badge Assignment from Business Data

An AI-powered pipeline that ingests **structured business performance data** (CSV or SQL), applies transparent **scoring rules stored in YAML**, assigns a **priority badge** (Top / Medium / Low), and generates **LLM-written performance summaries**.

> ⚠️ Demo only — uses public or synthetic data. No confidential or proprietary data included.

---

## 🔍 Overview

**PromptBadge** combines:
- **Structured data analysis** — using sales, revenue, and customer KPIs  
- **Prompt engineering** — generating AI-written performance summaries  
- **Config-driven scoring** — rules and thresholds stored in **YAML** for easy updates  

Change scoring logic **without editing code**.

---

## ✨ Key Features

- Load data from **CSV**
- Score each entity using **configurable rules in YAML**
- Assign **visual priority badges** with [Shields.io](https://shields.io)
- (Optional) Generate **AI summaries** linked to metrics
- Save **prompts & responses** for audit (if you wire in an LLM step)

---

## ⚙️ Example Scoring Logic (YAML)

`scoring.yml` (excerpt):

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

---

## 📂 Repo Structure (current layout)

```
.
├─ README.md
├─ business_data.csv        # demo data (CSV)
├─ scoring.yml              # scoring rules + badge thresholds
├─ scoring.py               # applies rules, outputs badges.csv
├─ requirements.txt         # pandas + pyyaml
└─ .github/
   └─ workflows/
      └─ main.yml           # GitHub Actions workflow (demo automation)
```

> Note: `scoring.py` uses `Path`, so ensure it imports `from pathlib import Path`.

---

## 🚀 Getting Started (local)

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Run the scorer
```bash
mkdir -p reports
python scoring.py   --inp business_data.csv   --config scoring.yml   --out reports/badges.csv
```

This writes `reports/badges.csv` with columns like: `name, badge, score, sales_units, revenue, …`.

### 3) (Optional) Create a README-ready table
```bash
python - <<'PY'
import pandas as pd, pathlib
p = pathlib.Path("reports/badges.csv")
df = pd.read_csv(p)
keep = [c for c in ["name","badge","score","sales_units","revenue","new_clients","repeat_orders","region"] if c in df.columns]
out = df.sort_values("score", ascending=False)[keep].head(10)
md = out.to_markdown(index=False)
pathlib.Path("reports/badges_table.md").write_text(md)
print(md)
PY
```

Embed the table (or copy/paste) into the README.

---

## 🤖 Demo Workflow (GitHub Actions)

This repo includes a workflow that **rebuilds badges on each push** (or manually from the Actions tab) and commits results back to `reports/`.

**`.github/workflows/main.yml`:**

```yaml
name: PromptBadge Demo

on:
  push:
    branches: [ main ]
    paths:
      - "business_data.csv"
      - "scoring.yml"
      - "scoring.py"
      - ".github/workflows/main.yml"
  workflow_dispatch: {}

permissions:
  contents: write

jobs:
  run-scoring:
    runs-on: ubuntu-latest
    steps:
      - name: Check out
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Sanity check files exist
        run: |
          test -f business_data.csv || (echo "Missing business_data.csv" && exit 1)
          test -f scoring.yml || (echo "Missing scoring.yml" && exit 1)
          test -f scoring.py || (echo "Missing scoring.py" && exit 1)

      - name: Run scoring
        run: |
          mkdir -p reports
          python scoring.py             --inp business_data.csv             --config scoring.yml             --out reports/badges.csv

      - name: Produce a README-ready markdown table
        run: |
          python - <<'PY'
          import pandas as pd, pathlib
          p = pathlib.Path("reports/badges.csv")
          df = pd.read_csv(p)
          keep = [c for c in ["name","badge","score","sales_units","revenue","new_clients","repeat_orders","region"] if c in df.columns]
          out = df.sort_values("score", ascending=False)[keep].head(10)
          md = out.to_markdown(index=False)
          pathlib.Path("reports/badges_table.md").write_text(md)
          print(md)
          PY

      - name: Upload artifacts (optional)
        uses: actions/upload-artifact@v4
        with:
          name: promptbadge-reports
          path: reports/

      - name: Commit updated reports back to repo
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: update PromptBadge demo reports [skip ci]"
          file_pattern: reports/*.csv reports/*.md
```

### How to run it
- **Automatic:** push any commit to `main` that affects one of the watched files.  
- **Manual:** repo → **Actions** → “PromptBadge Demo” → **Run workflow”.

---

## 🏷️ Badges in the README

Render priority with Shields:

```md
![Top](https://img.shields.io/badge/Priority-Top-brightgreen)
![Medium](https://img.shields.io/badge/Priority-Medium-yellow)
![Low](https://img.shields.io/badge/Priority-Low-lightgrey)
```

## 🏆 Top 10 Accounts

👉 [View latest badge table](reports/badges_table.md)

---

## 🧪 Prompt Engineering (optional)

**System Prompt**
```
You are a business analyst. Given structured performance metrics for an account or region,
write a 3–4 sentence summary and one-sentence recommendation.
Reference actual numbers; if data is missing, say so.
```

**User Prompt Template**
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

---

## 🛠️ Technologies
- Python — pandas
- YAML — human-readable config
- GitHub Actions — automated demo runs
- Shields.io — badge rendering

## 🔎 Transparency
- Rules stored outside code for flexibility
- (Optional) Prompts & responses saved for reproducibility
- Uses synthetic or anonymized business data

---

## 👩‍💻 Author
**Dana Brooks**  
📧 danatallent@yahoo.com  
🔗 LinkedIn

“Turning structured business data + prompts into actionable, traceable signals.”

