from pathlib import Path

import pandas as pd


# =========================================================
# 14 - Compare Churn Prediction Models
# =========================================================
#
# Purpose:
# Compare the three materially different Logistic Regression
# churn models developed during the modeling stage.
#
# Model 1:
# Baseline Logistic Regression
# Includes TotalCharges_Clean and all service variables.
#
# Model 2:
# Refined Logistic Regression
# Excludes TotalCharges_Clean.
#
# Model 4:
# Reduced Service Logistic Regression
# Excludes TotalCharges_Clean and seven service variables.
#
# Model 3 is intentionally excluded because it only renamed
# "No internet service" to "Not Applicable" and produced
# identical predictive results.
#
# Source:
# data/analysis_outputs/
# =========================================================


# ---------------------------------------------------------
# 1. Locate Project
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "analysis_outputs"
)


# ---------------------------------------------------------
# 2. Define Input Files
# ---------------------------------------------------------

model_1_path = (
    OUTPUT_DIR
    / "model_performance.csv"
)

model_2_path = (
    OUTPUT_DIR
    / "refined_model_performance.csv"
)

model_4_path = (
    OUTPUT_DIR
    / "reduced_service_model_performance.csv"
)


# ---------------------------------------------------------
# 3. Load Model Results
# ---------------------------------------------------------

model_1 = pd.read_csv(model_1_path).iloc[0]

model_2 = pd.read_csv(model_2_path).iloc[0]

model_4 = pd.read_csv(model_4_path).iloc[0]


# ---------------------------------------------------------
# 4. Define Model Information
# ---------------------------------------------------------

models = {
    "Model 1 - Baseline": {
        "data": model_1,
        "predictors": 19,
        "description": (
            "Baseline model including TotalCharges_Clean "
            "and all service variables"
        ),
    },
    "Model 2 - Refined": {
        "data": model_2,
        "predictors": 18,
        "description": (
            "Excludes TotalCharges_Clean"
        ),
    },
    "Model 4 - Reduced Service": {
        "data": model_4,
        "predictors": 12,
        "description": (
            "Excludes TotalCharges_Clean and seven "
            "service-specific variables"
        ),
    },
}


# ---------------------------------------------------------
# 5. Display Header
# ---------------------------------------------------------

print("=" * 75)
print("LOGISTIC REGRESSION CHURN MODEL COMPARISON")
print("=" * 75)


# ---------------------------------------------------------
# 6. Display Model Descriptions
# ---------------------------------------------------------

for model_name, model_info in models.items():

    print(f"\n{model_name}:")
    print(model_info["description"])

    print(
        f"Original predictors: "
        f"{model_info['predictors']}"
    )


# ---------------------------------------------------------
# 7. Define Metrics
# ---------------------------------------------------------

metrics = [
    ("Accuracy", "accuracy"),
    ("Precision", "precision"),
    ("Recall", "recall"),
    ("F1 Score", "f1_score"),
    ("ROC-AUC", "roc_auc"),
]


# ---------------------------------------------------------
# 8. Build Performance Comparison
# ---------------------------------------------------------

comparison_rows = []

for metric_name, column_name in metrics:

    row = {
        "metric": metric_name,
        "model_1_baseline": model_1[column_name],
        "model_2_refined": model_2[column_name],
        "model_4_reduced_service": model_4[column_name],
    }

    comparison_rows.append(row)


comparison_df = pd.DataFrame(comparison_rows)


# ---------------------------------------------------------
# 9. Display Performance Comparison
# ---------------------------------------------------------

print("\nPerformance Comparison")
print("-" * 75)

display_df = comparison_df.copy()

for column in [
    "model_1_baseline",
    "model_2_refined",
    "model_4_reduced_service",
]:
    display_df[column] = display_df[column].map(
        lambda value: f"{value:.4f}"
    )


print(
    display_df.to_string(index=False)
)


