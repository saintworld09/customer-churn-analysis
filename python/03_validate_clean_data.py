from pathlib import Path
import pandas as pd


# =========================================================
# CUSTOMER CHURN DATASET - PROCESSED DATA VALIDATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "customer_churn_clean.csv"
)


# =========================================================
# 1. LOAD PROCESSED DATA
# =========================================================

df = pd.read_csv(PROCESSED_FILE)

print("=" * 70)
print("CUSTOMER CHURN DATASET - PROCESSED DATA VALIDATION")
print("=" * 70)


# =========================================================
# 2. DATASET STRUCTURE
# =========================================================

print("\n" + "-" * 70)
print("DATASET STRUCTURE")
print("-" * 70)

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns):,}")

print("\nColumns:")

for column in df.columns:
    print(f"- {column}")


# =========================================================
# 3. DUPLICATE VALIDATION
# =========================================================

print("\n" + "-" * 70)
print("DUPLICATE VALIDATION")
print("-" * 70)

print(
    f"Duplicate rows: "
    f"{df.duplicated().sum():,}"
)

print(
    f"Duplicate customer IDs: "
    f"{df['customerID'].duplicated().sum():,}"
)


# =========================================================
# 4. TOTAL CHARGES VALIDATION
# =========================================================

print("\n" + "-" * 70)
print("TOTAL CHARGES VALIDATION")
print("-" * 70)

print(
    f"Recorded charges: "
    f"{(df['TotalCharges_Status'] == 'Recorded').sum():,}"
)

print(
    f"Not recorded: "
    f"{(df['TotalCharges_Status'] == 'Not Recorded').sum():,}"
)

print(
    f"Clean numeric TotalCharges missing: "
    f"{df['TotalCharges_Clean'].isna().sum():,}"
)


# =========================================================
# 5. TENURE BAND VALIDATION
# =========================================================

print("\n" + "-" * 70)
print("TENURE BAND VALIDATION")
print("-" * 70)

print(
    df["Tenure_Band"]
    .value_counts()
    .sort_index()
)


# =========================================================
# 6. SENIOR CITIZEN STATUS VALIDATION
# =========================================================

print("\n" + "-" * 70)
print("SENIOR CITIZEN STATUS VALIDATION")
print("-" * 70)

print(
    df["SeniorCitizen_Status"]
    .value_counts()
)


# =========================================================
# 7. CHURN VALIDATION
# =========================================================

print("\n" + "-" * 70)
print("CHURN VALIDATION")
print("-" * 70)

print(
    f"Churned customers: "
    f"{(df['Churn_Flag'] == 1).sum():,}"
)

print(
    f"Active customers: "
    f"{(df['Churn_Flag'] == 0).sum():,}"
)

print(
    f"Invalid Churn_Flag values: "
    f"{(~df['Churn_Flag'].isin([0, 1])).sum():,}"
)

print(
    f"Churn rate: "
    f"{df['Churn_Flag'].mean() * 100:.2f}%"
)


# =========================================================
# 8. ZERO-TENURE VALIDATION
# =========================================================

print("\n" + "-" * 70)
print("ZERO-TENURE VALIDATION")
print("-" * 70)

zero_tenure = df[df["tenure"] == 0]

print(
    f"Zero-tenure customers: "
    f"{len(zero_tenure):,}"
)

print(
    f"Zero-tenure customers with "
    f"unrecorded TotalCharges: "
    f"{zero_tenure['TotalCharges_Clean'].isna().sum():,}"
)


# =========================================================
# 9. FINAL VALIDATION CHECK
# =========================================================

validation_passed = (
    len(df) == 7043
    and len(df.columns) == 26
    and df.duplicated().sum() == 0
    and df["customerID"].duplicated().sum() == 0
    and df["TotalCharges_Clean"].isna().sum() == 11
    and (df["Churn_Flag"] == 1).sum() == 1869
    and (df["Churn_Flag"] == 0).sum() == 5174
    and (~df["Churn_Flag"].isin([0, 1])).sum() == 0
)


print("\n" + "=" * 70)

if validation_passed:
    print("VALIDATION PASSED")
    print("The processed dataset is ready for downstream analysis.")
else:
    print("VALIDATION FAILED")
    print("Review the validation results above.")

print("=" * 70)