#!/usr/bin/env python3
"""Validate that the problem set contains 30 rows and expected topic counts."""
import pandas as pd
from pathlib import Path

path = Path("data/problem_set.csv")
df = pd.read_csv(path)
required = {"problem_id", "topic", "problem", "reference_answer", "difficulty"}
missing = required - set(df.columns)
if missing:
    raise SystemExit(f"Missing columns: {sorted(missing)}")
if len(df) != 30:
    raise SystemExit(f"Expected 30 problems; found {len(df)}")
if df["problem_id"].duplicated().any():
    raise SystemExit("Duplicate problem IDs found")
print("Problem set validated: 30 unique problems.")
print(df.groupby("topic").size().to_string())
