# Data Quality Assessment

## 1. Objective

The purpose of this assessment is to evaluate the quality, completeness, consistency, and structure of the customer churn dataset before and after data preparation.

The assessment identifies potential data-quality issues, documents the decisions made during cleaning, and verifies that the processed dataset is suitable for downstream analysis using SQL, Python, and Power BI.

The original dataset is preserved unchanged in:

`data/raw/Telco-Customer-Churn.csv`

The processed dataset is stored in:

`data/processed/customer_churn_clean.csv`

---

## 2. Raw Dataset Profile

The project uses the IBM Telco Customer Churn sample dataset.

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

**Initial assessment:** The raw dataset has a consistent record structure and contains no identified duplicate records or customer IDs. However, further inspection revealed 11 blank values in `TotalCharges` that required special treatment.

---

## 3. Raw Data Quality Findings

### 3.1 Duplicate Records

The raw dataset was checked for duplicate rows and duplicate customer identifiers.

Findings:

- No duplicate rows were identified.
- No duplicate `customerID` values were identified.

**Assessment:** No duplication issue was identified in the source dataset.

### 3.2 Missing and Blank Values

The initial pandas missing-value check did not identify standard null values in the raw dataset.

However, a closer inspection identified 11 blank string values in the `TotalCharges` column.

All 11 affected customers had:

```text
tenure = 0
```

This indicates that the affected customers had zero months of recorded tenure and no recorded total charges in the source data.

**Treatment decision:**

- The original `TotalCharges` column was preserved.
- A separate numeric column, `TotalCharges_Clean`, was created.
- Blank values were converted to missing numeric values (`NaN`) rather than being replaced with zero.
- A `TotalCharges_Status` column was added to distinguish recorded from unrecorded charges.

This approach preserves the original information and avoids introducing unsupported financial values.

### 3.3 Text and Category Consistency

Text fields were inspected and leading or trailing whitespace was removed from string columns during cleaning.

The following category values were retained because they represent meaningful service conditions:

- `No internet service`
- `No phone service`

These values were not treated as missing data.

The `SeniorCitizen` field was also treated as a categorical indicator rather than as a continuous numerical measure.

**Assessment:** Text standardization was applied while preserving meaningful category distinctions.

### 3.4 Customer Churn Distribution

The raw dataset contains:

| Customer Status | Customers | Percentage |
|---|---:|---:|
| Churned (`Yes`) | 1,869 | 26.54% |
| Retained (`No`) | 5,174 | 73.46% |
| **Total** | **7,043** | **100.00%** |

The churn rate was calculated as:

`Churned Customers / Total Customers × 100`

The resulting churn rate is **26.54%**.

**Assessment:** The dataset contains both churned and retained customers, making it suitable for examining customer retention patterns and churn-related characteristics. The unequal class distribution should nevertheless be considered when building and evaluating predictive models.

---

## 4. Data Cleaning and Transformation Decisions

The cleaning process was implemented in:

`python/02_data_cleaning.py`

The following transformations were applied:

| Transformation | Implementation | Purpose |
|---|---|---|
| Text standardization | Removed leading and trailing whitespace from string columns | Improve consistency |
| Numeric charge conversion | Created `TotalCharges_Clean` from `TotalCharges` | Enable numerical analysis |
| Missing charge identification | Created `TotalCharges_Status` | Distinguish recorded and unrecorded charges |
| Tenure grouping | Created `Tenure_Band` | Support customer lifecycle segmentation |
| Senior citizen classification | Created `SeniorCitizen_Status` | Improve categorical interpretation |
| Churn encoding | Created `Churn_Flag` | Support numerical and statistical analysis |

### 4.1 Total Charges Treatment

The original `TotalCharges` field was retained.

The additional fields are:

- `TotalCharges_Clean`: Numeric representation of the original total charges, with unrecorded values remaining missing.
- `TotalCharges_Status`: Indicates whether the original total charge was recorded.

The status categories are:

| Status | Meaning | Customers |
|---|---|---:|
| Recorded | A total charge value was available | 7,032 |
| Not Recorded | The original total charge was blank | 11 |

No missing charge was automatically assumed to be zero.

### 4.2 Tenure Band Classification

The continuous `tenure` field was grouped into five customer lifecycle categories.

| Tenure Band | Customers |
|---|---:|
| 0–6 Months | 1,481 |
| 7–12 Months | 705 |
| 13–24 Months | 1,024 |
| 25–48 Months | 1,594 |
| 49–72 Months | 2,239 |
| **Total** | **7,043** |

This transformation supports customer segmentation and makes it easier to compare churn patterns across different stages of the customer relationship.

### 4.3 Senior Citizen Classification

The original binary `SeniorCitizen` field was converted into a more readable categorical field.

| Category | Customers |
|---|---:|
| Non-Senior Citizen | 5,901 |
| Senior Citizen | 1,142 |
| **Total** | **7,043** |

