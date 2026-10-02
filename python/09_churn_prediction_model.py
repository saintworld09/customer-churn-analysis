"""
=========================================================
09 - Churn Prediction Model
=========================================================

Purpose:
Build an interpretable Logistic Regression model to
predict customer churn.

The model uses:
- Customer demographic features
- Service features
- Contract information
- Payment information
- Tenure
- Monthly charges
- Total charges

Target:
Churn_Flag

Important:
- Churn_Flag is NOT used as a predictor.
- Churn is NOT used as a predictor.
- Derived fields that duplicate other predictors are excluded.
- Preprocessing is fitted only on the training data.
- Results describe predictive performance, not causation.

Evaluation metrics:
- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

Outputs:
data/analysis_outputs/
    model_performance.csv
    logistic_regression_coefficients.csv
=========================================================
"""

from pathlib import Path

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


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

PERFORMANCE_FILE = (
    OUTPUT_DIR
    / "model_performance.csv"
)

COEFFICIENT_FILE = (
    OUTPUT_DIR
    / "logistic_regression_coefficients.csv"
)


# =========================================================
# 2. Load cleaned dataset
# =========================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("LOGISTIC REGRESSION CHURN MODEL")
print("=" * 60)

print(f"Rows loaded: {len(df):,}")
print(f"Columns loaded: {len(df.columns)}")


# =========================================================
# 3. Define target
# =========================================================

target = "Churn_Flag"

y = df[target]


# =========================================================
# 4. Define predictor features
# =========================================================
#
# We intentionally exclude:
#
# customerID
# Churn
# Churn_Flag
# Tenure_Band
# SeniorCitizen_Status
# TotalCharges_Status
#
# Reasons:
# - customerID is an identifier, not a predictive feature.
# - Churn is the original target label.
# - Churn_Flag is the encoded target.
# - Tenure_Band duplicates tenure.
# - SeniorCitizen_Status duplicates SeniorCitizen.
# - TotalCharges_Status represents whether TotalCharges
#   was recorded rather than the customer's charge amount.
#
# =========================================================

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


feature_columns = (
    numeric_features
    + categorical_features
)

X = df[feature_columns]


print("\nPredictor features:")
for feature in feature_columns:
    print(f"- {feature}")


# =========================================================
# 5. Train/test split
# =========================================================
#
# stratify=y keeps the churn proportion approximately
# consistent between training and test datasets.
#
# random_state makes the result reproducible.
# =========================================================

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
    f"Training churn rate: "
    f"{y_train.mean() * 100:.2f}%"
)

print(
    f"Testing churn rate: "
    f"{y_test.mean() * 100:.2f}%"
)


# =========================================================
# 6. Define preprocessing
# =========================================================

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


categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="most_frequent"
            ),
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
        ),
    ]
)


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


# =========================================================
# 7. Define Logistic Regression model
# =========================================================

model = LogisticRegression(
    max_iter=1000,
    random_state=42,
)


# =========================================================
# 8. Create complete modeling pipeline
# =========================================================

model_pipeline = Pipeline(
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


# =========================================================
# 9. Train model
# =========================================================

print("\nTraining Logistic Regression model...")

model_pipeline.fit(
    X_train,
    y_train,
)

print("Model training complete.")


# =========================================================
# 10. Generate predictions
# =========================================================

y_pred = model_pipeline.predict(X_test)

y_probability = model_pipeline.predict_proba(
    X_test
)[:, 1]


# =========================================================
# 11. Calculate evaluation metrics
# =========================================================

accuracy = accuracy_score(
    y_test,
    y_pred,
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0,
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0,
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0,
)

roc_auc = roc_auc_score(
    y_test,
    y_probability,
)


# =========================================================
# 12. Display model performance
# =========================================================

print("\nModel Performance")
print("-" * 60)

print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"ROC-AUC:   {roc_auc:.4f}")


# =========================================================
# 13. Display confusion matrix
# =========================================================

matrix = confusion_matrix(
    y_test,
    y_pred,
)

print("\nConfusion Matrix")
print("-" * 60)

print(matrix)

print(
    "\nConfusion Matrix Layout:"
)

print(
    "[[True Negative, False Positive],"
)

print(
    " [False Negative, True Positive]]"
)


# =========================================================
# 14. Save model performance
# =========================================================

performance_output = pd.DataFrame(
    [
        {
            "model": "Logistic Regression",
            "test_rows": len(X_test),
            "accuracy": round(
                accuracy,
                4
            ),
            "precision": round(
                precision,
                4
            ),
            "recall": round(
                recall,
                4
            ),
            "f1_score": round(
                f1,
                4
            ),
            "roc_auc": round(
                roc_auc,
                4
            ),
            "true_negative": int(
                matrix[0, 0]
            ),
            "false_positive": int(
                matrix[0, 1]
            ),
            "false_negative": int(
                matrix[1, 0]
            ),
            "true_positive": int(
                matrix[1, 1]
            ),
        }
    ]
)

performance_output.to_csv(
    PERFORMANCE_FILE,
    index=False,
)


# =========================================================
# 15. Extract model coefficients
# =========================================================

trained_preprocessor = (
    model_pipeline.named_steps[
        "preprocessor"
    ]
)

trained_model = (
    model_pipeline.named_steps[
        "model"
    ]
)


feature_names = (
    trained_preprocessor
    .get_feature_names_out()
)

coefficients = (
    trained_model.coef_[0]
)


coefficient_output = pd.DataFrame(
    {
        "feature": feature_names,
        "coefficient": coefficients,
    }
)


coefficient_output[
    "absolute_coefficient"
] = (
    coefficient_output[
        "coefficient"
    ].abs()
)


coefficient_output[
    "direction"
] = coefficient_output[
    "coefficient"
].apply(
    lambda value:
    "Positive association with predicted churn"
    if value > 0
    else "Negative association with predicted churn"
)


coefficient_output = (
    coefficient_output
    .sort_values(
        "absolute_coefficient",
        ascending=False,
    )
    .reset_index(drop=True)
)


# =========================================================
# 16. Save model coefficients
# =========================================================

coefficient_output.to_csv(
    COEFFICIENT_FILE,
    index=False,
)


# =========================================================
# 17. Display strongest model coefficients
# =========================================================

print("\nStrongest model coefficients")
print("-" * 60)

print(
    coefficient_output[
        [
            "feature",
            "coefficient",
            "direction",
        ]
    ]
    .head(15)
    .to_string(index=False)
)


# =========================================================
# 18. Completion message
# =========================================================

print("\n" + "=" * 60)
print("MODEL ANALYSIS COMPLETE")
print("=" * 60)

print(
    f"Saved: {PERFORMANCE_FILE}"
)

print(
    f"Saved: {COEFFICIENT_FILE}"
)