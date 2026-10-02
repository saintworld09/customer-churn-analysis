from pathlib import Path

import pandas as pd


# =========================================================
# CUSTOMER CHURN DATASET - SEGMENT ANALYSIS VALIDATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "analysis_outputs"
)

SEGMENT_FILE = (
    OUTPUT_DIR
    / "customer_segment_churn_analysis.csv"
)

HIGH_CHURN_FILE = (
    OUTPUT_DIR
    / "high_churn_customer_segments.csv"
)


# =========================================================
# 1. LOAD ANALYTICAL OUTPUTS
# =========================================================

segment_df = pd.read_csv(SEGMENT_FILE)

high_churn_df = pd.read_csv(HIGH_CHURN_FILE)


print("=" * 70)
print("CUSTOMER CHURN - SEGMENT ANALYSIS VALIDATION")
print("=" * 70)


# =========================================================
# 2. BASIC FILE VALIDATION
# =========================================================

print("\n" + "-" * 70)
print("FILE VALIDATION")
print("-" * 70)

print(
    f"Full segment analysis rows: "
    f"{len(segment_df):,}"
)

print(
    f"High-churn segment rows: "
    f"{len(high_churn_df):,}"
)


# =========================================================
# 3. REQUIRED COLUMNS
# =========================================================

required_columns = [
    "Contract",
    "Tenure_Band",
    "InternetService",
    "PaymentMethod",
    "customers",
    "churned_customers",
    "churn_rate",
    "difference_vs_overall_pp"
]


missing_columns = [
    column
    for column in required_columns
    if column not in segment_df.columns
]


print("\n" + "-" * 70)
print("COLUMN VALIDATION")
print("-" * 70)

print(
    f"Missing required columns: "
    f"{len(missing_columns)}"
)

if missing_columns:
    print("Missing columns:")
    for column in missing_columns:
        print(f"- {column}")


# =========================================================
# 4. CUSTOMER COUNT VALIDATION
# =========================================================

print("\n" + "-" * 70)
print("CUSTOMER COUNT VALIDATION")
print("-" * 70)

invalid_customer_counts = (
    segment_df["customers"] <= 0
).sum()

invalid_churn_counts = (
    segment_df["churned_customers"] < 0
).sum()

churn_exceeds_customers = (
    segment_df["churned_customers"]
    > segment_df["customers"]
).sum()


print(
    f"Segments with invalid customer counts: "
    f"{invalid_customer_counts}"
)

print(
    f"Segments with invalid churn counts: "
    f"{invalid_churn_counts}"
)

print(
    f"Segments where churned > customers: "
    f"{churn_exceeds_customers}"
)


# =========================================================
# 5. CHURN RATE VALIDATION
# =========================================================

print("\n" + "-" * 70)
print("CHURN RATE VALIDATION")
print("-" * 70)

invalid_churn_rates = (
    (segment_df["churn_rate"] < 0)
    |
    (segment_df["churn_rate"] > 100)
).sum()


print(
    f"Invalid churn rates: "
    f"{invalid_churn_rates}"
)


# =========================================================
# 6. MINIMUM SEGMENT SIZE VALIDATION
# =========================================================

minimum_segment_size = 100

small_segments = (
    segment_df["customers"]
    < minimum_segment_size
).sum()


print("\n" + "-" * 70)
print("MINIMUM SEGMENT SIZE VALIDATION")
print("-" * 70)

print(
    f"Minimum required segment size: "
    f"{minimum_segment_size}"
)

print(
    f"Segments below minimum size: "
    f"{small_segments}"
)


# =========================================================
# 7. HIGH-CHURN OUTPUT VALIDATION
# =========================================================

high_churn_with_low_rate = (
    high_churn_df["difference_vs_overall_pp"]
    <= 0
).sum()


print("\n" + "-" * 70)
print("HIGH-CHURN SEGMENT VALIDATION")
print("-" * 70)

print(
    f"High-churn segments: "
    f"{len(high_churn_df):,}"
)

print(
    f"High-churn output rows at or below "
    f"overall churn: "
    f"{high_churn_with_low_rate}"
)


# =========================================================
# 8. FINAL VALIDATION
# =========================================================

validation_passed = (
    len(segment_df) > 0
    and len(high_churn_df) > 0
    and len(missing_columns) == 0
    and invalid_customer_counts == 0
    and invalid_churn_counts == 0
    and churn_exceeds_customers == 0
    and invalid_churn_rates == 0
    and small_segments == 0
    and high_churn_with_low_rate == 0
)


print("\n" + "=" * 70)

if validation_passed:
    print("VALIDATION PASSED")
    print(
        "Segment analysis outputs are internally consistent."
    )
else:
    print("VALIDATION FAILED")
    print(
        "Review the validation results above."
    )

print("=" * 70)