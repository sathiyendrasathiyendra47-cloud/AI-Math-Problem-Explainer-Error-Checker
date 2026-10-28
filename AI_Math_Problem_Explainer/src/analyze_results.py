#!/usr/bin/env python3
"""Analyze completed AI Math Capstone results and generate summary CSVs/charts."""
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

REQUIRED = {"ai_tool", "prompt_type", "final_answer_score", "step_accuracy_score", "error_type"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/results.csv", help="Completed results CSV")
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise SystemExit(f"Missing required columns: {', '.join(sorted(missing))}")

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    df["final_answer_score"] = pd.to_numeric(df["final_answer_score"], errors="coerce")
    df["step_accuracy_score"] = pd.to_numeric(df["step_accuracy_score"], errors="coerce")
    for col in ("final_answer_score", "step_accuracy_score"):
        invalid = df[col].dropna().loc[~df[col].dropna().isin([0, 1])]
        if not invalid.empty:
            raise SystemExit(f"{col} must contain only 0, 1, or blank values.")

    final_summary = (df.groupby(["ai_tool", "prompt_type"], dropna=False)
        .agg(total_scored=("final_answer_score", "count"),
             final_answer_accuracy=("final_answer_score", "mean"))
        .reset_index())
    final_summary["final_answer_accuracy_pct"] = final_summary["final_answer_accuracy"] * 100
    final_summary.to_csv(out / "final_answer_summary.csv", index=False)

    step_summary = (df.groupby(["ai_tool", "prompt_type"], dropna=False)
        .agg(steps_scored=("step_accuracy_score", "count"),
             step_accuracy=("step_accuracy_score", "mean"))
        .reset_index())
    step_summary["step_accuracy_pct"] = step_summary["step_accuracy"] * 100
    step_summary.to_csv(out / "step_accuracy_summary.csv", index=False)

    errors = df[df["error_type"].notna() & (df["error_type"].astype(str).str.strip() != "")]
    errors = errors[~errors["error_type"].astype(str).str.lower().isin(["none", "nan"])]
    if errors.empty:
        pd.DataFrame(columns=["error_type", "count"]).to_csv(out / "error_type_summary.csv", index=False)
    else:
        errors.groupby("error_type").size().sort_values(ascending=False).rename("count").to_csv(out / "error_type_summary.csv")

    # Chart 1: accuracy by tool and prompt
    pivot = final_summary.pivot(index="prompt_type", columns="ai_tool", values="final_answer_accuracy_pct")
    ax = pivot.plot(kind="bar", figsize=(10, 6))
    ax.set_ylabel("Final-answer accuracy (%)")
    ax.set_xlabel("Prompt type")
    ax.set_title("Final-Answer Accuracy by AI Tool and Prompt Type")
    ax.set_ylim(0, 100)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(out / "final_answer_accuracy.png", dpi=160)
    plt.close()

    # Chart 2: step accuracy
    pivot2 = step_summary.pivot(index="prompt_type", columns="ai_tool", values="step_accuracy_pct")
    ax = pivot2.plot(kind="bar", figsize=(10, 6))
    ax.set_ylabel("Step accuracy (%)")
    ax.set_xlabel("Prompt type")
    ax.set_title("Step Accuracy by AI Tool and Prompt Type")
    ax.set_ylim(0, 100)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(out / "step_accuracy.png", dpi=160)
    plt.close()

    # Chart 3: error type counts
    err_counts = errors.groupby("error_type").size().sort_values(ascending=False)
    if not err_counts.empty:
        ax = err_counts.plot(kind="bar", figsize=(10, 6))
        ax.set_ylabel("Number of recorded errors")
        ax.set_xlabel("Error type")
        ax.set_title("Recorded Error Types")
        plt.xticks(rotation=35, ha="right")
        plt.tight_layout()
        plt.savefig(out / "error_types.png", dpi=160)
        plt.close()

    print(f"Analysis complete. Outputs saved to: {out.resolve()}")
    print("Reminder: charts are meaningful only after entering real, verified experiment scores.")

if __name__ == "__main__":
    main()
