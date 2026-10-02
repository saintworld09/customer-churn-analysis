from pathlib import Path
import pandas as pd


# =========================================================
# 11 - Compare Churn Prediction Models
# =========================================================
#
# Business Question:
# How does the refined Logistic Regression model compare
# with the baseline model after removing TotalCharges_Clean?
#
# Purpose:
# Compare predictive performance, confusion-matrix results,
# and model complexity.
#
# Model 1:
# Baseline Logistic Regression
# Includes TotalCharges_Clean
#
# Model 2:
# Refined Logistic Regression
# Excludes TotalCharges_Clean
# =========================================================


# ---------------------------------------------------------
# 1. Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_DIR = PROJECT_ROOT / "data" / "analysis_outputs"

MODEL_1_PATH = OUTPUT_DIR / "model_performance.csv"
MODEL_2_PATH = OUTPUT_DIR / "refined_model_performance.csv"

COMPARISON_PATH = OUTPUT_DIR / "model_comparison.csv"


# ---------------------------------------------------------
# 2. Load model performance files
# ---------------------------------------------------------

model_1 = pd.read_csv(MODEL_1_PATH)
model_2 = pd.read_csv(MODEL_2_PATH)


# ---------------------------------------------------------
# 3. Select the single model result row
# ---------------------------------------------------------

model_1 = model_1.iloc[0]
model_2 = model_2.iloc[0]


# ---------------------------------------------------------
# 4. Metrics to compare
# ---------------------------------------------------------

metrics = [
    ("Accuracy", "accuracy"),
    ("Precision", "precision"),
    ("Recall", "recall"),
    ("F1 Score", "f1_score"),
    ("ROC-AUC", "roc_auc"),
]


# ---------------------------------------------------------
# 5. Build performance comparison
# ---------------------------------------------------------

comparison_rows = []

for display_name, column_name in metrics:

    model_1_value = model_1[column_name]
    model_2_value = model_2[column_name]

    change = model_2_value - model_1_value

    comparison_rows.append(
        {
            "metric": display_name,
            "model_1_baseline": model_1_value,
            "model_2_refined": model_2_value,
            "change": change,
            "change_percentage_points": change * 100,
        }
    )


comparison_df = pd.DataFrame(comparison_rows)


# ---------------------------------------------------------
# 6. Add confusion matrix comparison
# ---------------------------------------------------------

confusion_rows = [
    {
        "metric": "True Negative",
        "model_1_baseline": model_1["true_negative"],
        "model_2_refined": model_2["true_negative"],
        "change": (
            model_2["true_negative"]
            - model_1["true_negative"]
        ),
    },
    {
        "metric": "False Positive",
        "model_1_baseline": model_1["false_positive"],
        "model_2_refined": model_2["false_positive"],
        "change": (
            model_2["false_positive"]
            - model_1["false_positive"]
        ),
    },
    {
        "metric": "False Negative",
        "model_1_baseline": model_1["false_negative"],
        "model_2_refined": model_2["false_negative"],
        "change": (
            model_2["false_negative"]
            - model_1["false_negative"]
        ),
    },
    {
        "metric": "True Positive",
        "model_1_baseline": model_1["true_positive"],
        "model_2_refined": model_2["true_positive"],
        "change": (
            model_2["true_positive"]
            - model_1["true_positive"]
        ),
    },
]


confusion_df = pd.DataFrame(confusion_rows)


# ---------------------------------------------------------
# 7. Display model information
# ---------------------------------------------------------

print("=" * 70)
print("LOGISTIC REGRESSION MODEL COMPARISON")
print("=" * 70)

print()
print("Model 1:")
print("Baseline Logistic Regression")
print("Includes TotalCharges_Clean")

print()
print("Model 2:")
print("Refined Logistic Regression")
print("Excludes TotalCharges_Clean")


# ---------------------------------------------------------
# 8. Display performance comparison
# ---------------------------------------------------------

print()
print("Performance Comparison")
print("-" * 70)

display_df = comparison_df[
    [
        "metric",
        "model_1_baseline",
        "model_2_refined",
        "change_percentage_points",
    ]
].copy()

display_df["model_1_baseline"] = display_df[
    "model_1_baseline"
].map(lambda x: f"{x:.4f}")

display_df["model_2_refined"] = display_df[
    "model_2_refined"
].map(lambda x: f"{x:.4f}")

display_df["change_percentage_points"] = display_df[
    "change_percentage_points"
].map(lambda x: f"{x:+.2f}")

print(display_df.to_string(index=False))


# ---------------------------------------------------------
# 9. Display metric interpretations
# ---------------------------------------------------------

print()
print("Metric Changes")
print("-" * 70)

for _, row in comparison_df.iterrows():

    metric = row["metric"]
    change = row["change_percentage_points"]

    if change > 0:
        direction = "increased"
    elif change < 0:
        direction = "decreased"
    else:
        direction = "did not change"

    print(
        f"{metric}: {direction} by "
        f"{abs(change):.2f} percentage points"
    )


# ---------------------------------------------------------
# 10. Display confusion matrix comparison
# ---------------------------------------------------------

print()
print("Confusion Matrix Comparison")
print("-" * 70)

confusion_display = confusion_df.copy()

confusion_display["model_1_baseline"] = (
    confusion_display["model_1_baseline"].astype(int)
)

confusion_display["model_2_refined"] = (
    confusion_display["model_2_refined"].astype(int)
)

confusion_display["change"] = (
    confusion_display["change"].astype(int)
)

print(confusion_display.to_string(index=False))


# ---------------------------------------------------------
# 11. Display model complexity
# ---------------------------------------------------------

print()
print("Model Complexity")
print("-" * 70)

print("Model 1 predictors: 19")
print("Model 2 predictors: 18")
print("Model 2 removes: TotalCharges_Clean")


# ---------------------------------------------------------
# 12. Save performance comparison
# ---------------------------------------------------------

comparison_df.to_csv(
    COMPARISON_PATH,
    index=False
)


# ---------------------------------------------------------
# 13. Completion message
# ---------------------------------------------------------

print()
print("=" * 70)
print("MODEL COMPARISON COMPLETE")
print("=" * 70)

print(f"Saved: {COMPARISON_PATH}")