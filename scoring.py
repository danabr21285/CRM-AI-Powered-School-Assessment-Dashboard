#!/usr/bin/env python3
"""
scoring.py — Apply YAML-configured scoring rules to business data and assign badges.

Usage:
  python scoring.py --inp data/raw/business_data.csv --config scoring.yml --out reports/badges.csv
"""
import argparse
import json
from typing import Dict, List, Tuple, Any
import pandas as pd
import math

try:
    import yaml  # PyYAML
except ImportError as e:
    raise SystemExit("Missing dependency 'pyyaml'. Install with: pip install pyyaml") from e


def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def bin_points(x: float, bins: List[List[float]]) -> int:
    """Return points for x using bins like [[threshold, points], ...] (assumed descending thresholds)."""
    if x is None or (isinstance(x, float) and math.isnan(x)):
        x = 0
    for thr, pts in bins:
        if x >= thr:
            return int(pts)
    # if nothing matched, fallback to the last bin's points or 0
    return int(bins[-1][1] if bins else 0)


def score_row(row: pd.Series, cfg: Dict[str, Any]) -> Tuple[int, List[str]]:
    rules = cfg.get("rules", {})
    score = 0
    hits: List[str] = []

    # numeric binned metrics
    for col in ("sales_units", "revenue", "new_clients", "repeat_orders"):
        if col in rules and "bins" in rules[col]:
            val = row.get(col, 0)
            pts = bin_points(float(val) if val is not None else 0, rules[col]["bins"])
            score += pts
            hits.append(f"{col}:{val}+{pts}")

    # boolean: visited_last_year → +1 when True
    if "visited_last_year" in rules and rules["visited_last_year"].get("true") is not None:
        if bool(row.get("visited_last_year", False)):
            pts = int(rules["visited_last_year"]["true"])
            score += pts
            hits.append(f"visited_last_year+{pts}")

    # categorical: strategic_region
    if "strategic_region" in rules:
        vals = set(rules["strategic_region"].get("values", []))
        pts = int(rules["strategic_region"].get("points", 0))
        region = row.get("region", None)
        if region in vals:
            score += pts
            hits.append(f"region[{region}]+{pts}")

    # penalty: missing_account_manager (has_account_manager == False)
    if "missing_account_manager" in rules and "when_false_has_manager" in rules["missing_account_manager"]:
        if not bool(row.get("has_account_manager", True)):
            pts = int(rules["missing_account_manager"]["when_false_has_manager"])
            score += pts
            hits.append(f"no_manager{pts}")

    return int(score), hits


def assign_badge(score: int, badge_cfg: Dict[str, Dict[str, int]]) -> str:
    # expected keys: top, medium, low with min/max
    for name in ("top", "medium", "low"):
        rng = badge_cfg.get(name, {})
        if "min" in rng and "max" in rng and rng["min"] <= score <= rng["max"]:
            return name.capitalize()
    # fallback: infer bucket
    if score >= badge_cfg.get("top", {}).get("min", 18):
        return "Top"
    if score >= badge_cfg.get("medium", {}).get("min", 13):
        return "Medium"
    return "Low"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inp", required=True, help="Path to input CSV file")
    ap.add_argument("--config", required=True, help="Path to YAML scoring config")
    ap.add_argument("--out", required=True, help="Path to write output CSV")
    ap.add_argument("--id-col", default="entity_id", help="Primary key column name (default: entity_id)")
    ap.add_argument("--name-col", default="name", help="Display name column (default: name)")
    args = ap.parse_args()

    cfg = load_yaml(args.config)

    # Load data
    df = pd.read_csv(args.inp)

    # Calculate scores and rule hits
    scores: List[int] = []
    hits_all: List[str] = []
    for _, row in df.iterrows():
        s, hits = score_row(row, cfg)
        scores.append(s)
        hits_all.append(" | ".join(hits))

    df_out = df.copy()
    df_out["score"] = scores
    df_out["badge"] = [assign_badge(s, cfg.get("badges", {})) for s in scores]
    df_out["rule_hits"] = hits_all

    # Order columns nicely
    ordered = [c for c in [args.id_col, args.name_col, "badge", "score", "rule_hits"] if c in df_out.columns]
    rest = [c for c in df_out.columns if c not in ordered]
    df_out = df_out[ordered + rest]

    # Save CSV
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df_out.to_csv(out_path, index=False)

    # Print a small summary to stdout
    counts = df_out["badge"].value_counts().to_dict()
    print("Badge distribution:", json.dumps(counts, indent=2))
    print("Wrote:", out_path.as_posix())


if __name__ == "__main__":
    main()
