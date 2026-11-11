# Project Methodology

## 1. Introduction

This document explains the methodology followed in the Customer Churn Analytics project.

The project uses a structured data analytics workflow to investigate customer churn in a telecommunications business. It combines data preparation, data quality assessment, SQL analysis, Python-based statistical and predictive analysis, and Power BI reporting.

The methodology is designed to move from raw customer records to validated analytical findings and practical business recommendations.

The project follows these major stages:

1. Business problem definition.
2. Data acquisition and understanding.
3. Data quality assessment.
4. Data cleaning and preparation.
5. Exploratory data analysis.
6. SQL database development and analysis.
7. Python statistical and predictive analysis.
8. Power BI business intelligence reporting.
9. Business recommendations and conclusions.
10. Validation and documentation.

## 2. Business Problem Definition

Customer churn occurs when customers discontinue a company's products or services.

For a telecommunications company, customer churn can affect revenue, customer lifetime value, business growth, and the cost of acquiring replacement customers.

The main business problem addressed in this project is the need to understand customer churn patterns and identify customer groups that may require retention attention.

### 2.1 Business Questions

The project was designed to answer the following questions:

- What percentage of customers have churned?
- How many customers have left compared with those who remain?
- Which contract categories have higher churn rates?
- How does customer tenure relate to churn?
- Which customer services and payment methods are associated with churn?
- Which combinations of customer characteristics identify high-risk segments?
- How effectively can machine learning models identify customers likely to churn?
- How can the findings support customer retention decisions?

### 2.2 Project Objectives

The objectives are to:

- Assess the quality and reliability of the customer dataset.
- Prepare a clean and analysis-ready dataset.
- Use SQL to investigate customer churn patterns.
- Apply Python for exploratory, statistical, and predictive analysis.
- Evaluate machine learning model performance.
- Develop a Power BI report for communicating findings.
- Recommend practical retention strategies based on analytical evidence.

## 3. Data Acquisition and Understanding

### 3.1 Dataset Source

The project uses the IBM Telco Customer Churn dataset.

The raw dataset is stored at:

`data/raw/Telco-Customer-Churn.csv`

### 3.2 Dataset Structure

| Attribute | Description |
|---|---|
| Original records | 7,043 |
| Original columns | 21 |
| Customer identifier | customerID |
| Target variable | Churn |
| Dataset subject | Telecommunications customers |

The dataset contains customer demographic information, account characteristics, subscribed services, billing information, tenure, and churn status.

### 3.3 Target Variable

The primary target variable is `Churn`.

It contains two possible outcomes:

- Yes: The customer has churned.
- No: The customer has remained with the company.

For numerical analysis, the project also uses a derived `Churn_Flag` field.

This provides a numerical representation of the churn outcome for calculations and modeling.

## 4. Data Quality Assessment

Before performing detailed analysis, the dataset was examined to identify quality issues that could affect analytical accuracy.

The assessment considered:

- Missing values.
- Duplicate records.
- Duplicate customer identifiers.
- Incorrect data types.
- Invalid categorical values.
- Inconsistent numerical values.
- Unusual tenure and billing records.
- Target variable consistency.

### 4.1 Key Data Quality Findings

| Data Quality Check | Result |
|---|---|
| Total records | 7,043 |
| Total original columns | 21 |
| Duplicate rows | 0 |
| Duplicate customer IDs | 0 |
| Records with recorded TotalCharges | 7,032 |
| Records with missing TotalCharges | 11 |
| Invalid churn flags | 0 |

The assessment identified 11 records where the original `TotalCharges` field was blank.

These records were investigated rather than automatically assigned zero financial values.

### 4.2 Zero-Tenure Customers

The 11 customers with missing total charges also had zero tenure.

This pattern was considered when deciding how to handle the missing financial values.

The missing values were retained as missing because an absent recorded charge should not automatically be interpreted as a confirmed financial value of zero.

### 4.3 Data Quality Documentation

The detailed findings, validation checks, cleaning decisions, and limitations are documented in:

