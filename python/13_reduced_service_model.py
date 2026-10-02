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
# 13 - Reduced Service Feature Model
# =========================================================
#
# Business Question:
# Do the individual internet service features provide
# additional predictive value beyond the main InternetService
# variable when predicting customer churn?
#
# Purpose:
# Test whether removing the seven service-specific variables
# changes churn prediction performance.
#
# Model Refinement:
# Retain InternetService but remove:
# - OnlineSecurity
# - OnlineBackup
# - DeviceProtection
# - TechSupport
# - StreamingTV
# - StreamingMovies
#
# The model uses the same dataset split, preprocessing,
# Logistic Regression configuration, and evaluation metrics
# as the previous models.
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
print("REDUCED SERVICE FEATURE - CHURN MODEL")
print("=" * 70)

print(f"Rows loaded: {len(df):,}")
print(f"Columns loaded: {len(df.columns)}")


# ---------------------------------------------------------
# 3. Define Target
# ---------------------------------------------------------

target = "Churn_Flag"

y = df[target]


# ---------------------------------------------------------
# 4. Define Predictor Features
# ---------------------------------------------------------
#
# This model starts from Model 2.
#
# TotalCharges_Clean remains excluded.
#
# The seven service-specific variables are removed to test
# whether they provide additional predictive information
# beyond InternetService.
# ---------------------------------------------------------

numeric_features = [
    "SeniorCitizen",
    "tenure",
    "MonthlyCharges",
]

categorical_features = [
    "gender",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
]

excluded_features = [
    "customerID",
    "Churn",
    "Churn_Flag",
    "TotalCharges_Clean",
    "Tenure_Band",
    "SeniorCitizen_Status",
    "TotalCharges_Status",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
]


print("\nPredictor features:")

for feature in numeric_features:
    print(f"- {feature}")

for feature in categorical_features:
    print(f"- {feature}")


print("\nExcluded from reduced service model:")

for feature in excluded_features:
    print(f"- {feature}")


# ---------------------------------------------------------
# 5. Create Predictor Dataset
# ---------------------------------------------------------

X = df[numeric_features + categorical_features]


# ---------------------------------------------------------
# 6. Train/Test Split
# ---------------------------------------------------------
#
# Exactly the same split as Models 1, 2, and 3.
# This allows a fair comparison between models.
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
# 7. Numeric Preprocessing
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
# 8. Categorical Preprocessing
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
# 9. Combine Preprocessing
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
# 10. Define Logistic Regression
# ---------------------------------------------------------

model = LogisticRegression(
    max_iter=1000,
    random_state=42,
)


# ---------------------------------------------------------
# 11. Build Modeling Pipeline
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
# 12. Train Model
# ---------------------------------------------------------

print("\nTraining reduced service Logistic Regression model...")

pipeline.fit(
    X_train,
    y_train,
)

print("Model training complete.")


# ---------------------------------------------------------
# 13. Generate Predictions
# ---------------------------------------------------------

y_pred = pipeline.predict(X_test)

y_probability = pipeline.predict_proba(X_test)[:, 1]


# ---------------------------------------------------------
# 14. Calculate Performance Metrics
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# 15. Confusion Matrix
# ---------------------------------------------------------

tn, fp, fn, tp = confusion_matrix(
    y_test,
    y_pred,
).ravel()


# ---------------------------------------------------------
# 16. Display Performance
# ---------------------------------------------------------

print("\nReduced Service Model Performance")
print("-" * 70)

print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"ROC-AUC:   {roc_auc:.4f}")


print("\nConfusion Matrix")
print("-" * 70)

print(
    [
        [tn, fp],
        [fn, tp],
    ]
)

print("\nConfusion Matrix Layout:")
print(
    "[[True Negative, False Positive],"
)
print(
    " [False Negative, True Positive]]"
)


# ---------------------------------------------------------
# 17. Extract Model Coefficients
# ---------------------------------------------------------

feature_names = pipeline.named_steps[
    "preprocessor"
].get_feature_names_out()

coefficients = pipeline.named_steps[
    "model"
].coef_[0]


coefficient_df = pd.DataFrame(
    {
        "feature": feature_names,
        "coefficient": coefficients,
    }
)

coefficient_df["absolute_coefficient"] = (
    coefficient_df["coefficient"].abs()
)

coefficient_df = coefficient_df.sort_values(
    "absolute_coefficient",
    ascending=False,
)


# ---------------------------------------------------------
# 18. Display Strongest Coefficients
# ---------------------------------------------------------

print("\nStrongest reduced service model coefficients")
print("-" * 70)

print(
    coefficient_df[
        [
            "feature",
            "coefficient",
        ]
    ].head(15).to_string(index=False)
)


# ---------------------------------------------------------
# 19. Save Model Performance
# ---------------------------------------------------------

performance_df = pd.DataFrame(
    [
        {
            "model": "Reduced Service Logistic Regression",
            "test_rows": len(X_test),
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "roc_auc": roc_auc,
            "true_negative": tn,
            "false_positive": fp,
            "false_negative": fn,
            "true_positive": tp,
        }
    ]
)


performance_path = (
    OUTPUT_DIR
    / "reduced_service_model_performance.csv"
)

performance_df.to_csv(
    performance_path,
    index=False,
)


# ---------------------------------------------------------
# 20. Save Model Coefficients
# ---------------------------------------------------------

coefficient_path = (
    OUTPUT_DIR
    / "reduced_service_logistic_regression_coefficients.csv"
)

coefficient_df.to_csv(
    coefficient_path,
    index=False,
)


# ---------------------------------------------------------
# 21. Completion Message
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("REDUCED SERVICE MODEL COMPLETE")
print("=" * 70)

print(f"Saved: {performance_path}")
print(f"Saved: {coefficient_path}")