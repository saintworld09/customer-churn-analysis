from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "analysis_outputs"
    / "churn_threshold_analysis.csv"
)
OUTPUT_DIR = PROJECT_ROOT / "data" / "analysis_outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


print("=" * 70)
print("CHURN THRESHOLD BUSINESS IMPACT ANALYSIS")
print("=" * 70)


# ---------------------------------------------------------
# Load threshold analysis results
# ---------------------------------------------------------

df = pd.read_csv(INPUT_PATH)

print(f"Rows loaded: {len(df):,}")
print(f"Columns loaded: {len(df.columns)}")


# ---------------------------------------------------------
# Calculate business-impact metrics
# ---------------------------------------------------------

df["churners_captured"] = df["true_positive"]

df["churners_missed"] = df["false_negative"]

df["unnecessary_contacts"] = df["false_positive"]

df["capture_rate"] = (
    df["churners_captured"]
    / (df["churners_captured"] + df["churners_missed"])
    * 100
)

df["contact_efficiency"] = (
    df["churners_captured"]
    / df["flagged_customers"]
    * 100
)

df["miss_rate"] = (
    df["churners_missed"]
    / (df["churners_captured"] + df["churners_missed"])
    * 100
)


# ---------------------------------------------------------
# Select business-focused columns
# ---------------------------------------------------------

business_impact = df[
    [
        "threshold",
        "flagged_customers",
        "flagged_percentage",
        "churners_captured",
        "churners_missed",
        "unnecessary_contacts",
        "capture_rate",
        "miss_rate",
        "contact_efficiency",
        "precision",
        "recall",
        "f1_score",
    ]
].copy()


# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print("\nBusiness Impact by Threshold")
print("-" * 70)

display_df = business_impact.copy()

for column in [
    "flagged_percentage",
    "capture_rate",
    "miss_rate",
    "contact_efficiency",
]:
    display_df[column] = display_df[column].map(
        lambda value: f"{value:.2f}%"
    )

for column in [
    "precision",
    "recall",
    "f1_score",
]:
    display_df[column] = display_df[column].map(
        lambda value: f"{value:.4f}"
    )

print(
    display_df[
        [
            "threshold",
            "flagged_customers",
            "flagged_percentage",
            "churners_captured",
            "churners_missed",
            "unnecessary_contacts",
            "capture_rate",
            "miss_rate",
            "contact_efficiency",
        ]
    ].to_string(index=False)
)


# ---------------------------------------------------------
# Save business-impact analysis
# ---------------------------------------------------------

output_path = (
    OUTPUT_DIR
    / "churn_threshold_business_impact.csv"
)

business_impact.to_csv(output_path, index=False)


print("\n" + "=" * 70)
print("BUSINESS IMPACT ANALYSIS COMPLETE")
print("=" * 70)
print(f"Saved: {output_path}")