`documentation/data_quality_assessment.md`

## 5. Data Cleaning and Preparation

The data preparation stage transformed the original dataset into a structured format suitable for analysis.

The main objective was to improve data consistency while preserving the underlying customer information.

### 5.1 Cleaning Activities

The preparation process included:

- Inspecting column names and data types.
- Checking customer identifiers.
- Reviewing missing values.
- Converting financial fields into appropriate numerical formats.
- Creating a cleaned total charges field.
- Creating customer tenure categories.
- Creating a readable senior citizen category.
- Creating a numerical churn indicator.
- Validating the processed dataset.

### 5.2 Derived Analytical Fields

Five additional analytical fields were created.

| Derived Field | Purpose |
|---|---|
| TotalCharges_Clean | Stores total charges in a numeric format |
| TotalCharges_Status | Identifies the status of total charges data |
| Tenure_Band | Groups customers into tenure categories |
| SeniorCitizen_Status | Provides readable senior citizen categories |
| Churn_Flag | Represents churn as a numerical indicator |

### 5.3 Tenure Segmentation

Customer tenure was grouped into the following categories:

| Tenure Band | Description |
|---|---|
| 0–6 Months | Very early customer relationship |
| 7–12 Months | Early customer relationship |
| 13–24 Months | Developing customer relationship |
| 25–48 Months | Established customer relationship |
| 49–72 Months | Long-term customer relationship |

This segmentation makes it easier to compare churn behavior across different stages of the customer relationship.

### 5.4 Processed Dataset

The final processed dataset is stored at:

`data/processed/customer_churn_clean.csv`

Its validated structure contains:

- 7,043 records.
- 26 columns.

The processed dataset serves as the foundation for the subsequent analytical stages.

## 6. Exploratory Data Analysis

Exploratory Data Analysis (EDA) was used to understand the structure of the processed dataset and investigate patterns associated with customer churn.

The analysis considered both numerical and categorical variables.

### 6.1 Customer Distribution

The analysis examined the distribution of customers according to their churn status.

| Customer Status | Customers |
|---|---:|
| Churned | 1,869 |
| Active | 5,174 |
| Total | 7,043 |

The overall churn rate was calculated as:

\[
\text{Churn Rate} =
\frac{1,869}{7,043}\times100
=26.54\%
\]

### 6.2 Categorical Analysis

Categorical variables were compared against the churn outcome.

The investigation included:

- Contract.
- InternetService.
- PaymentMethod.
- OnlineSecurity.
- TechSupport.
- OnlineBackup.
- DeviceProtection.
- Partner.
- Dependents.
- SeniorCitizen_Status.

### 6.3 Numerical Analysis

Numerical variables were also investigated to understand their relationship with customer churn.

Important numerical variables included:

- Tenure.
- MonthlyCharges.
- TotalCharges_Clean.

The analysis examined customer distributions and differences between churned and retained customers.

### 6.4 Exploratory Analysis Outputs

Exploratory findings were used to guide more focused SQL analysis, statistical analysis, predictive modeling, and customer segmentation.

The detailed Python analysis and its generated outputs are documented in:

`documentation/python_analysis.md`

## 7. SQL Database Development and Analysis

SQL was used to organize the processed customer data and perform structured analytical queries.

The project uses the `customer_churn_db` database.

### 7.1 Database Structure

The SQL stage includes:

- A customer churn table.
- A customer churn analytical view.
- Eighteen analytical SQL queries.
- Schema creation scripts.

The main table is:

`customer_churn`

The analytical view is:

`vw_customer_churn`

### 7.2 SQL Schema Development

The database schema was designed to store the customer information and derived analytical fields.

The schema includes customer identifiers, categorical attributes, service information, financial values, tenure, and churn indicators.

The customer identifier is the primary key.

### 7.3 Analytical SQL Queries

The SQL analysis investigated:

