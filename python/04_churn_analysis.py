from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# =========================================================
# CUSTOMER CHURN ANALYSIS - PYTHON
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
print("CUSTOMER CHURN ANALYSIS")
print("=" * 70)

print(f"\nDataset shape: {df.shape}")


# =========================================================
# 2. OVERALL CHURN PROFILE
# =========================================================

total_customers = len(df)

churned_customers = (
    df["Churn_Flag"] == 1
).sum()

active_customers = (
    df["Churn_Flag"] == 0
).sum()

churn_rate = (
    df["Churn_Flag"].mean() * 100
)


print("\n" + "-" * 70)
print("OVERALL CHURN PROFILE")
print("-" * 70)

print(f"Total customers: {total_customers:,}")
print(f"Churned customers: {churned_customers:,}")
print(f"Active customers: {active_customers:,}")
print(f"Churn rate: {churn_rate:.2f}%")


# =========================================================
# 3. CHURN BY CONTRACT
# =========================================================

contract_analysis = (
    df.groupby("Contract")
    .agg(
        customers=("customerID", "count"),
        churned_customers=("Churn_Flag", "sum"),
        churn_rate=("Churn_Flag", "mean")
    )
    .reset_index()
)

contract_analysis["churn_rate"] = (
    contract_analysis["churn_rate"] * 100
)

contract_analysis = contract_analysis.sort_values(
    "churn_rate",
    ascending=False
)


print("\n" + "-" * 70)
print("CHURN BY CONTRACT")
print("-" * 70)

print(
    contract_analysis.to_string(index=False)
)


# =========================================================
# 4. CHURN BY TENURE BAND
# =========================================================

tenure_order = [
    "0–6 Months",
    "7–12 Months",
    "13–24 Months",
    "25–48 Months",
    "49–72 Months"
]

tenure_analysis = (
    df.groupby("Tenure_Band")
    .agg(
        customers=("customerID", "count"),
        churned_customers=("Churn_Flag", "sum"),
        churn_rate=("Churn_Flag", "mean")
    )
    .reindex(tenure_order)
    .reset_index()
)

tenure_analysis["churn_rate"] = (
    tenure_analysis["churn_rate"] * 100
)


print("\n" + "-" * 70)
print("CHURN BY TENURE BAND")
print("-" * 70)

print(
    tenure_analysis.to_string(index=False)
)


# =========================================================
# 5. MONTHLY CHARGES BY CHURN STATUS
# =========================================================

monthly_charges_analysis = (
    df.groupby("Churn")
    .agg(
        customers=("customerID", "count"),
        average_monthly_charges=("MonthlyCharges", "mean"),
        minimum_monthly_charges=("MonthlyCharges", "min"),
        maximum_monthly_charges=("MonthlyCharges", "max")
    )
    .reset_index()
)

monthly_charges_analysis[
    "average_monthly_charges"
] = monthly_charges_analysis[
    "average_monthly_charges"
].round(2)

monthly_charges_analysis[
    "minimum_monthly_charges"
] = monthly_charges_analysis[
    "minimum_monthly_charges"
].round(2)

monthly_charges_analysis[
    "maximum_monthly_charges"
] = monthly_charges_analysis[
    "maximum_monthly_charges"
].round(2)


print("\n" + "-" * 70)
print("MONTHLY CHARGES BY CHURN STATUS")
print("-" * 70)

print(
    monthly_charges_analysis.to_string(index=False)
)


# =========================================================
# 6. CREATE OUTPUT DIRECTORY
# =========================================================

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
# 7. SAVE ANALYTICAL OUTPUTS
# =========================================================

contract_analysis.to_csv(
    OUTPUT_DIR / "churn_by_contract.csv",
    index=False
)

tenure_analysis.to_csv(
    OUTPUT_DIR / "churn_by_tenure.csv",
    index=False
)

monthly_charges_analysis.to_csv(
    OUTPUT_DIR / "monthly_charges_by_churn.csv",
    index=False
)


# =========================================================
# 8. VISUALIZATION - CHURN BY CONTRACT
# =========================================================

plt.figure(figsize=(9, 6))

plt.bar(
    contract_analysis["Contract"],
    contract_analysis["churn_rate"]
)

plt.title("Churn Rate by Contract Type")

plt.xlabel("Contract Type")

plt.ylabel("Churn Rate (%)")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "churn_rate_by_contract.png",
    dpi=300
)

plt.close()


# =========================================================
# 9. VISUALIZATION - CHURN BY TENURE
# =========================================================

plt.figure(figsize=(9, 6))

plt.bar(
    tenure_analysis["Tenure_Band"],
    tenure_analysis["churn_rate"]
)

plt.title("Churn Rate by Tenure Band")

plt.xlabel("Tenure Band")

plt.ylabel("Churn Rate (%)")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "churn_rate_by_tenure.png",
    dpi=300
)

plt.close()


# =========================================================
# 10. VISUALIZATION - MONTHLY CHARGES
# =========================================================

plt.figure(figsize=(8, 6))

plt.bar(
    monthly_charges_analysis["Churn"],
    monthly_charges_analysis[
        "average_monthly_charges"
    ]
)

plt.title("Average Monthly Charges by Churn Status")

plt.xlabel("Churn Status")

plt.ylabel("Average Monthly Charges")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "average_monthly_charges_by_churn.png",
    dpi=300
)

plt.close()


# =========================================================
# 11. FINAL MESSAGE
# =========================================================

print("\n" + "-" * 70)
print("OUTPUTS")
print("-" * 70)

print(f"Analysis outputs saved to:")
print(OUTPUT_DIR)

print("\nGenerated files:")
print("- churn_by_contract.csv")
print("- churn_by_tenure.csv")
print("- monthly_charges_by_churn.csv")
print("- churn_rate_by_contract.png")
print("- churn_rate_by_tenure.png")
print("- average_monthly_charges_by_churn.png")

print("\n" + "=" * 70)
print("PYTHON CHURN ANALYSIS COMPLETE")
print("=" * 70)