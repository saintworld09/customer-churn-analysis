# Data Quality Assessment

## Objective

The purpose of this assessment is to evaluate the quality and structure of the raw customer churn dataset before any transformation or analytical processing is performed.

The raw dataset is preserved unchanged in:

`data/raw/Telco-Customer-Churn.csv`

---

## Dataset Profile

| Check | Result |
|---|---:|
| Records | 7,043 |
| Columns | 21 |
| Duplicate rows | 0 |
| Duplicate customer IDs | 0 |
| Standard missing values detected by pandas | 0 |
| Blank `TotalCharges` values | 11 |
| Minimum tenure | 0 months |
| Maximum tenure | 72 months |
| Minimum monthly charge | 18.25 |
| Maximum monthly charge | 118.75 |
| Churned customers | 1,869 |
| Retained customers | 5,174 |
| Churn rate | 26.54% |

---

## Findings

### 1. Duplicate Records

No duplicate rows were identified.

No duplicate customer IDs were identified.

**Assessment:** No duplication issue identified.

---

### 2. Missing and Blank Values

Pandas did not identify standard null values in the raw CSV.

However, 11 blank string values were identified in `TotalCharges`.

All 11 affected customers have:

```text
tenure = 0