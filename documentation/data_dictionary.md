# Data Dictionary

## Dataset Overview

**Dataset Name:** Telco Customer Churn

**Source:** IBM Telco Customer Churn sample dataset

**File:** `Telco-Customer-Churn.csv`

**Initial Records:** 7,043 customers

**Fields:** 21

**Purpose:** Analyze customer characteristics, services, billing behavior, contract information, and churn patterns.

---

## Data Dictionary

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
| InternetService | String | Categorical | Type of internet service used by the customer: DSL, Fiber optic, or No internet service. |
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
| TotalCharges | Decimal | Numerical | Total amount charged to the customer over the recorded customer relationship. |
| Churn | String | Target Variable | Indicates whether the customer left the company. `Yes = Churned`, `No = Retained`. |

---

## Categorical Values

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

---

## Numerical Fields

### tenure

Range:

- Minimum: 0 months
- Maximum: 72 months

### MonthlyCharges

Range:

- Minimum: 18.25
- Maximum: 118.75

### TotalCharges

The raw dataset stores this field as text because 11 records contain blank values.

Further transformation is required before numerical analysis.

---

## Data Quality Notes

- No duplicate rows were identified.
- No duplicate customer IDs were identified.
- 11 customers have blank `TotalCharges`.
- All 11 customers with blank `TotalCharges` have a tenure of 0 months.
- Several service-related fields contain `No internet service` or `No phone service`. These are meaningful business categories and should not automatically be treated as missing values.
- `SeniorCitizen` is stored numerically but should be treated analytically as a binary categorical field.
- `Churn` is the primary target variable for the churn analysis and predictive modeling stages.