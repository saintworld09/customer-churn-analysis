# Customer Churn Analytics

An end-to-end data analytics project investigating customer churn in the telecommunications industry using data preparation, SQL, Python, machine learning, and Power BI.

## Project Overview

Customer churn is a major business challenge for subscription-based companies. When customers discontinue their services, businesses lose recurring revenue and may incur additional costs acquiring replacement customers.

This project analyzes the IBM Telco Customer Churn dataset to understand customer churn patterns, identify high-risk customer segments, evaluate predictive models, and develop data-driven customer retention recommendations.

The project follows an end-to-end analytics workflow, transforming raw customer records into validated insights and business intelligence reporting.

## Business Problem

A telecommunications company needs to understand why customers leave and which customer groups are more likely to churn.

Without a clear understanding of churn patterns, the company may struggle to prioritize retention efforts, allocate resources effectively, and identify customers who need additional attention.

This project investigates customer characteristics, service subscriptions, contract arrangements, payment methods, and tenure to identify patterns associated with churn.

## Project Objectives

The main objectives are to:

- Assess the quality and reliability of the customer dataset.
- Clean and prepare the data for analysis.
- Develop a structured SQL database and perform analytical queries.
- Investigate customer churn patterns using Python.
- Identify important categorical associations and high-risk customer segments.
- Build and evaluate machine learning models for churn prediction.
- Communicate findings through an interactive Power BI report.
- Translate analytical findings into practical retention recommendations.

## Dataset

The project uses the IBM Telco Customer Churn dataset.

| Dataset Attribute | Value |
|---|---|
| Original records | 7,043 |
| Original columns | 21 |
| Processed records | 7,043 |
| Processed columns | 26 |
| Customer identifier | `customerID` |
| Target variable | `Churn` |
| Analytical subject | Telecommunications customer churn |

The dataset contains information about customer demographics, account characteristics, subscribed services, contract types, billing information, tenure, and churn status.

### Data Preparation

The raw dataset was inspected, cleaned, transformed, and validated before analysis.

Five derived fields were added:

| Derived Field | Purpose |
|---|---|
| `TotalCharges_Clean` | Numeric version of total charges |
| `TotalCharges_Status` | Identifies the status of total charges data |
| `Tenure_Band` | Groups customers by tenure |
| `SeniorCitizen_Status` | Provides readable senior citizen categories |
| `Churn_Flag` | Represents churn as a numerical indicator |

The final processed dataset contains 7,043 records and 26 columns.

**Data quality highlights:**

- No duplicate customer records were identified.
- No duplicate customer identifiers were identified.
- Eleven records had missing original total charges.
- The 11 missing total charges belonged to customers with zero tenure.
- Missing total charges were retained as missing rather than automatically replaced with zero.
- The processed dataset passed the project's validation script.

## Analytical Workflow

The project follows a structured workflow covering data preparation, database analysis, statistical analysis, predictive modeling, and business intelligence.

<details>
<summary>1. Data Quality Assessment and Preparation</summary>

The initial stage involved examining the raw dataset and identifying potential quality issues.

Activities included:

- Inspecting dataset dimensions and data types.
- Checking missing values and duplicate records.
- Validating customer identifiers.
- Reviewing numerical and categorical fields.
- Cleaning total charges.
- Creating derived analytical fields.
- Grouping customers into tenure categories.
- Validating the processed dataset.

**Main output:** `data/processed/customer_churn_clean.csv`

</details>

<details>
<summary>2. SQL Database Development and Analysis</summary>

SQL was used to organize the processed data and investigate customer churn through structured analytical queries.

The database is named `customer_churn_db`.

Main database objects:

- `customer_churn` — customer churn table.
- `vw_customer_churn` — analytical view.

The SQL stage contains two schema scripts and 18 analytical queries.

Analysis includes:

- Overall churn rate.
- Churn by contract type.
- Churn by tenure.
- Churn by internet service.
- Churn by payment method.
- Churn by customer support and security services.
- Customer segment comparisons.
- High-risk customer combinations.
- Monthly and total charges by churn status.

</details>

<details>
<summary>3. Python Statistical and Predictive Analysis</summary>

Python was used for deeper investigation of customer churn patterns.

The analysis included:

- Exploratory data analysis.
- Customer segmentation.
- Statistical association analysis.
- Predictive modeling.
- Model evaluation.
- Classification threshold analysis.
- Business impact analysis.

