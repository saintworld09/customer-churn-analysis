from pathlib import Path

import pandas as pd


# =========================================================
# CUSTOMER CHURN DATASET - CUSTOMER SEGMENT ANALYSIS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_FILE = (
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

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# 1. LOAD PROCESSED DATA
# =========================================================

df = pd.read_csv(PROCESSED_FILE)

print("=" * 70)
print("CUSTOMER CHURN - CUSTOMER SEGMENT ANALYSIS")
print("=" * 70)

print(f"\nDataset shape: {df.shape}")


# =========================================================
# 2. OVERALL CHURN RATE
# =========================================================

overall_churn_rate = (
    df["Churn_Flag"].mean() * 100
)

print("\n" + "-" * 70)
print("OVERALL BENCHMARK")
print("-" * 70)

print(
    f"Overall churn rate: "
    f"{overall_churn_rate:.2f}%"
)


# =========================================================
# 3. DEFINE SEGMENT DIMENSIONS
# =========================================================

segment_columns = [
    "Contract",
    "Tenure_Band",
    "InternetService",
    "PaymentMethod"
]

minimum_segment_size = 100


# =========================================================
# 4. CREATE CUSTOMER SEGMENTS
# =========================================================

segment_analysis = (
    df.groupby(segment_columns)
    .agg(
        customers=("customerID", "count"),
        churned_customers=("Churn_Flag", "sum"),
        churn_rate=("Churn_Flag", "mean")
    )
    .reset_index()
)


# Convert churn rate to percentage
segment_analysis["churn_rate"] = (
    segment_analysis["churn_rate"] * 100
)


# =========================================================
# 5. FILTER SMALL SEGMENTS
# =========================================================

segment_analysis = segment_analysis[
    segment_analysis["customers"] >= minimum_segment_size
].copy()


# =========================================================
# 6. CALCULATE DIFFERENCE FROM OVERALL CHURN
# =========================================================

segment_analysis["difference_vs_overall_pp"] = (
    segment_analysis["churn_rate"]
    - overall_churn_rate
)


# =========================================================
# 7. ROUND ANALYTICAL VALUES
# =========================================================

segment_analysis["churn_rate"] = (
    segment_analysis["churn_rate"].round(2)
)

segment_analysis["difference_vs_overall_pp"] = (
    segment_analysis["difference_vs_overall_pp"].round(2)
)


# =========================================================
# 8. SORT BY CHURN RATE
# =========================================================

segment_analysis = segment_analysis.sort_values(
    by="churn_rate",
    ascending=False
)


# =========================================================
# 9. DISPLAY TOP SEGMENTS
# =========================================================

print("\n" + "-" * 70)
print("HIGHEST-CHURN OBSERVED SEGMENTS")
print("-" * 70)

print(
    segment_analysis.head(15).to_string(
        index=False
    )
)


# =========================================================
# 10. DISPLAY LOWEST-CHURN OBSERVED SEGMENTS
# =========================================================

print("\n" + "-" * 70)
print("LOWEST-CHURN OBSERVED SEGMENTS")
print("-" * 70)

print(
    segment_analysis.tail(10).sort_values(
        by="churn_rate"
    ).to_string(
        index=False
    )
)


# =========================================================
# 11. IDENTIFY SEGMENTS ABOVE THE OVERALL RATE
# =========================================================

high_churn_segments = segment_analysis[
    segment_analysis["churn_rate"] > overall_churn_rate
].copy()


high_churn_segments = high_churn_segments.sort_values(
    by="churn_rate",
    ascending=False
)


print("\n" + "-" * 70)
print("SEGMENTS ABOVE OVERALL CHURN RATE")
print("-" * 70)

print(
    f"Segments above overall rate: "
    f"{len(high_churn_segments):,}"
)


# =========================================================
# 12. SAVE FULL SEGMENT ANALYSIS
# =========================================================

segment_analysis.to_csv(
    OUTPUT_DIR / "customer_segment_churn_analysis.csv",
    index=False
)


# =========================================================
# 13. SAVE HIGH-CHURN SEGMENTS
# =========================================================

high_churn_segments.to_csv(
    OUTPUT_DIR / "high_churn_customer_segments.csv",
    index=False
)


# =========================================================
# 14. FINAL OUTPUT
# =========================================================

print("\n" + "-" * 70)
print("OUTPUTS")
print("-" * 70)

print(
    "Saved:"
)

print(
    "- customer_segment_churn_analysis.csv"
)

print(
    "- high_churn_customer_segments.csv"
)

print("\n" + "=" * 70)
print("CUSTOMER SEGMENT ANALYSIS COMPLETE")
print("=" * 70)