# ---------------------------------------------------------
# 10. Calculate Changes from Model 1
# ---------------------------------------------------------

change_from_baseline = comparison_df.copy()

change_from_baseline[
    "model_2_vs_model_1_pp"
] = (
    (
        change_from_baseline["model_2_refined"]
        - change_from_baseline["model_1_baseline"]
    )
    * 100
)

change_from_baseline[
    "model_4_vs_model_1_pp"
] = (
    (
        change_from_baseline["model_4_reduced_service"]
        - change_from_baseline["model_1_baseline"]
    )
    * 100
)


# ---------------------------------------------------------
# 11. Display Changes
# ---------------------------------------------------------

print("\nChange From Baseline")
print("-" * 75)

for _, row in change_from_baseline.iterrows():

    print(f"\n{row['metric']}:")

    print(
        f"  Model 2 vs Model 1: "
        f"{row['model_2_vs_model_1_pp']:+.2f} "
        f"percentage points"
    )

    print(
        f"  Model 4 vs Model 1: "
        f"{row['model_4_vs_model_1_pp']:+.2f} "
        f"percentage points"
    )


# ---------------------------------------------------------
# 12. Confusion Matrix Comparison
# ---------------------------------------------------------

confusion_rows = []

confusion_metrics = [
    ("True Negative", "true_negative"),
    ("False Positive", "false_positive"),
    ("False Negative", "false_negative"),
    ("True Positive", "true_positive"),
]


for metric_name, column_name in confusion_metrics:

    confusion_rows.append(
        {
            "metric": metric_name,
            "model_1_baseline": int(
                model_1[column_name]
            ),
            "model_2_refined": int(
                model_2[column_name]
            ),
            "model_4_reduced_service": int(
                model_4[column_name]
            ),
        }
    )


confusion_df = pd.DataFrame(
    confusion_rows
)


# ---------------------------------------------------------
# 13. Display Confusion Matrix Comparison
# ---------------------------------------------------------

print("\nConfusion Matrix Comparison")
print("-" * 75)

print(
    confusion_df.to_string(index=False)
)


# ---------------------------------------------------------
# 14. Model Complexity Comparison
# ---------------------------------------------------------

complexity_df = pd.DataFrame(
    [
        {
            "model": "Model 1 - Baseline",
            "original_predictors": 19,
            "change_from_previous": "Baseline",
        },
        {
            "model": "Model 2 - Refined",
            "original_predictors": 18,
            "change_from_previous": (
                "Removed TotalCharges_Clean"
            ),
        },
        {
            "model": "Model 4 - Reduced Service",
            "original_predictors": 12,
            "change_from_previous": (
                "Removed seven service variables"
            ),
        },
    ]
)


print("\nModel Complexity")
print("-" * 75)

print(
    complexity_df.to_string(index=False)
)


# ---------------------------------------------------------
# 15. Save Performance Comparison
# ---------------------------------------------------------

performance_output = (
    OUTPUT_DIR
    / "three_model_comparison.csv"
)

comparison_df.to_csv(
    performance_output,
    index=False,
)


# ---------------------------------------------------------
# 16. Save Confusion Matrix Comparison
# ---------------------------------------------------------

confusion_output = (
    OUTPUT_DIR
    / "three_model_confusion_matrix_comparison.csv"
)

confusion_df.to_csv(
    confusion_output,
    index=False,
)


# ---------------------------------------------------------
# 17. Save Model Complexity
# ---------------------------------------------------------

complexity_output = (
    OUTPUT_DIR
    / "three_model_complexity_comparison.csv"
)

complexity_df.to_csv(
    complexity_output,
    index=False,
)


# ---------------------------------------------------------
# 18. Completion Message
# ---------------------------------------------------------

print("\n" + "=" * 75)
print("THREE-MODEL COMPARISON COMPLETE")
print("=" * 75)

print(f"Saved: {performance_output}")
print(f"Saved: {confusion_output}")
print(f"Saved: {complexity_output}")