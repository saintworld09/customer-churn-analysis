"""
=========================================================
08 - Statistical Feature Association Analysis
=========================================================

Purpose:
Measure the statistical association between customer
features and churn.

Methods:
- Cramér's V for categorical features
- Point-biserial correlation for numerical features

Important:
Association does not imply causation.

Source:
data/processed/customer_churn_clean.csv

Output:
data/analysis_outputs/statistical_feature_association.csv
=========================================================
"""

from pathlib import Path

import pandas as pd
from scipy.stats import chi2_contingency, pointbiserialr


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

OUTPUT_FILE = (
    OUTPUT_DIR
    / "statistical_feature_association.csv"
)


# =========================================================
# 2. Load cleaned dataset
# =========================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("STATISTICAL FEATURE ASSOCIATION ANALYSIS")
print("=" * 60)

print(f"Rows loaded: {len(df):,}")
print(f"Columns loaded: {len(df.columns)}")


# =========================================================
# 3. Overall churn information
# =========================================================

overall_churn_rate = df["Churn_Flag"].mean() * 100

print(
    f"\nOverall churn rate: "
    f"{overall_churn_rate:.2f}%"
)


# =========================================================
# 4. Define features
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

numeric_features = [
    "tenure",
    "MonthlyCharges",
    "TotalCharges_Clean",
]


# =========================================================
# 5. Cramér's V function
# =========================================================

def calculate_cramers_v(feature, target):
    """
    Calculate Cramér's V between a categorical feature
    and a categorical/binary target.
    """

    contingency_table = pd.crosstab(
        df[feature],
        df[target]
    )

    chi2, _, _, _ = chi2_contingency(
        contingency_table
    )

    n = contingency_table.sum().sum()

    rows, columns = contingency_table.shape

    minimum_dimension = min(
        rows - 1,
        columns - 1
    )

    if minimum_dimension == 0:
        return 0.0

    cramers_v = (
        (chi2 / n)
        / minimum_dimension
    ) ** 0.5

    return cramers_v


# =========================================================
# 6. Calculate categorical associations
# =========================================================

results = []

print("\nCategorical feature associations:")
print("-" * 60)

for feature in categorical_features:

    cramers_v = calculate_cramers_v(
        feature,
        "Churn"
    )

    results.append(
        {
            "feature": feature,
            "feature_type": "Categorical",
            "association_method": "Cramer's V",
            "association_value": round(
                cramers_v,
                4
            ),
        }
    )

    print(
        f"{feature:<25} "
        f"Cramer's V = {cramers_v:.4f}"
    )


# =========================================================
# 7. Calculate numerical associations
# =========================================================

print("\nNumerical feature associations:")
print("-" * 60)

for feature in numeric_features:

    analysis_data = df[
        [feature, "Churn_Flag"]
    ].dropna()

    correlation, p_value = pointbiserialr(
        analysis_data["Churn_Flag"],
        analysis_data[feature]
    )

    results.append(
        {
            "feature": feature,
            "feature_type": "Numerical",
            "association_method": (
                "Point-biserial correlation"
            ),
            "association_value": round(
                correlation,
                4
            ),
        }
    )

    print(
        f"{feature:<25} "
        f"Correlation = {correlation:.4f} "
        f"| p-value = {p_value:.6f}"
    )


# =========================================================
# 8. Create consolidated output
# =========================================================

association_output = pd.DataFrame(results)


# =========================================================
# 9. Add absolute association value
# =========================================================

association_output["absolute_association"] = (
    association_output[
        "association_value"
    ].abs()
)


# =========================================================
# 10. Sort by absolute association
# =========================================================

association_output = (
    association_output
    .sort_values(
        "absolute_association",
        ascending=False
    )
    .reset_index(drop=True)
)


# =========================================================
# 11. Add association interpretation
# =========================================================

def interpret_association(value):
    """
    Provide a broad descriptive interpretation.

    These labels are deliberately general and should not
    be treated as universal statistical thresholds.
    """

    value = abs(value)

    if value < 0.10:
        return "Very weak"
    elif value < 0.20:
        return "Weak"
    elif value < 0.30:
        return "Moderate"
    elif value < 0.50:
        return "Relatively strong"
    else:
        return "Strong"


association_output["association_description"] = (
    association_output[
        "association_value"
    ].apply(interpret_association)
)


# =========================================================
# 12. Display final results
# =========================================================

print("\nCombined association results:")
print("-" * 60)

print(
    association_output[
        [
            "feature",
            "feature_type",
            "association_method",
            "association_value",
            "association_description",
        ]
    ].to_string(index=False)
)


# =========================================================
# 13. Save output
# =========================================================

association_output.to_csv(
    OUTPUT_FILE,
    index=False
)


# =========================================================
# 14. Completion message
# =========================================================

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)

print(
    f"Saved: {OUTPUT_FILE}"
)