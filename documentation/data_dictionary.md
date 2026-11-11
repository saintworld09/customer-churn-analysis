
# Data Dictionary

## 1. Dataset Overview

**Dataset Name:** Telco Customer Churn

**Source:** IBM Telco Customer Churn sample dataset

**Raw File:** `data/raw/Telco-Customer-Churn.csv`

**Cleaned File:** `data/processed/customer_churn_clean.csv`

**Initial Records:** 7,043 customers

**Original Fields:** 21

**Cleaned Fields:** 26

**Purpose:** Analyze customer characteristics, services, billing behavior, contract information, and churn patterns to identify customer churn patterns and support data-driven retention decisions.

---

## 2. Original Dataset Fields

The following table describes the 21 fields provided in the original IBM Telco Customer Churn dataset.

| Column | Data Type | Analytical Type | Description |
|---|---|---|---|
| customerID | String | Identifier | Unique identifier assigned to each customer. |
| gender | String | Categorical | Customer gender. |
| SeniorCitizen | Integer | Binary Categorical | Indicates whether the customer is classified as a senior citizen. `0 = No`, `1 = Yes`. |
| Partner | String | Binary Categorical | Indicates whether the customer has a partner. |
| Dependents | String | Binary Categorical | Indicates whether the customer has dependents. |
| tenure | Integer | Numerical | Number of months the customer has remained with the company. |
| PhoneService | String | Binary Categorical | Indicates whether the customer has phone service. |
| MultipleLines | String | Categorical | Indicates whether the customer has multiple phone lines. Includes `No phone service` where applicable. |
| InternetService | String | Categorical | Type of internet service used by the customer: DSL, Fiber optic, or No. |
| OnlineSecurity | String | Categorical | Indicates whether the customer has online security, no online security, or no internet service. |
| OnlineBackup | String | Categorical | Indicates whether the customer has online backup, no online backup, or no internet service. |
| DeviceProtection | String | Categorical | Indicates whether the customer has device protection, no device protection, or no internet service. |
| TechSupport | String | Categorical | Indicates whether the customer has technical support, no technical support, or no internet service. |
| StreamingTV | String | Categorical | Indicates whether the customer subscribes to streaming TV, does not subscribe, or has no internet service. |
| StreamingMovies | String | Categorical | Indicates whether the customer subscribes to streaming movies, does not subscribe, or has no internet service. |
| Contract | String | Categorical | Type of customer contract: month-to-month, one year, or two year. |
| PaperlessBilling | String | Binary Categorical | Indicates whether the customer uses paperless billing. |
| PaymentMethod | String | Categorical | Payment method used by the customer. |
| MonthlyCharges | Decimal | Numerical | Customer's current monthly service charges. |
| TotalCharges | String | Numerical (Raw) | Total amount charged to the customer over the recorded customer relationship. Stored as text in the raw dataset because of blank values. |
| Churn | String | Target Variable | Indicates whether the customer left the company. `Yes = Churned`, `No = Retained`. |

---

## 3. Derived Fields in the Cleaned Dataset

Five additional fields were created during Python data cleaning and transformation. These fields support data validation, segmentation, numerical analysis, and predictive modeling.

| Column | Data Type | Analytical Type | Description |
|---|---|---|---|
| TotalCharges_Clean | Float | Numerical | Numeric version of `TotalCharges`, created using numeric conversion. Blank or invalid values are retained as missing values rather than replaced with zero. |
| TotalCharges_Status | String | Data Quality Indicator | Identifies whether a customer's total charges were recorded. Values: `Recorded` and `Not Recorded`. |
| Tenure_Band | String | Categorical / Segmentation | Groups customers into five tenure categories: `0–6 Months`, `7–12 Months`, `13–24 Months`, `25–48 Months`, and `49–72 Months`. |
| SeniorCitizen_Status | String | Categorical | Converts the original `SeniorCitizen` indicator into readable categories: `Senior Citizen` and `Non-Senior Citizen`. |
| Churn_Flag | Integer | Binary Target Variable | Converts the original churn outcome into a numerical indicator: `1 = Churned`, `0 = Retained`. |

### Purpose of the Derived Fields

