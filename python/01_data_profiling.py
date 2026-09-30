from pathlib import Path
import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Telco-Customer-Churn.csv"
)


# ============================================================
# LOAD RAW DATA
# ============================================================

df = pd.read_csv(DATA_FILE)


# ============================================================
# BASIC DATASET INFORMATION
# ============================================================

print("=" * 70)
print("CUSTOMER CHURN DATASET - INITIAL DATA QUALITY PROFILE")
print("=" * 70)

print("\n1. DATASET SHAPE")
print("-" * 70)
print(f"Rows:    {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")


print("\n2. COLUMN NAMES")
print("-" * 70)

for column in df.columns:
    print(column)


print("\n3. DATA TYPES")
print("-" * 70)

print(df.dtypes)


# ============================================================
# DUPLICATES
# ============================================================

print("\n4. DUPLICATE CHECK")
print("-" * 70)

print(f"Duplicate rows: {df.duplicated().sum():,}")
print(f"Duplicate customer IDs: {df['customerID'].duplicated().sum():,}")


# ============================================================
# MISSING VALUES
# ============================================================

print("\n5. MISSING VALUES")
print("-" * 70)

missing_values = df.isnull().sum()

print(missing_values[missing_values > 0])

if missing_values.sum() == 0:
    print("Pandas detected no standard missing values.")


# ============================================================
# BLANK STRING CHECK
# ============================================================

print("\n6. BLANK STRING CHECK")
print("-" * 70)

blank_counts = {}

for column in df.select_dtypes(include="str").columns:
    blank_count = df[column].astype(str).str.strip().eq("").sum()

    if blank_count > 0:
        blank_counts[column] = blank_count

if blank_counts:
    for column, count in blank_counts.items():
        print(f"{column}: {count:,} blank values")
else:
    print("No blank string values detected.")


# ============================================================
# TOTAL CHARGES INVESTIGATION
# ============================================================

print("\n7. TOTAL CHARGES INVESTIGATION")
print("-" * 70)

total_charges_numeric = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

invalid_total_charges = total_charges_numeric.isna().sum()

print(
    f"Values that cannot be converted to numeric: "
    f"{invalid_total_charges:,}"
)

if invalid_total_charges > 0:
    print("\nRows with invalid TotalCharges values:")

    print(
        df.loc[
            total_charges_numeric.isna(),
            ["customerID", "tenure", "MonthlyCharges", "TotalCharges", "Churn"]
        ].to_string(index=False)
    )


# ============================================================
# NUMERICAL SUMMARY
# ============================================================

print("\n8. NUMERICAL SUMMARY")
print("-" * 70)

print(df.describe())


# ============================================================
# UNIQUE VALUES
# ============================================================

print("\n9. UNIQUE VALUE COUNTS")
print("-" * 70)

for column in df.columns:
    print(f"{column}: {df[column].nunique():,} unique values")


# ============================================================
# CATEGORICAL VALUE INSPECTION
# ============================================================

categorical_columns = [
    "gender",
    "SeniorCitizen",
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
    "Churn"
]

print("\n10. CATEGORICAL VALUE CHECK")
print("-" * 70)

for column in categorical_columns:
    print(f"\n{column}:")
    print(df[column].value_counts(dropna=False))


# ============================================================
# NUMERICAL RANGE CHECK
# ============================================================

print("\n11. NUMERICAL RANGE CHECK")
print("-" * 70)

print(
    f"Tenure - Min: {df['tenure'].min()}, "
    f"Max: {df['tenure'].max()}"
)

print(
    f"Monthly Charges - Min: {df['MonthlyCharges'].min()}, "
    f"Max: {df['MonthlyCharges'].max()}"
)


# ============================================================
# CHURN DISTRIBUTION
# ============================================================

print("\n12. CHURN DISTRIBUTION")
print("-" * 70)

churn_counts = df["Churn"].value_counts()

print(churn_counts)

print("\nChurn percentages:")

churn_percentages = (
    df["Churn"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(churn_percentages)


# ============================================================
# CUSTOMER TENURE CHECK
# ============================================================

print("\n13. ZERO-TENURE CUSTOMERS")
print("-" * 70)

zero_tenure = df[df["tenure"] == 0]

print(f"Customers with zero tenure: {len(zero_tenure):,}")

if len(zero_tenure) > 0:
    print(
        zero_tenure[
            [
                "customerID",
                "tenure",
                "MonthlyCharges",
                "TotalCharges",
                "Churn"
            ]
        ].to_string(index=False)
    )


# ============================================================
# END
# ============================================================

print("\n" + "=" * 70)
print("END OF DATA QUALITY PROFILE")
print("=" * 70)