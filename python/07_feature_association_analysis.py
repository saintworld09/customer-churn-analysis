"""
=========================================================
07 - Feature Association Analysis
=========================================================

Purpose:
Systematically analyze the relationship between key
customer characteristics and churn.

The analysis includes:
- Churn rates for categorical features
- Churn-rate difference between the highest and lowest
  observed categories
- Numeric feature comparisons between churned and
  non-churned customers

Important:
These results describe associations in the dataset.
They do not establish causal relationships.

Source:
data/processed/customer_churn_clean.csv

Outputs:
data/analysis_outputs/
    feature_association_analysis.csv
    numeric_feature_churn_comparison.csv
=========================================================
"""

from pathlib import Path
import pandas as pd


# =========================================================
# 1. Define project paths
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "customer_churn_clean.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "analysis_outputs"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# 2. Load cleaned dataset
# =========================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("FEATURE ASSOCIATION ANALYSIS")
print("=" * 60)

print(f"Rows loaded: {len(df):,}")
print(f"Columns loaded: {len(df.columns)}")


# =========================================================
# 3. Calculate overall churn rate
# =========================================================

overall_churn_rate = df["Churn_Flag"].mean() * 100

print(f"\nOverall churn rate: {overall_churn_rate:.2f}%")


# =========================================================
# 4. Define categorical features
# =========================================================

categorical_features = [
    "gender",
    "SeniorCitizen_Status",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "Tenure_Band",
    "TotalCharges_Status",
]


# =========================================================
# 5. Analyze categorical features
# =========================================================

association_results = []

for feature in categorical_features:

    grouped = (
        df.groupby(feature, dropna=False)
        .agg(
            customers=("customerID", "count"),
            churned_customers=("Churn_Flag", "sum"),
            churn_rate=("Churn_Flag", "mean"),
        )
        .reset_index()
    )

    grouped["churn_rate"] = grouped["churn_rate"] * 100

    highest_churn = grouped["churn_rate"].max()
    lowest_churn = grouped["churn_rate"].min()

    churn_rate_difference = highest_churn - lowest_churn

    for _, row in grouped.iterrows():

        association_results.append(
            {
                "feature": feature,
                "category": row[feature],
                "customers": int(row["customers"]),
                "churned_customers": int(row["churned_customers"]),
                "churn_rate": round(row["churn_rate"], 2),
                "overall_churn_rate": round(
                    overall_churn_rate,
                    2
                ),
                "difference_vs_overall_pp": round(
                    row["churn_rate"] - overall_churn_rate,
                    2
                ),
                "feature_churn_range_pp": round(
                    churn_rate_difference,
                    2
                ),
            }
        )


categorical_output = pd.DataFrame(association_results)


# =========================================================
# 6. Rank categorical associations
# =========================================================

feature_strength = (
    categorical_output.groupby("feature")
    .agg(
        highest_churn_rate=("churn_rate", "max"),
        lowest_churn_rate=("churn_rate", "min"),
        churn_rate_range_pp=("feature_churn_range_pp", "max"),
    )
    .reset_index()
    .sort_values(
        "churn_rate_range_pp",
        ascending=False
    )
)


# =========================================================
# 7. Display categorical feature summary
# =========================================================

print("\nCategorical feature association summary:")
print("-" * 60)

print(
    feature_strength.to_string(
        index=False
    )
)


# =========================================================
# 8. Define numerical features
# =========================================================

numeric_features = [
    "tenure",
    "MonthlyCharges",
    "TotalCharges_Clean",
]


# =========================================================
# 9. Compare numerical features by churn status
# =========================================================

numeric_results = []

for feature in numeric_features:

    grouped = (
        df.groupby("Churn")[feature]
        .agg(
            customers="count",
            average="mean",
            median="median",
            minimum="min",
            maximum="max",
        )
        .reset_index()
    )

    for _, row in grouped.iterrows():

        numeric_results.append(
            {
                "feature": feature,
                "churn_status": row["Churn"],
                "customers": int(row["customers"]),
                "average": round(row["average"], 2),
                "median": round(row["median"], 2),
                "minimum": round(row["minimum"], 2),
                "maximum": round(row["maximum"], 2),
            }
        )


numeric_output = pd.DataFrame(numeric_results)


# =========================================================
# 10. Calculate numerical differences
# =========================================================

numeric_difference_results = []

for feature in numeric_features:

    churned = df.loc[
        df["Churn"] == "Yes",
        feature
    ].dropna()

    active = df.loc[
        df["Churn"] == "No",
        feature
    ].dropna()

    churned_average = churned.mean()
    active_average = active.mean()

    difference = churned_average - active_average

    numeric_difference_results.append(
        {
            "feature": feature,
            "churned_average": round(
                churned_average,
                2
            ),
            "active_average": round(
                active_average,
                2
            ),
            "difference_churned_minus_active": round(
                difference,
                2
            ),
        }
    )


numeric_difference_output = pd.DataFrame(
    numeric_difference_results
)


# =========================================================
# 11. Save outputs
# =========================================================

categorical_output_file = (
    OUTPUT_DIR
    / "feature_association_analysis.csv"
)

numeric_output_file = (
    OUTPUT_DIR
    / "numeric_feature_churn_comparison.csv"
)

categorical_output.to_csv(
    categorical_output_file,
    index=False
)

numeric_difference_output.to_csv(
    numeric_output_file,
    index=False
)


# =========================================================
# 12. Display numerical comparison
# =========================================================

print("\nNumerical feature comparison:")
print("-" * 60)

print(
    numeric_difference_output.to_string(
        index=False
    )
)


# =========================================================
# 13. Completion message
# =========================================================

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)

print(
    f"Saved: {categorical_output_file}"
)

print(
    f"Saved: {numeric_output_file}"
)