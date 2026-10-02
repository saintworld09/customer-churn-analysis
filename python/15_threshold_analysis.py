from pathlib import Path

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# =========================================================
# 15 - Churn Classification Threshold Analysis
# =========================================================
#
# Business Question:
# How does changing the churn classification threshold affect
# the model's ability to identify potential churners?
#
# Purpose:
# Evaluate the trade-off between precision, recall, F1 score,
# and the number of customers flagged for potential churn
# at different probability thresholds.
#
# Model:
# Baseline Logistic Regression
#
# Important:
# The model and test set remain unchanged.
# Only the classification threshold is changed.
#
# Source:
# data/processed/customer_churn_clean.csv
# =========================================================


# ---------------------------------------------------------
# 1. Locate Project and Data
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
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


# ---------------------------------------------------------
# 2. Load Processed Data
# ---------------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("CHURN CLASSIFICATION THRESHOLD ANALYSIS")
print("=" * 70)

print(f"Rows loaded: {len(df):,}")
print(f"Columns loaded: {len(df.columns)}")


# ---------------------------------------------------------
# 3. Define Target
# ---------------------------------------------------------

target = "Churn_Flag"

y = df[target]


# ---------------------------------------------------------
# 4. Define Baseline Model Features
# ---------------------------------------------------------
#
# This is the same predictor specification used by the
# baseline Logistic Regression model.
#
# TotalCharges_Clean is included here.
# ---------------------------------------------------------

numeric_features = [
    "SeniorCitizen",
    "tenure",
    "MonthlyCharges",
    "TotalCharges_Clean",
]

categorical_features = [
    "gender",
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
]


X = df[
    numeric_features + categorical_features
]


# ---------------------------------------------------------
# 5. Train/Test Split
# ---------------------------------------------------------
#
# Keep exactly the same split used by the baseline model.
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)


print("\nDataset split:")
print(f"Training rows: {len(X_train):,}")
print(f"Testing rows:  {len(X_test):,}")

print(
    f"Training churn rate: {y_train.mean():.2%}"
)

print(
    f"Testing churn rate: {y_test.mean():.2%}"
)


# ---------------------------------------------------------
# 6. Numeric Preprocessing
# ---------------------------------------------------------

numeric_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median"),
        ),
        (
            "scaler",
            StandardScaler(),
        ),
    ]
)


# ---------------------------------------------------------
# 7. Categorical Preprocessing
# ---------------------------------------------------------

categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent"),
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
        ),
    ]
)


# ---------------------------------------------------------
# 8. Combine Preprocessing
# ---------------------------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            numeric_features,
        ),
        (
            "categorical",
            categorical_pipeline,
            categorical_features,
        ),
    ]
)


# ---------------------------------------------------------
# 9. Define Baseline Logistic Regression
# ---------------------------------------------------------

model = LogisticRegression(
    max_iter=1000,
    random_state=42,
)


# ---------------------------------------------------------
# 10. Build Pipeline
# ---------------------------------------------------------

pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor,
        ),
        (
            "model",
            model,
        ),
    ]
)


# ---------------------------------------------------------
# 11. Train Baseline Model
# ---------------------------------------------------------

print("\nTraining baseline Logistic Regression model...")

pipeline.fit(
    X_train,
    y_train,
)

print("Model training complete.")


# ---------------------------------------------------------
# 12. Generate Churn Probabilities
# ---------------------------------------------------------
#
# We use probabilities rather than the model's default
# predictions because threshold analysis requires us to
# choose the probability cutoff ourselves.
# ---------------------------------------------------------

churn_probability = pipeline.predict_proba(
    X_test
)[:, 1]


# ---------------------------------------------------------
# 13. Calculate ROC-AUC
# ---------------------------------------------------------
#
# ROC-AUC does not depend on one classification threshold.
# It evaluates discrimination across thresholds.
# ---------------------------------------------------------

roc_auc = roc_auc_score(
    y_test,
    churn_probability,
)


print("\nBaseline Model ROC-AUC")
print("-" * 70)
print(f"ROC-AUC: {roc_auc:.4f}")


# ---------------------------------------------------------
# 14. Define Thresholds
# ---------------------------------------------------------

thresholds = [
    0.30,
    0.35,
    0.40,
    0.45,
    0.50,
    0.55,
    0.60,
    0.65,
    0.70,
]


# ---------------------------------------------------------
# 15. Evaluate Each Threshold
# ---------------------------------------------------------

results = []


for threshold in thresholds:

    # Convert probability into a binary prediction.
    #
    # Probability >= threshold → predicted churn
    # Probability < threshold  → predicted no churn
    y_pred_threshold = (
        churn_probability >= threshold
    ).astype(int)


    # Calculate classification metrics
    accuracy = accuracy_score(
        y_test,
        y_pred_threshold,
    )

    precision = precision_score(
        y_test,
        y_pred_threshold,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        y_pred_threshold,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        y_pred_threshold,
        zero_division=0,
    )


    # Confusion matrix
    tn, fp, fn, tp = confusion_matrix(
        y_test,
        y_pred_threshold,
    ).ravel()


    # Number of customers predicted to churn
    flagged_customers = int(
        y_pred_threshold.sum()
    )

    flagged_percentage = (
        flagged_customers
        / len(y_test)
        * 100
    )


    results.append(
        {
            "threshold": threshold,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "true_negative": tn,
            "false_positive": fp,
            "false_negative": fn,
            "true_positive": tp,
            "flagged_customers": flagged_customers,
            "flagged_percentage": flagged_percentage,
            "roc_auc": roc_auc,
        }
    )


# ---------------------------------------------------------
# 16. Create Results DataFrame
# ---------------------------------------------------------

results_df = pd.DataFrame(results)


# ---------------------------------------------------------
# 17. Display Threshold Results
# ---------------------------------------------------------

print("\nThreshold Performance Comparison")
print("-" * 70)

display_df = results_df.copy()

for column in [
    "accuracy",
    "precision",
    "recall",
    "f1_score",
    "roc_auc",
]:
    display_df[column] = display_df[column].map(
        lambda value: f"{value:.4f}"
    )


display_df["flagged_percentage"] = (
    display_df["flagged_percentage"].map(
        lambda value: f"{value:.2f}%"
    )
)


print(
    display_df[
        [
            "threshold",
            "accuracy",
            "precision",
            "recall",
            "f1_score",
            "flagged_customers",
            "flagged_percentage",
            "true_positive",
            "false_positive",
            "false_negative",
        ]
    ].to_string(index=False)
)


# ---------------------------------------------------------
# 18. Display Threshold Interpretation
# ---------------------------------------------------------

print("\nThreshold Interpretation")
print("-" * 70)

print(
    "Lower thresholds classify more customers as "
    "potential churners."
)

print(
    "Higher thresholds classify fewer customers as "
    "potential churners."
)

print(
    "Lower thresholds generally increase recall while "
    "reducing precision."
)

print(
    "Higher thresholds generally increase precision while "
    "reducing recall."
)


# ---------------------------------------------------------
# 19. Save Threshold Analysis
# ---------------------------------------------------------

output_path = (
    OUTPUT_DIR
    / "churn_threshold_analysis.csv"
)

results_df.to_csv(
    output_path,
    index=False,
)


# ---------------------------------------------------------
# 20. Completion Message
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("THRESHOLD ANALYSIS COMPLETE")
print("=" * 70)

print(f"Saved: {output_path}")