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
# 12 - Service Category Refinement
# =========================================================
#
# Business Question:
# Does explicitly separating customers with "No internet
# service" from customers who selected "No" for a service
# improve the churn prediction model?
#
# Purpose:
# Test a controlled refinement of the service-related
# categorical variables while keeping the dataset split,
# predictors, preprocessing approach, and Logistic Regression
# configuration consistent with the previous models.
#
# Model Refinement:
# "No internet service" is changed to "Not Applicable" in
# service columns where that category represents customers
# who do not have internet service.
#
# Important:
# This script does not modify the processed source dataset.
# The transformation is applied only to the modeling copy.
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
print("SERVICE CATEGORY REFINEMENT - CHURN MODEL")
print("=" * 70)

print(f"Rows loaded: {len(df):,}")
print(f"Columns loaded: {len(df.columns)}")


# ---------------------------------------------------------
# 3. Create Modeling Copy
# ---------------------------------------------------------

model_df = df.copy()


# ---------------------------------------------------------
# 4. Service Category Refinement
# ---------------------------------------------------------
#
# These columns contain "No internet service" for customers
# whose InternetService value is "No".
#
# We preserve the information but rename the category to
# "Not Applicable" to make the modeling meaning explicit.
# ---------------------------------------------------------

service_columns = [
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
]

for column in service_columns:
    model_df[column] = model_df[column].replace(
        "No internet service",
        "Not Applicable"
    )


print("\nService category refinement:")
print("- 'No internet service' changed to 'Not Applicable'")
print("- Columns refined:")

for column in service_columns:
    print(f"  - {column}")


# ---------------------------------------------------------
# 5. Define Target
# ---------------------------------------------------------

target = "Churn_Flag"

y = model_df[target]


# ---------------------------------------------------------
# 6. Define Predictors
# ---------------------------------------------------------
#
# TotalCharges_Clean remains excluded because Model 2 showed
# that removing it produced a slightly simpler model with
# only a small decrease in ROC-AUC.
#
# The current refinement focuses only on service categories.
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

excluded_features = [
    "customerID",
    "Churn",
    "Churn_Flag",
    "TotalCharges_Clean",
    "Tenure_Band",
    "SeniorCitizen_Status",
    "TotalCharges_Status",
]


print("\nPredictor features:")

for feature in numeric_features:
    print(f"- {feature}")

for feature in categorical_features:
    print(f"- {feature}")


print("\nExcluded from refined model:")

for feature in excluded_features:
    print(f"- {feature}")


# ---------------------------------------------------------
# 7. Train/Test Split
# ---------------------------------------------------------
#
# Keep exactly the same split as Models 1 and 2 so that
# performance differences can be compared fairly.
# ---------------------------------------------------------

X = model_df[numeric_features + categorical_features]

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
# 8. Numeric Preprocessing
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
# 9. Categorical Preprocessing
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
# 10. Combine Preprocessing
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
# 11. Define Logistic Regression
# ---------------------------------------------------------

model = LogisticRegression(
    max_iter=1000,
    random_state=42,
)


# ---------------------------------------------------------
# 12. Build Modeling Pipeline
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
# 13. Train Model
# ---------------------------------------------------------

print("\nTraining service-refined Logistic Regression model...")

pipeline.fit(
    X_train,
    y_train,
)

print("Model training complete.")


# ---------------------------------------------------------
# 14. Generate Predictions
# ---------------------------------------------------------

y_pred = pipeline.predict(X_test)

y_probability = pipeline.predict_proba(X_test)[:, 1]


# ---------------------------------------------------------
# 15. Calculate Performance Metrics
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
# 16. Confusion Matrix
# ---------------------------------------------------------

tn, fp, fn, tp = confusion_matrix(
    y_test,
    y_pred,
).ravel()


# ---------------------------------------------------------
# 17. Display Performance
# ---------------------------------------------------------

print("\nService-Refined Model Performance")
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
# 18. Extract Model Coefficients
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
# 19. Display Strongest Coefficients
# ---------------------------------------------------------

print("\nStrongest service-refined model coefficients")
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
# 20. Save Model Performance
# ---------------------------------------------------------

performance_df = pd.DataFrame(
    [
        {
            "model": "Service Refined Logistic Regression",
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
    / "service_refined_model_performance.csv"
)

performance_df.to_csv(
    performance_path,
    index=False,
)


# ---------------------------------------------------------
# 21. Save Model Coefficients
# ---------------------------------------------------------

coefficient_path = (
    OUTPUT_DIR
    / "service_refined_logistic_regression_coefficients.csv"
)

coefficient_df.to_csv(
    coefficient_path,
    index=False,
)


# ---------------------------------------------------------
# 22. Completion Message
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("SERVICE CATEGORY REFINEMENT COMPLETE")
print("=" * 70)

print(f"Saved: {performance_path}")
print(f"Saved: {coefficient_path}")