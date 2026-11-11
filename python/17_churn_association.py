"""
=========================================================
Customer Churn Analytics
17 - Strength of Association with Churn
=========================================================

Purpose:
    Measure the strength of association between customer
    attributes/services and churn using Cramér's V.

Method:
    Cramér's V is appropriate for measuring the association
    between categorical variables.

Output:
    data/processed/churn_association.csv

Interpretation:
    0.00 = No association
    1.00 = Perfect association

The resulting dataset will be used in Power BI to create
the "Strength of Association with Churn" visual.
=========================================================
"""

from pathlib import Path

import pandas as pd
from scipy.stats import chi2_contingency


# =========================================================
# 1. PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Telco-Customer-Churn.csv"
)

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = PROCESSED_DIR / "churn_association.csv"


# =========================================================
# 2. LOAD RAW DATA
# =========================================================

print("=" * 60)
print("CUSTOMER CHURN - STRENGTH OF ASSOCIATION ANALYSIS")
print("=" * 60)

print("\nLoading raw customer churn data...")

df = pd.read_csv(RAW_FILE)

print(f"Rows loaded: {len(df):,}")
print(f"Columns loaded: {len(df.columns):,}")


# =========================================================
# 3. CLEAN COLUMN NAMES
# =========================================================

df.columns = df.columns.str.strip()


# =========================================================
# 4. CLEAN TOTALCHARGES
# =========================================================

"""
TotalCharges contains some blank values in the original
Telco Customer Churn dataset.

Although TotalCharges is not directly used in the Cramér's V
analysis below, we clean it here so the dataframe remains
consistent with the project's broader data-cleaning workflow.
"""

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)


# =========================================================
# 5. CREATE TENURE BAND
# =========================================================

"""
Business-friendly tenure categories.

These match the tenure bands used in the Power BI project:

0–6
7–12
13–24
25–48
49–72
"""

df["Tenure_Band"] = pd.cut(
    df["tenure"],
    bins=[-1, 6, 12, 24, 48, 72],
    labels=[
        "0–6",
        "7–12",
        "13–24",
        "25–48",
        "49–72"
    ],
    include_lowest=True
)


# =========================================================
# 6. CREATE SENIOR CITIZEN STATUS
# =========================================================

"""
Convert the numeric SeniorCitizen field into a
business-friendly categorical field.
"""

df["SeniorCitizen_Status"] = df["SeniorCitizen"].map({
    0: "Non-Senior Citizen",
    1: "Senior Citizen"
})


# =========================================================
# 7. DEFINE CHURN DRIVER VARIABLES
# =========================================================

"""
These are the business-relevant categorical variables that
will be evaluated against Churn.

We intentionally exclude:

- customerID
- tenure (raw numeric version)
- MonthlyCharges
- TotalCharges

because they are identifiers or continuous/numeric variables
and are not appropriate for this particular Cramér's V chart.
"""

drivers = [
    "Contract",
    "Tenure_Band",
    "InternetService",
    "TechSupport",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "PaymentMethod",
    "SeniorCitizen_Status",
    "Partner",
    "Dependents"
]


# =========================================================
# 8. VALIDATE REQUIRED COLUMNS
# =========================================================

missing_columns = [
    column
    for column in drivers + ["Churn"]
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        "The following required columns are missing from "
        f"the dataset: {missing_columns}"
    )


# =========================================================
# 9. DEFINE CRAMÉR'S V FUNCTION
# =========================================================

def cramers_v(x, y):
    """
    Calculate bias-corrected Cramér's V.

    Parameters
    ----------
    x : pandas.Series
        First categorical variable.

    y : pandas.Series
        Second categorical variable.

    Returns
    -------
    float
        Bias-corrected Cramér's V value.
    """

    # Remove missing observations
    data = pd.DataFrame({
        "x": x,
        "y": y
    }).dropna()

    # Create contingency table
    confusion_matrix = pd.crosstab(
        data["x"],
        data["y"]
    )

    # Chi-square statistic
    chi2 = chi2_contingency(
        confusion_matrix,
        correction=False
    )[0]

    # Total number of observations
    n = confusion_matrix.sum().sum()

    # Number of rows and columns
    r, k = confusion_matrix.shape

    # Phi-squared
    phi2 = chi2 / n

    # Bias correction
    phi2corr = max(
        0,
        phi2 - (
            (k - 1) * (r - 1)
        ) / (n - 1)
    )

    rcorr = (
        r
        - ((r - 1) ** 2) / (n - 1)
    )

    kcorr = (
        k
        - ((k - 1) ** 2) / (n - 1)
    )

    denominator = min(
        kcorr - 1,
        rcorr - 1
    )

    # Protect against division by zero
    if denominator <= 0:
        return 0.0

    return (phi2corr / denominator) ** 0.5


# =========================================================
# 10. CALCULATE ASSOCIATION FOR EACH DRIVER
# =========================================================

print("\nCalculating Cramér's V values...")

results = []

for driver in drivers:

    association = cramers_v(
        df[driver],
        df["Churn"]
    )

    results.append({
        "Driver": driver,
        "Cramers_V": association
    })


# =========================================================
# 11. CREATE RESULTS DATAFRAME
# =========================================================

association_df = pd.DataFrame(results)


# =========================================================
# 12. SORT BY ASSOCIATION STRENGTH
# =========================================================

association_df = association_df.sort_values(
    by="Cramers_V",
    ascending=False
).reset_index(drop=True)


# =========================================================
# 13. ROUND VALUES
# =========================================================

association_df["Cramers_V"] = association_df[
    "Cramers_V"
].round(4)


# =========================================================
# 14. CREATE INTERPRETATION BAND
# =========================================================

"""
These labels are intended as descriptive guidance rather
than strict statistical rules.

They help make the output easier to interpret in analysis.
"""

def classify_association(value):

    if value < 0.10:
        return "Very Weak"

    elif value < 0.20:
        return "Weak"

    elif value < 0.30:
        return "Moderate"

    elif value < 0.50:
        return "Strong"

    else:
        return "Very Strong"


association_df["Association_Strength"] = (
    association_df["Cramers_V"]
    .apply(classify_association)
)


# =========================================================
# 15. ADD RANK
# =========================================================

association_df.insert(
    0,
    "Rank",
    range(1, len(association_df) + 1)
)


# =========================================================
# 16. DISPLAY RESULTS
# =========================================================

print("\n")
print("=" * 60)
print("CRAMÉR'S V RESULTS")
print("=" * 60)

print(
    association_df.to_string(
        index=False
    )
)


# =========================================================
# 17. CREATE PROCESSED DIRECTORY
# =========================================================

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# 18. EXPORT RESULTS
# =========================================================

association_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# =========================================================
# 19. CONFIRM OUTPUT
# =========================================================

print("\n")
print("=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)

print(
    f"\nOutput file created:\n{OUTPUT_FILE}"
)

print(
    f"\nDrivers analyzed: {len(association_df)}"
)

print(
    "\nThe file is ready to import into Power BI."
)

print("=" * 60)