The project also used bias-corrected Cramér's V to examine associations between categorical customer characteristics and churn.

Predictive modeling was evaluated using accuracy, precision, recall, F1-score, and ROC-AUC.

</details>

<details>
<summary>4. Power BI Business Intelligence Reporting</summary>

Power BI was used to present the analytical findings in a six-page report.

The existing report contains:

1. Executive Overview
2. Churn Drivers
3. High-Risk Segments
4. Predictive Intelligence
5. Retention Strategy
6. Insight & Recommendation

The report connects customer churn metrics, segment comparisons, predictive model results, and business recommendations.

An advanced redesign using Power BI HTML Content is planned as a future improvement. It is not represented as an already completed implementation.

</details>

## Key Findings

The analysis produced several important findings.

### 1. Overall Customer Churn

| Metric | Result |
|---|---:|
| Total customers | 7,043 |
| Churned customers | 1,869 |
| Active customers | 5,174 |
| Overall churn rate | 26.54% |

Approximately 26.54% of the customers in the dataset have churned.

### 2. Contract Type and Churn

| Contract Type | Churn Rate |
|---|---:|
| Month-to-month | 42.71% |
| One year | 11.27% |
| Two year | 2.83% |

Month-to-month customers have a substantially higher observed churn rate than customers on longer-term contracts.

### 3. Customer Tenure and Churn

| Tenure Band | Churn Rate |
|---|---:|
| 0–6 Months | 52.94% |
| 49–72 Months | 9.51% |

Early-tenure customers show considerably higher churn than customers who have maintained longer relationships with the company.

### 4. Categorical Association Analysis

Bias-corrected Cramér's V was used to examine associations between categorical customer characteristics and churn.

The strongest associations included:

| Variable | Cramér's V |
|---|---:|
| Contract | 0.4098 |
| Tenure_Band | 0.3621 |
| OnlineSecurity | 0.3470 |
| TechSupport | 0.3425 |
| InternetService | 0.3220 |
| PaymentMethod | 0.3027 |

These results describe statistical associations, not proof of causation.

### 5. High-Risk Customer Segment

The Python segmentation analysis identified a customer combination with a reported churn rate of 75.45%:

- Month-to-month contract.
- 0–6 months tenure.
- Fiber optic internet service.
- Electronic check payment method.

This segment provides an example of how combining multiple customer characteristics can reveal groups that deserve closer retention attention.

The segment's customer count should also be considered when interpreting the percentage.

## Predictive Modeling Results

The baseline Logistic Regression model produced the following results:

| Evaluation Metric | Result |
|---|---:|
| Accuracy | 80.55% |
| Precision | 65.72% |
| Recall | 55.88% |
| F1-score | 0.6040 |
| ROC-AUC | 0.8419 |

The ROC-AUC result indicates that the baseline model demonstrates useful ability to distinguish between customers who churn and customers who remain.

### Classification Threshold Analysis

The project also examined how changing the classification threshold affects the number of customers identified for retention intervention.

| Threshold | Customers Flagged | Actual Churners Captured |
|---|---:|---:|
| 0.30 | 543 | 282 |
| 0.70 | 92 | 68 |

A lower threshold captures more actual churners but can increase the number of customers incorrectly flagged.

A higher threshold creates a smaller intervention group but misses more actual churners.

The appropriate threshold depends on business priorities, intervention costs, and available retention resources.

## Business Recommendations

Based on the analytical findings, the following actions are recommended for further investigation and implementation.

**1. Improve early customer engagement**

Customers within their first six months show elevated churn. A structured onboarding and early engagement process may help identify problems before customers leave.

**2. Review month-to-month customer retention**

Investigate the reasons behind the higher churn among month-to-month customers and communicate the benefits of suitable longer-term plans.

**3. Prioritize high-risk customer groups**

Use customer characteristics and validated predictive risk estimates to prioritize retention attention.

**4. Improve customer support and service awareness**

Investigate customer experiences with technical support, online security, and other subscribed services.

**5. Review payment-related experiences**

Examine payment difficulties and customer preferences, especially among segments with elevated observed churn.

**6. Measure retention performance**

Evaluate retention activities using customer retention rates, intervention costs, and the number of customers successfully retained.

These recommendations are based on observed analytical patterns. Their actual effectiveness should be measured after implementation.

## Tools and Technologies