- Overall customer churn.
- Churn by contract type.
- Churn by tenure band.
- Churn by contract and tenure.
- Churn by contract and internet service.
- Churn by contract and payment method.
- Early-tenure month-to-month customers.
- Churn by senior citizen status.
- Churn by partner and dependents.
- Churn by technical support and security services.
- Monthly charges by churn status.
- Total charges by churn status.
- High-risk customer combinations.

### 7.4 SQL Findings

The SQL analysis supported several important findings.

| Contract Type | Churn Rate |
|---|---:|
| Month-to-month | 42.71% |
| One year | 11.27% |
| Two year | 2.83% |

These results show substantial differences in observed churn across contract categories.

SQL provided a structured way to investigate customer groups and validate findings from the wider analytical workflow.

Detailed SQL scripts, query explanations, and findings are documented in:

`documentation/sql_analysis.md`

## 8. Python Statistical and Predictive Analysis

Python was used for deeper analytical investigation, statistical evaluation, customer segmentation, and predictive modeling.

The project uses a dedicated virtual environment:

`.venv`

Python scripts are stored in:

`python/`

### 8.1 Python Analysis Activities

The Python stage included:

- Data inspection and validation.
- Exploratory data analysis.
- Customer churn segmentation.
- Statistical association analysis.
- Predictive model development.
- Model evaluation.
- Classification threshold analysis.
- Business impact analysis.

### 8.2 Statistical Association Analysis

Categorical variables were examined using bias-corrected Cramér's V.

This measure helps evaluate the strength of association between categorical variables and the churn outcome.

Important results included:

| Variable | Cramér's V | Project Interpretation |
|---|---:|---|
| Contract | 0.4098 | Strong |
| Tenure_Band | 0.3621 | Strong |
| OnlineSecurity | 0.3470 | Strong |
| TechSupport | 0.3425 | Strong |
| InternetService | 0.3220 | Strong |
| PaymentMethod | 0.3027 | Strong |
| OnlineBackup | 0.2919 | Moderate |
| DeviceProtection | 0.2811 | Moderate |
| Dependents | 0.1638 | Weak |
| SeniorCitizen_Status | 0.1504 | Weak |
| Partner | 0.1500 | Weak |

The strength labels use the project's descriptive interpretation thresholds. They should not be treated as universal statistical standards.

Association does not establish causation.

### 8.3 Predictive Modeling

Machine learning was applied to investigate whether customer characteristics could help identify customers likely to churn.

The baseline Logistic Regression model achieved the following evaluation results:

| Metric | Result |
|---|---:|
| Accuracy | 80.55% |
| Precision | 65.72% |
| Recall | 55.88% |
| F1-score | 0.6040 |
| ROC-AUC | 0.8419 |

These metrics provide different perspectives on model performance.

Accuracy measures overall prediction correctness, precision measures the reliability of positive predictions, recall measures the proportion of actual churners detected, F1-score balances precision and recall, and ROC-AUC measures the model's ability to distinguish between the two classes.

### 8.4 Classification Threshold Analysis

The classification threshold was investigated to understand how different decision thresholds affect the number of customers identified for intervention.

Examples from the analysis include:

| Threshold | Customers Flagged | Actual Churners Captured |
|---|---:|---:|
| 0.30 | 543 | 282 |
| 0.70 | 92 | 68 |

A lower threshold can identify more potential churners but may also increase unnecessary retention interventions.

A higher threshold produces a smaller group but can miss more customers who eventually churn.

### 8.5 High-Risk Customer Segmentation

The segmentation analysis identified an important high-risk combination:

- Month-to-month contract.
- 0–6 months tenure.
- Fiber optic internet service.
- Electronic check payment method.

The reported churn rate for this segment was 75.45%.

This finding supports targeted investigation and retention attention.

The segment's customer count should also be considered when interpreting its churn rate.

### 8.6 Python Outputs

Python generated analytical outputs in the project output directories, including:

- Customer churn summaries.
- High-risk customer segment results.
- Model comparison results.
- Confusion matrix results.
- Threshold analysis results.
- Categorical association results.