- **TotalCharges_Clean:** Makes total charges suitable for numerical calculations and statistical analysis.
- **TotalCharges_Status:** Makes it possible to distinguish customers with recorded charges from those with missing charge values.
- **Tenure_Band:** Supports customer segmentation and churn comparisons across different customer relationship durations.
- **SeniorCitizen_Status:** Improves readability in reports and visualizations.
- **Churn_Flag:** Provides a numerical target variable for statistical analysis and machine learning models.

---

## 4. Categorical Values

This section documents the expected categorical values in the original dataset and the additional categories introduced during cleaning.

### Gender

- Female
- Male

### SeniorCitizen

- 0 = No
- 1 = Yes

### Partner

- Yes
- No

### Dependents

- Yes
- No

### PhoneService

- Yes
- No

### MultipleLines

- Yes
- No
- No phone service

### InternetService

- DSL
- Fiber optic
- No

### OnlineSecurity

- Yes
- No
- No internet service

### OnlineBackup

- Yes
- No
- No internet service

### DeviceProtection

- Yes
- No
- No internet service

### TechSupport

- Yes
- No
- No internet service

### StreamingTV

- Yes
- No
- No internet service

### StreamingMovies

- Yes
- No
- No internet service

### Contract

- Month-to-month
- One year
- Two year

### PaperlessBilling

- Yes
- No

### PaymentMethod

- Electronic check
- Mailed check
- Bank transfer (automatic)
- Credit card (automatic)

### Churn

- Yes
- No

### TotalCharges_Status

- Recorded
- Not Recorded

### Tenure_Band

- 0–6 Months
- 7–12 Months
- 13–24 Months
- 25–48 Months
- 49–72 Months

### SeniorCitizen_Status

- Senior Citizen
- Non-Senior Citizen

---

## 5. Numerical Fields

### tenure

**Description:** Number of months a customer has remained with the company.

- Minimum: 0 months
- Maximum: 72 months

### MonthlyCharges

**Description:** Current monthly service charges for each customer.

- Minimum: 18.25
- Maximum: 118.75

### TotalCharges

**Description:** Total amount charged to a customer over the recorded customer relationship.

The raw dataset stores this field as text because 11 records contain blank values. It is preserved in its original form during cleaning.

### TotalCharges_Clean

**Description:** Numeric version of the original `TotalCharges` field.

The cleaning process converts the field to a numeric data type. Blank values become missing numeric values (`NaN`), not zero.

- Recorded values: 7,032
- Missing values: 11

---

## 6. Data Quality Notes

- The original dataset contains 7,043 customer records and 21 fields.
- The cleaned dataset contains 7,043 customer records and 26 fields.
- No duplicate rows were identified in the cleaned dataset.
- No duplicate customer IDs were identified.
- Eleven customers have blank `TotalCharges` values.
- All 11 customers with blank `TotalCharges` have a tenure of 0 months.
- The original `TotalCharges` field is preserved, while `TotalCharges_Clean` provides its numeric counterpart.
- Missing total charge values are not replaced with zero because doing so could introduce misleading financial information.
- Several service-related fields contain `No internet service` or `No phone service`. These are meaningful business categories and should not automatically be treated as missing values.
- `SeniorCitizen` is stored numerically but should be treated analytically as a binary categorical field.
- `Churn` is the original target variable, while `Churn_Flag` is its numerical representation.
- The cleaned dataset was validated to confirm the expected record count, column count, uniqueness of customer IDs, missing total charge count, and churn flag distribution.

---

## 7. Dataset Usage

The dataset supports several stages of the Customer Churn Analytics project:

| Analytical Stage | Relevant Fields |
|---|---|
| Customer profiling | gender, SeniorCitizen_Status, Partner, Dependents |
| Customer lifecycle analysis | tenure, Tenure_Band |
| Service analysis | PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies |
| Contract analysis | Contract |
| Billing analysis | MonthlyCharges, TotalCharges_Clean, TotalCharges_Status |
| Payment analysis | PaymentMethod, PaperlessBilling |
| Churn analysis | Churn, Churn_Flag |
| Predictive modeling | Churn_Flag and selected customer/service features |

---

## 8. Conclusion

The data dictionary documents both the original IBM Telco Customer Churn dataset and the additional fields introduced during data preparation.

It provides a consistent reference for understanding field definitions, analytical types, categorical values, data quality considerations, and the role of each field across the Excel, SQL, Python, and Power BI stages of the project.