| Tool | Purpose |
|---|---|
| Microsoft Excel | Spreadsheet inspection and analysis |
| Power Query | Data cleaning and transformation |
| SQL | Database development and analytical querying |
| Python | Data analysis and predictive modeling |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Scikit-learn | Machine learning and model evaluation |
| Matplotlib | Data visualization |
| Power BI | Business intelligence reporting |
| Git and GitHub | Version control |
| Visual Studio Code | Development environment |

## Repository Structure

The following structure highlights the main project directories and documentation. Individual script and output files are maintained within their respective folders.

```text
customer-churn-analysis/
│
├── data/
│   ├── raw/
│   │   └── Telco-Customer-Churn.csv
│   │
│   ├── processed/
│   │   └── customer_churn_clean.csv
│   │
│   └── analysis_outputs/
│
├── documentation/
│   ├── data_quality_assessment.md
│   ├── data_dictionary.md
│   ├── python_analysis.md
│   ├── sql_analysis.md
│   ├── powerbi_dashboard_guide.md
│   └── project_methodology.md
│
├── python/
│   ├── 01_*.py
│   ├── 02_*.py
│   ├── 03_validate_clean_data.py
│   └── ...
│
├── sql/
│   ├── schema/
│   │   ├── 01_create_customer_churn_table.sql
│   │   └── 02_create_customer_churn_view.sql
│   │
│   └── queries/
│       └── Analytical SQL queries
│
├── powerbi/
│   └── Power BI project files
│
├── .venv/
│
└── README.md
```

## Documentation

Detailed technical documentation is available in the `documentation/` directory.

| Document | Description |
|---|---|
| [Data Quality Assessment](documentation/data_quality_assessment.md) | Data quality checks, issues, cleaning decisions, and validation results |
| [Data Dictionary](documentation/data_dictionary.md) | Definitions and descriptions of dataset fields |
| [Python Analysis](documentation/python_analysis.md) | Python scripts, statistical analysis, predictive modeling, and findings |
| [SQL Analysis](documentation/sql_analysis.md) | Database schema, analytical view, SQL queries, and findings |
| [Power BI Dashboard Guide](documentation/powerbi_dashboard_guide.md) | Existing report structure, metrics, interpretation, and dashboard guidance |
| [Project Methodology](documentation/project_methodology.md) | Complete project workflow and analytical methodology |

## Reproducibility

### Requirements

The Python analysis requires:

- Python.
- The project's Python dependencies.
- The project dataset.
- The project repository structure.

### Python Environment

The project uses a local virtual environment named `.venv`.

From the project root, activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents activation, the Python executable can be called directly:

```powershell
.\.venv\Scripts\python.exe --version
```

### Validate the Processed Dataset

Run the data validation script:

```powershell
.\.venv\Scripts\python.exe .\python\03_validate_clean_data.py
```

Expected validation result:

```text
VALIDATION PASSED
```

### SQL Analysis

The SQL schema scripts and analytical queries are available in the `sql/` directory.

The database used in the project is:

```text
customer_churn_db
```

The main analytical view is:

```text
vw_customer_churn
```

Execute the schema and query scripts using a compatible SQL environment after configuring the database connection.

### Power BI

Open the available Power BI project file in Power BI Desktop.

Refresh the data sources and verify the important customer counts, churn rates, segment results, and predictive metrics against the documented analytical outputs.

## Limitations

The project has several limitations:

- The analysis is based on the supplied IBM Telco Customer Churn dataset.
- Eleven records have missing total charges, which were retained as missing.
- Observed relationships do not establish causation.
- Predictive model performance may change when applied to new customer populations.
- Classification threshold selection involves trade-offs between identifying churners and limiting unnecessary interventions.
- Business recommendations require implementation and measurement before their effectiveness can be established.

## Conclusion

This project demonstrates how a complete data analytics workflow can transform raw telecommunications customer data into meaningful business insights.

By combining data preparation, SQL, Python, machine learning, and Power BI, the analysis identifies important churn patterns, evaluates predictive performance, and develops practical customer retention recommendations.

The project demonstrates the use of analytical techniques to investigate business problems, validate data, communicate findings, and support evidence-based decisions.

---

**Project:** Customer Churn Analytics  
**Domain:** Telecommunications / Customer Analytics  
**Focus Areas:** Data Analytics, SQL, Python, Machine Learning, Power BI, Business Intelligence