The detailed script-by-script explanations, methodology, findings, and output descriptions are documented in:

`documentation/python_analysis.md`

## 9. Power BI Business Intelligence Reporting

Power BI was used to communicate the analytical findings through a multi-page report.

The purpose of this stage was to transform technical results into business-friendly information that stakeholders could understand and use.

### 9.1 Report Structure

The existing report contains six pages:

| Page | Main Purpose |
|---|---|
| Executive Overview | Summarizes overall customer churn |
| Churn Drivers | Investigates customer attributes associated with churn |
| High-Risk Segments | Highlights customer groups with elevated churn |
| Predictive Intelligence | Presents predictive model performance |
| Retention Strategy | Translates findings into retention actions |
| Insight & Recommendation | Summarizes conclusions and priorities |

### 9.2 Reporting Objectives

The Power BI report was designed to:

- Communicate important churn metrics.
- Support customer segment comparisons.
- Present important analytical findings.
- Explain predictive model performance.
- Connect analysis to business recommendations.
- Provide a clear reporting experience.

### 9.3 Future Dashboard Redesign

An advanced Power BI dashboard using HTML Content is planned as a future improvement.

The intended redesign will focus on more advanced visual presentation, reusable HTML-based components, improved layout, and a more cohesive user experience.

This methodology documents the existing report baseline and does not claim that the planned redesign has already been implemented.

Detailed page descriptions, metric definitions, validation checks, and dashboard guidance are documented in:

`documentation/powerbi_dashboard_guide.md`

## 10. Business Findings and Recommendations

The analytical stages produced findings that can support customer retention decisions.

### 10.1 Overall Churn

The dataset contains 7,043 customers, of whom 1,869 churned.

The overall churn rate is 26.54%.

This indicates that customer retention is an important business concern within the analyzed population.

### 10.2 Contract Type

Month-to-month customers have a churn rate of 42.71%, compared with 11.27% for one-year customers and 2.83% for two-year customers.

**Recommendation:** Investigate the needs of month-to-month customers and communicate the benefits of longer-term plans where appropriate.

### 10.3 Customer Tenure

Customers in the 0–6 months tenure band have an observed churn rate of 52.94%.

**Recommendation:** Strengthen onboarding and early customer engagement to identify service problems before customers decide to leave.

### 10.4 High-Risk Segment

The identified combination of month-to-month contract, early tenure, fiber optic service, and electronic check payment has a reported churn rate of 75.45%.

**Recommendation:** Consider targeted retention attention for customers with similar characteristics while evaluating segment size and intervention costs.

### 10.5 Customer Support and Security Services

OnlineSecurity and TechSupport showed important categorical associations with churn.

**Recommendation:** Investigate customer awareness, service adoption, and support experiences before deciding which interventions are most appropriate.

### 10.6 Predictive Retention

The baseline Logistic Regression model achieved an ROC-AUC of 0.8419.

**Recommendation:** Use predictive scores as decision-support information to prioritize customer engagement, while monitoring false positives, missed churners, and intervention outcomes.

### 10.7 Measuring Retention Effectiveness

Recommendations should be evaluated after implementation.

Possible measures include:

- Retention rate among contacted customers.
- Churn rate among targeted customer segments.
- Number of customers successfully retained.
- Retention campaign cost.
- Revenue associated with retained customers.
- Differences between contacted and comparable non-contacted customers.

Where practical, controlled experiments should be used to determine whether an intervention actually improves retention.

## 11. Validation and Reproducibility

Validation was performed at different stages to improve confidence in the results.

### 11.1 Data Validation

The processed dataset was checked for:

- Expected row and column counts.
- Duplicate customer identifiers.
- Missing values.
- Valid churn categories.
- Correct derived fields.
- Consistent tenure categories.

The validation script is:

`python/03_validate_clean_data.py`

Run it from the project root using:

```powershell
.\.venv\Scripts\python.exe .\python\03_validate_clean_data.py
```

The validation script returned:

`VALIDATION PASSED`