### 4.4 Churn Encoding

The original `Churn` field was retained, and a numerical representation was created.

| Churn Status | Churn_Flag |
|---|---:|
| No | 0 |
| Yes | 1 |

This allows churn status to be used more conveniently in numerical analysis, aggregation, and predictive modelling.

---

## 5. Processed Dataset Validation

After cleaning, the processed dataset was validated using:

`python/03_validate_clean_data.py`

The validation was executed using the project's virtual environment:

```powershell
.\.venv\Scripts\python.exe .\python\03_validate_clean_data.py
```

### 5.1 Dataset Structure

| Validation Check | Expected / Observed Result |
|---|---:|
| Rows | 7,043 |
| Columns | 26 |
| Duplicate rows | 0 |
| Duplicate customer IDs | 0 |

The processed dataset contains the original 21 fields and five additional analytical fields.

### 5.2 Total Charges Validation

| Validation Check | Result |
|---|---:|
| Recorded charges | 7,032 |
| Unrecorded charges | 11 |
| Missing values in `TotalCharges_Clean` | 11 |
| Zero-tenure customers | 11 |
| Zero-tenure customers with unrecorded charges | 11 |

The results confirm that the missing charge values were retained as missing numeric values and correctly identified through the status field.

### 5.3 Derived Category Validation

The validation script confirmed the following distributions:

**Tenure bands**

| Category | Customers |
|---|---:|
| 0–6 Months | 1,481 |
| 7–12 Months | 705 |
| 13–24 Months | 1,024 |
| 25–48 Months | 1,594 |
| 49–72 Months | 2,239 |

**Senior citizen status**

| Category | Customers |
|---|---:|
| Non-Senior Citizen | 5,901 |
| Senior Citizen | 1,142 |

### 5.4 Churn Validation

| Validation Check | Result |
|---|---:|
| Churned customers | 1,869 |
| Retained customers | 5,174 |
| Invalid `Churn_Flag` values | 0 |
| Churn rate | 26.54% |

The churn counts and encoded values were consistent with the source dataset.

### 5.5 Validation Outcome

**Validation Status: PASSED**

The validation script completed successfully and confirmed:

- The expected 7,043 records and 26 columns.
- No duplicate rows or customer IDs.
- Exactly 11 missing numeric total-charge values.
- The expected churn counts.
- No invalid churn flag values.

The processed dataset is ready for downstream analytical work.

---

## 6. Data Quality Considerations and Limitations

Although the dataset passed the implemented validation checks, the following considerations remain important when interpreting the analysis.

### 6.1 Unrecorded Total Charges

The 11 blank total-charge values were not replaced with zero. They remain missing in `TotalCharges_Clean`.

Analyses involving total charges should account for these missing values and avoid treating them as actual zero charges.

### 6.2 Unequal Churn Distribution

Approximately 26.54% of customers churned, compared with 73.46% who remained.

This imbalance should be considered when evaluating classification models. Accuracy alone may not provide a complete picture of model performance; recall, precision, F1-score, and confusion matrices are also useful.

### 6.3 Sample Dataset Limitations

The project uses a sample telecommunications customer dataset. Its findings describe patterns within the available dataset and should not automatically be generalized to every telecommunications company or customer population.

### 6.4 Observational Data

The dataset contains customer characteristics, service subscriptions, billing information, and churn outcomes.

Associations between customer attributes and churn do not, by themselves, establish that those attributes caused customers to leave.

Business recommendations should therefore be treated as evidence-informed opportunities for further investigation and testing.

### 6.5 Scope of Validation

The validation script checks dataset structure, duplicates, total-charge missingness, derived category distributions, churn counts, and invalid churn flags.

Passing these checks does not guarantee that every field is free from all possible business-rule, measurement, or source-data issues.

---

## 7. Reproducibility

Run the following commands from the project root using the project's virtual environment.

**Step 1: Run data cleaning**

```powershell
.\.venv\Scripts\python.exe .\python\02_data_cleaning.py
```

**Step 2: Validate the processed dataset**

```powershell
.\.venv\Scripts\python.exe .\python\03_validate_clean_data.py
```

The validation script should report:

```text
VALIDATION PASSED
The processed dataset is ready for downstream analysis.
```

---

## 8. Conclusion

The raw customer churn dataset was inspected for duplication, missing values, category consistency, and basic numerical characteristics.

The cleaning process preserved the original source data, addressed the 11 blank total-charge values without assuming they were zero, and introduced five additional fields to support analytical work.

The resulting processed dataset contains 7,043 records and 26 columns. It successfully passed the implemented validation checks and provides a consistent foundation for the project's subsequent SQL analysis, Python exploration, statistical analysis, predictive modelling, and Power BI reporting.
'@ | Set-Content -Path .\documentation\data_quality_assessment.md -Encoding UTF8




