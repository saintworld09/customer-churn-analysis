from pathlib import Path
import pandas as pd


# =========================================================
# CUSTOMER CHURN DATASET - REUSABLE DATA CLEANING PIPELINE
# =========================================================

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "Telco-Customer-Churn.csv"
PROCESSED_FILE = PROJECT_ROOT / "data" / "processed" / "customer_churn_clean.csv"


# =========================================================
# 1. LOAD RAW DATA
# =========================================================

df = pd.read_csv(RAW_FILE)

print("=" * 70)
print("CUSTOMER CHURN DATASET - DATA CLEANING PIPELINE")
print("=" * 70)

print(f"\nRaw dataset shape: {df.shape}")


# =========================================================
# 2. CLEAN TEXT FIELDS
# =========================================================

text_columns = df.select_dtypes(include="str").columns

for column in text_columns:
    df[column] = df[column].str.strip()


# =========================================================
# 3. CLEAN TOTAL CHARGES
# =========================================================

# Preserve the original TotalCharges column.
# Convert the analytical copy to numeric.
df["TotalCharges_Clean"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

# Track whether TotalCharges was recorded.
df["TotalCharges_Status"] = df["TotalCharges_Clean"].apply(
    lambda value: "Not Recorded" if pd.isna(value) else "Recorded"
)


# =========================================================
# 4. CREATE TENURE BAND
# =========================================================

def create_tenure_band(tenure):
    if tenure <= 6:
        return "0–6 Months"
    elif tenure <= 12:
        return "7–12 Months"
    elif tenure <= 24:
        return "13–24 Months"
    elif tenure <= 48:
        return "25–48 Months"
    else:
        return "49–72 Months"


df["Tenure_Band"] = df["tenure"].apply(create_tenure_band)


# =========================================================
# 5. CREATE SENIOR CITIZEN STATUS
# =========================================================

df["SeniorCitizen_Status"] = df["SeniorCitizen"].apply(
    lambda value: (
        "Senior Citizen"
        if value == 1
        else "Non-Senior Citizen"
    )
)


# =========================================================
# 6. CREATE CHURN FLAG
# =========================================================

df["Churn_Flag"] = (
    df["Churn"]
    .map({"Yes": 1, "No": 0})
)


# =========================================================
# 7. VALIDATION
# =========================================================

print("\n" + "-" * 70)
print("CLEANING VALIDATION")
print("-" * 70)

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns):,}")

print(
    f"Duplicate rows: "
    f"{df.duplicated().sum():,}"
)

print(
    f"Duplicate customer IDs: "
    f"{df['customerID'].duplicated().sum():,}"
)

print(
    f"TotalCharges - recorded: "
    f"{(df['TotalCharges_Status'] == 'Recorded').sum():,}"
)

print(
    f"TotalCharges - not recorded: "
    f"{(df['TotalCharges_Status'] == 'Not Recorded').sum():,}"
)

print(
    f"Churned customers: "
    f"{df['Churn_Flag'].sum():,}"
)

print(
    f"Active customers: "
    f"{(df['Churn_Flag'] == 0).sum():,}"
)

print(
    f"Churn rate: "
    f"{df['Churn_Flag'].mean() * 100:.2f}%"
)


# =========================================================
# 8. SAVE PROCESSED DATASET
# =========================================================

df.to_csv(
    PROCESSED_FILE,
    index=False
)

print("\n" + "-" * 70)
print("OUTPUT")
print("-" * 70)

print(f"Processed file saved to:")
print(PROCESSED_FILE)

print("\n" + "=" * 70)
print("DATA CLEANING COMPLETE")
print("=" * 70)