### 11.2 SQL Validation

The SQL stage supports reproducibility through schema scripts, a reusable analytical view, and individual query files.

Analytical results should be checked against the processed dataset and Python findings where the same metric definitions apply.

### 11.3 Python Reproducibility

The Python environment and scripts are maintained within the project repository.

Run Python scripts using the project's virtual environment to reduce dependency inconsistencies.

### 11.4 Power BI Validation

The report should be checked against the documented analytical results.

Important checks include customer counts, churn counts, churn rates, segment calculations, and predictive model metrics.

### 11.5 Documentation

The methodology and technical details are separated into focused documentation files:

- `documentation/data_quality_assessment.md`
- `documentation/data_dictionary.md`
- `documentation/python_analysis.md`
- `documentation/sql_analysis.md`
- `documentation/powerbi_dashboard_guide.md`

## 12. Project Limitations

The project has several limitations that should be considered when interpreting its findings.

### 12.1 Dataset Limitations

The analysis is based on the supplied IBM Telco Customer Churn dataset. Its findings may not represent every telecommunications company or customer population.

### 12.2 Missing Financial Values

Eleven records contain missing total charges. These values were retained as missing rather than automatically replaced with zero.

### 12.3 Observational Analysis

The relationships identified between customer characteristics and churn are observational. They do not independently prove causation.

### 12.4 Predictive Model Limitations

Predictive performance depends on the available dataset, model configuration, and evaluation methodology.

The model should be evaluated again before being applied to a different or future customer population.

### 12.5 Retention Recommendation Limitations

The recommendations are based on analytical evidence and business reasoning. Their actual impact requires implementation and measurement.

### 12.6 Dashboard Redesign

The HTML Content dashboard redesign remains a planned improvement. The existing Power BI documentation describes the current six-page report baseline.

## 13. Tools and Technologies

The project uses the following tools and technologies:

| Tool or Technology | Role in the Project |
|---|---|
| Microsoft Excel | Initial data inspection and spreadsheet analysis |
| Power Query | Data transformation and preparation |
| SQL | Database development and analytical queries |
| Python | Data analysis, statistical analysis, segmentation, and machine learning |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical operations |
| Scikit-learn | Predictive modeling and evaluation |
| Matplotlib | Data visualization |
| Power BI | Business intelligence reporting |
| Git and GitHub | Version control and project management |
| Visual Studio Code | Development environment |

## 14. Overall Project Workflow

The project follows this sequence:

1. Obtain the original customer churn dataset.
2. Inspect the dataset and understand its structure.
3. Assess data quality and identify inconsistencies.
4. Clean and prepare the customer records.
5. Create additional analytical fields.
6. Validate the processed dataset.
7. Develop the SQL database structure.
8. Create the analytical SQL view.
9. Execute SQL queries to investigate churn patterns.
10. Perform exploratory and statistical analysis in Python.
11. Develop and evaluate predictive models.
12. Investigate classification threshold trade-offs.
13. Identify high-risk customer segments.
14. Build the Power BI report.
15. Interpret findings and develop retention recommendations.
16. Validate the final analytical outputs.
17. Document the methodology and project findings.

## 15. Conclusion

The Customer Churn Analytics project demonstrates an end-to-end data analytics workflow using a real-world telecommunications customer dataset.

The methodology combines data quality assessment, data preparation, SQL analysis, Python statistical and predictive analysis, and Power BI reporting.

The project identified an overall churn rate of 26.54%, substantial differences in churn across contract types, elevated churn among early-tenure customers, and a high-risk customer segment with a reported churn rate of 75.45%.

The predictive modeling stage also demonstrated how machine learning can support customer risk identification, with the baseline Logistic Regression model achieving an ROC-AUC of 0.8419.

The final objective is not simply to describe customer churn but to demonstrate how structured data analysis can produce evidence-based insights and support practical business decisions.

The project also provides a reproducible analytical foundation that can be extended through future dashboard improvements, additional modeling, and retention performance measurement.