
# SQL Analysis Documentation

## 1. Project Overview

### Purpose

The SQL stage of the Customer Churn Analytics project was designed to investigate customer churn patterns using structured queries.

The analysis uses SQL to examine customer retention, identify customer groups with elevated churn rates, compare customer characteristics, and investigate financial differences between customers who churned and those who remained active.

The SQL analysis complements the Python analysis and Power BI dashboard by providing a relational database approach to exploring customer churn.

### Database

Database name: `customer_churn_db`

Primary analytical view: `vw_customer_churn`

Underlying table: `customer_churn`

### SQL Files

The project contains:

- 18 analytical SQL queries.
- 2 database schema scripts.
- 1 primary customer table.
- 1 analytical database view.

---

## 2. Database Structure

### 2.1 Customer Churn Table

**File:** `sql/schema/01_create_customer_churn_table.sql`

The `customer_churn` table stores the cleaned customer dataset and its derived analytical fields.

The table uses `customer_id` as its primary key to ensure that each customer record is uniquely identified.

The schema contains 26 columns.

| Column | Data Type | Description |
|---|---|---|
| customer_id | VARCHAR(20) | Unique customer identifier and primary key |
| gender | VARCHAR(20) | Customer gender |
| senior_citizen | INTEGER | Original senior citizen indicator |
| partner | VARCHAR(10) | Whether the customer has a partner |
| dependents | VARCHAR(10) | Whether the customer has dependents |
| tenure | INTEGER | Number of months the customer has stayed |
| phone_service | VARCHAR(10) | Whether phone service is subscribed to |
| multiple_lines | VARCHAR(30) | Multiple phone line subscription status |
| internet_service | VARCHAR(30) | Internet service type |
| online_security | VARCHAR(30) | Online security subscription status |
| online_backup | VARCHAR(30) | Online backup subscription status |
| device_protection | VARCHAR(30) | Device protection subscription status |
| tech_support | VARCHAR(30) | Technical support subscription status |
| streaming_tv | VARCHAR(30) | Streaming TV subscription status |
| streaming_movies | VARCHAR(30) | Streaming movies subscription status |
| contract | VARCHAR(30) | Customer contract type |
| paperless_billing | VARCHAR(10) | Paperless billing status |
| payment_method | VARCHAR(50) | Customer payment method |
| monthly_charges | NUMERIC(10,2) | Customer's monthly charges |
| total_charges | VARCHAR(30) | Original total charges field |
| churn | VARCHAR(10) | Original customer churn status |
| total_charges_clean | NUMERIC(12,2) | Cleaned numerical total charges |
| total_charges_status | VARCHAR(20) | Status of the original total charges value |
| tenure_band | VARCHAR(20) | Derived customer tenure category |
| senior_citizen_status | VARCHAR(25) | Readable senior citizen classification |
| churn_flag | INTEGER | Numerical churn indicator |

### 2.2 Database Design Decisions

Several design decisions were made when creating the customer table.

**Primary key**

`customer_id` is the primary key because every customer must have a unique identifier.

**Financial precision**

`monthly_charges` and `total_charges_clean` use numeric data types to preserve financial precision.

**Original and cleaned total charges**

The original `total_charges` field is retained as text, while `total_charges_clean` stores the cleaned numerical version.

This allows the analysis to preserve the original source information while using a numerical field for financial calculations.

**Derived analytical fields**

The table includes additional fields created during data preparation:

- `total_charges_clean`
- `total_charges_status`
- `tenure_band`
- `senior_citizen_status`
- `churn_flag`

These fields support more efficient analytical queries.

### 2.3 Customer Churn View

**File:** `sql/schema/02_create_customer_churn_view.sql`

The project creates a database view named `vw_customer_churn`.

The view selects the relevant customer and analytical columns from the underlying `customer_churn` table.

It provides a consistent source for all 18 analytical queries.

Instead of repeatedly referencing the underlying table, the analytical queries use:

```sql
FROM vw_customer_churn;
```

The view includes customer identification, demographics, tenure, services, contract information, billing information, churn status, and derived analytical fields.

**Benefits of the view**

1. Simplifies analytical queries.
2. Provides a consistent data source.
3. Reduces repeated column-selection logic.
4. Makes the SQL analysis easier to maintain.
5. Separates the underlying table structure from the analytical query layer.

The view does not independently store another copy of the customer records. It presents data from the underlying table.

---

## 3. SQL Analysis Methodology

The SQL analysis follows a structured approach.

### Step 1: Establish the Overall Churn Position

The first query calculates the total customer population, churned customers, active customers, and overall churn rate.

### Step 2: Examine Major Customer Characteristics

The next queries investigate churn across contract types, tenure bands, demographics, and service subscriptions.

### Step 3: Investigate Combined Customer Segments

Multiple customer characteristics are combined to identify groups with potentially elevated churn rates.

### Step 4: Examine Financial Characteristics

Monthly and accumulated customer charges are compared between churned and active customers.

### Step 5: Identify a High-Risk Customer Segment

The final query isolates a specific customer segment with a high observed churn rate.

---

## 4. Analytical SQL Queries

All 18 analytical queries use `vw_customer_churn` as their primary data source.

### 4.1 Query 01 — Overall Customer Churn

**File:** `01_overall_churn.sql`

**Business Question:**

What proportion of the total customer population has churned?

**Purpose:**

Establish the overall customer retention position by calculating the total customer population, churned customers, active customers, and churn rate.

**Key Metrics:**

- Total customers
- Churned customers
- Active customers
- Overall churn rate

**SQL Techniques:**

- `COUNT()`
- `SUM()`
- Arithmetic calculations
- `ROUND()`

**Calculation:**

Churn rate is calculated as:

Churn Rate = (Churned Customers / Total Customers) × 100

**Business Value:**

This query establishes the baseline churn position against which the other customer segments can be compared.

---

### 4.2 Query 02 — Churn by Contract Type

**File:** `02_churn_by_contract.sql`

**Business Question:**

How does customer churn vary across different contract types?

**Purpose:**

Compare customer volume and churn rates across month-to-month, one-year, and two-year contracts.

**Key Metrics:**

- Customers
- Churned customers
- Churn rate

**SQL Techniques:**

- `GROUP BY`
- `SUM()`
- `COUNT()`
- `ROUND()`
- `ORDER BY`

**Business Value:**

This analysis helps identify contract types associated with higher customer churn.

It is particularly useful for evaluating whether customers with shorter contractual commitments demonstrate different retention patterns from customers with longer commitments.

---

### 4.3 Query 03 — Churn by Tenure Band

**File:** `03_churn_by_tenure.sql`

**Business Question:**

How does customer churn vary across different customer tenure groups?

**Purpose:**

Investigate the relationship between customer length of service and observed churn rates.

**Tenure Categories:**

- 0–6 Months
- 7–12 Months
- 13–24 Months
- 25–48 Months
- 49–72 Months

**Key Metrics:**

- Customers
- Churned customers
- Churn rate

**SQL Techniques:**

- `GROUP BY`
- `CASE`
- `ORDER BY`
- Aggregate functions

**Business Value:**

This query helps identify whether customers are more likely to leave during their early relationship with the company or after remaining customers for a longer period.

The `CASE` expression ensures that tenure groups are displayed in their intended chronological order rather than alphabetical order.

---

### 4.4 Query 04 — Churn by Contract and Tenure

**File:** `04_churn_by_contract_tenure.sql`

**Business Question:**

How does customer churn vary across different tenure bands within each contract type?

**Purpose:**

Combine contract type and customer tenure to investigate how retention patterns differ across customer groups.

**Grouping Dimensions:**

- Contract
- Tenure band

**Key Metrics:**

- Customers
- Churned customers
- Churn rate

**SQL Techniques:**

- Multiple-column `GROUP BY`
- Aggregate functions
- `CASE`
- `ORDER BY`

**Business Value:**

This analysis provides more detailed insights than examining contract or tenure independently.

For example, it allows the business to investigate whether newer customers on month-to-month contracts demonstrate particularly high churn.

---

### 4.5 Query 05 — Churn by Contract and Internet Service

**File:** `05_churn_by_contract_internet.sql`

**Business Question:**

How does customer churn vary across internet service types within each contract type?

**Purpose:**

Investigate the combined relationship between contract type and internet service.

**Grouping Dimensions:**

- Contract
- Internet service

**Key Metrics:**

- Customers
- Churned customers
- Churn rate

**SQL Techniques:**

- Multiple-column `GROUP BY`
- Aggregate functions
- `ORDER BY`

**Business Value:**

This query helps identify customer groups that may require additional investigation based on their contract and internet service combinations.

It also supports the investigation of whether fiber optic customers exhibit different churn patterns across contract types.

---

### 4.6 Query 06 — Churn by Contract and Payment Method

**File:** `06_churn_by_contract_payment.sql`

**Business Question:**

How does customer churn vary across different payment methods within each contract type?

**Purpose:**

Compare customer retention across combinations of contract type and payment method.

**Grouping Dimensions:**

- Contract
- Payment method

**Key Metrics:**

- Customers
- Churned customers
- Churn rate

**SQL Techniques:**

- Multiple-column `GROUP BY`
- Aggregate functions
- `ORDER BY`

**Business Value:**

This analysis helps identify payment methods associated with higher or lower observed churn within different contract categories.

The results can support further investigation into payment experience, billing preferences, and customer retention.

---

### 4.7 Query 07 — Churn by Contract, Payment Method, and Tenure

**File:** `07_churn_by_contract_payment_tenure.sql`

**Business Question:**

Among month-to-month customers who use electronic check, how does churn vary across different tenure bands?

**Purpose:**

Investigate a specific customer group by combining three characteristics.

**Filters:**

- Contract = Month-to-month
- Payment Method = Electronic check

**Grouping Dimension:**

- Tenure band

**Key Metrics:**

- Customers
- Churned customers
- Churn rate

**SQL Techniques:**

- `WHERE`
- Multiple filter conditions using `AND`
- `GROUP BY`
- `CASE`
- Aggregate functions

**Business Value:**

This query investigates whether the churn observed among month-to-month electronic-check customers is concentrated among newer customers or distributed across different tenure groups.

---

### 4.8 Query 08 — Churn by Senior Citizen Status

**File:** `08_churn_by_senior_citizen.sql`

**Business Question:**

How does customer churn vary between senior citizens and non-senior citizens?

**Purpose:**

Compare customer retention patterns across the two senior citizen classifications.

**Grouping Dimension:**

- Senior citizen status

**Key Metrics:**

- Customers
- Churned customers
- Churn rate

**SQL Techniques:**

- `GROUP BY`
- Aggregate functions
- `ORDER BY`

**Business Value:**

This query helps investigate whether senior citizen status is associated with differences in observed customer churn.

---

### 4.9 Query 09 — Churn by Partner Status

**File:** `09_churn_by_partner.sql`

**Business Question:**

How does customer churn vary between customers who have a partner and those who do not?

**Purpose:**

Examine customer retention based on partner status.

**Grouping Dimension:**

- Partner

**Key Metrics:**

- Customers
- Churned customers
- Churn rate

**SQL Techniques:**

- `GROUP BY`
- Aggregate functions
- `ORDER BY`

**Business Value:**

This analysis helps determine whether customers with different household characteristics demonstrate different observed retention patterns.

---

### 4.10 Query 10 — Churn by Dependents Status

**File:** `10_churn_by_dependents.sql`

**Business Question:**

How does customer churn vary between customers with dependents and customers without dependents?

**Purpose:**

Compare retention patterns based on dependent status.

**Grouping Dimension:**

- Dependents

**Key Metrics:**

- Customers
- Churned customers
- Churn rate

**SQL Techniques:**

- `GROUP BY`
- Aggregate functions
- `ORDER BY`

**Business Value:**

The results help investigate whether having dependents is associated with different observed customer retention patterns.

---

### 4.11 Query 11 — Churn by Tech Support

**File:** `11_churn_by_tech_support.sql`

**Business Question:**

How does customer churn vary between customers with and without Tech Support?

**Purpose:**

Compare customer retention based on technical support subscription status.

**Grouping Dimension:**

- Tech Support

**Key Metrics:**

- Customers
- Churned customers
- Churn rate

**SQL Techniques:**

- `GROUP BY`
- Aggregate functions
- `ORDER BY`

**Business Value:**

This analysis helps investigate whether access to technical support is associated with different observed churn rates.

It can support further investigation into customer service experience and retention.

---

### 4.12 Query 12 — Churn by Online Security

**File:** `12_churn_by_online_security.sql`

**Business Question:**

How does customer churn vary between customers with and without Online Security?

**Purpose:**

Investigate customer retention based on online security subscription status.

**Grouping Dimension:**

- Online Security

**Key Metrics:**

- Customers
- Churned customers
- Churn rate

**SQL Techniques:**

- `GROUP BY`
- Aggregate functions
- `ORDER BY`

**Business Value:**

This analysis helps determine whether online security subscription status is associated with different observed customer retention patterns.

---

### 4.13 Query 13 — Churn by Online Backup

**File:** `13_churn_by_online_backup.sql`

**Business Question:**

How does customer churn vary between customers with and without Online Backup?

**Purpose:**

Compare churn patterns across online backup subscription categories.

**Grouping Dimension:**

- Online Backup

**Key Metrics:**

- Customers
- Churned customers
- Churn rate

**SQL Techniques:**

- `GROUP BY`
- Aggregate functions
- `ORDER BY`

**Business Value:**

The analysis helps investigate whether customers with different online backup subscription statuses demonstrate different observed retention patterns.

---

### 4.14 Query 14 — Churn by Device Protection

**File:** `14_churn_by_device_protection.sql`

**Business Question:**

How does customer churn vary between customers with and without Device Protection?

**Purpose:**

Examine customer retention based on device protection subscription status.

**Grouping Dimension:**

- Device Protection

**Key Metrics:**

- Customers
- Churned customers
- Churn rate

**SQL Techniques:**

- `GROUP BY`
- Aggregate functions
- `ORDER BY`

**Business Value:**

This query helps identify whether device protection subscription status is associated with different observed churn patterns.

---

### 4.15 Query 15 — Churn by Monthly Charges

**File:** `15_churn_by_monthly_charges.sql`

**Business Question:**

How do monthly charges differ between customers who churned and customers who remained active?

**Purpose:**

Compare monthly spending characteristics across customer churn groups.

**Grouping Dimension:**

- Churn status

**Key Metrics:**

- Customer count
- Average monthly charges
- Minimum monthly charges
- Maximum monthly charges

**SQL Techniques:**

- `GROUP BY`
- `AVG()`
- `MIN()`
- `MAX()`
- `ROUND()`

**Business Value:**

This analysis helps investigate whether monthly spending levels differ between churned and retained customers.

It can support further examination of pricing, affordability, and perceived customer value.

**Important implementation note:**

The current SQL query calculates customer count and monthly charge statistics. Although its original comment lists churn rate as a key metric, churn rate is not explicitly calculated in the query.

---

### 4.16 Query 16 — Churn by Total Charges

**File:** `16_churn_by_total_charges.sql`

**Business Question:**

How do accumulated customer charges differ between customers who churned and customers who remained active?

**Purpose:**

Compare accumulated financial contributions across customer churn groups.

**Grouping Dimension:**

- Churn status

**Key Metrics:**

- Customers with recorded charges
- Total accumulated charges
- Average total charges
- Minimum total charges
- Maximum total charges

**SQL Techniques:**

- `WHERE`
- `IS NOT NULL`
- `GROUP BY`
- `SUM()`
- `AVG()`
- `MIN()`
- `MAX()`
- `ROUND()`

**Data Quality Consideration:**

The query filters out records where `total_charges_clean` is NULL.

This prevents customers with unavailable accumulated charge values from being included in the financial calculations.

**Business Value:**

The results help compare accumulated customer charges between churned and retained customers.

They also provide additional financial context when interpreting customer tenure and retention.

---

### 4.17 Query 17 — Month-to-Month Churn by Tenure

**File:** `17_month_to_month_churn_by_tenure.sql`

**Business Question:**

Among month-to-month customers, how does churn vary across different tenure bands?

**Purpose:**

Focus specifically on month-to-month customers and investigate how retention changes across their tenure groups.

**Filter:**

- Contract = Month-to-month

**Grouping Dimension:**

- Tenure band

**Key Metrics:**

- Customers
- Churned customers
- Churn rate

**SQL Techniques:**

- `WHERE`
- `GROUP BY`
- `CASE`
- Aggregate functions
- `ORDER BY`

**Business Value:**

This query provides a more focused investigation of month-to-month customers.

It helps identify whether early-tenure customers within this contract category experience higher observed churn than longer-tenured customers.

---

### 4.18 Query 18 — High-Risk Customer Segment

**File:** `18_high_risk_customer_segment.sql`

**Business Question:**

What is the observed churn rate among customers who have a month-to-month contract, are within their first six months, use fiber optic internet, and pay by electronic check?

**Purpose:**

Identify a concentrated customer segment with a potentially elevated churn rate.

**Segment Conditions:**

- Contract = Month-to-month
- Tenure band = 0–6 Months
- Internet Service = Fiber optic
- Payment Method = Electronic check

**Key Metrics:**

- Segment customers
- Churned customers
- Segment churn rate

**SQL Techniques:**

- `WHERE`
- Multiple `AND` conditions
- `COUNT()`
- `SUM()`
- `ROUND()`

**Business Value:**

This query isolates a specific customer group for further investigation and retention planning.

It provides a focused segment-level view rather than relying only on individual churn drivers.

The resulting segment should be interpreted as an observed high-churn group, not as proof that its characteristics cause customers to leave.

---

## 5. SQL Techniques Applied

The project demonstrates several important SQL techniques used in practical data analytics.

| SQL Technique | Application |
|---|---|
| `SELECT` | Retrieve relevant customer fields |
| `FROM` | Define the analytical data source |
| `WHERE` | Filter customer records |
| `AND` | Combine multiple filtering conditions |
| `GROUP BY` | Aggregate customer records into categories |
| `ORDER BY` | Sort analytical results |
| `CASE` | Apply custom ordering to tenure bands |
| `COUNT()` | Calculate customer counts |
| `SUM()` | Calculate churned customer counts and accumulated charges |
| `AVG()` | Calculate average financial values |
| `MIN()` | Identify minimum financial values |
| `MAX()` | Identify maximum financial values |
| `ROUND()` | Format numerical results |
| `IS NOT NULL` | Exclude unavailable financial values |
| `CREATE TABLE` | Define the underlying database structure |
| `CREATE OR REPLACE VIEW` | Create the analytical database view |

### 5.1 Churn Rate Calculation

Most segmentation queries use the following calculation:

```sql
ROUND(
    SUM(churn_flag) * 100.0 / COUNT(*),
    2
) AS churn_rate
```

The `churn_flag` field uses:

- 1 = Customer churned.
- 0 = Customer remained active.

Multiplying by 100 converts the resulting proportion into a percentage.

The use of `100.0` ensures decimal arithmetic, while `ROUND()` limits the displayed result to two decimal places.

### 5.2 Custom Category Ordering

Tenure categories are ordered using a `CASE` expression.

```sql
ORDER BY
    CASE tenure_band
        WHEN '0–6 Months' THEN 1
        WHEN '7–12 Months' THEN 2
        WHEN '13–24 Months' THEN 3
        WHEN '25–48 Months' THEN 4
        WHEN '49–72 Months' THEN 5
    END;
```

This ensures that tenure groups appear in chronological order.

Without this custom ordering, SQL may sort the text values alphabetically rather than according to the actual tenure progression.

---

## 6. Major Findings From the SQL Analysis

The SQL queries support several important findings established across the wider project analysis.

### 6.1 Overall Customer Churn

The customer dataset contains 7,043 customers.

- Churned customers: 1,869
- Active customers: 5,174
- Overall churn rate: 26.54%

This establishes the baseline for evaluating customer retention.

### 6.2 Contract Type

| Contract | Churn Rate |
|---|---:|
| Month-to-month | 42.71% |
| One year | 11.27% |
| Two year | 2.83% |

Month-to-month customers demonstrate substantially higher observed churn than customers on longer contracts.

### 6.3 Customer Tenure

The wider project analysis identified an elevated churn rate among customers within their first six months.

The churn rate for the 0–6 month tenure group was 52.94%, compared with 9.51% among customers with 49–72 months of tenure.

This highlights the importance of early customer retention.

### 6.4 High-Risk Customer Segment

The project identified a high-risk segment combining:

- Month-to-month contracts.
- Early customer tenure.
- Fiber optic internet.
- Electronic check payments.

The wider Python segmentation analysis identified a segment churn rate of 75.45%.

This finding supports targeted retention investigation.

**Note:** The 75.45% result is a finding from the wider project analysis. It should not be interpreted as a SQL query result unless the SQL query output has independently been verified.

### 6.5 Financial Characteristics

The monthly and total charges queries provide a financial perspective on churn.

They help investigate:

- Differences in average monthly charges.
- Differences in accumulated customer charges.
- The distribution of financial contributions across churn groups.

These comparisons should be interpreted alongside tenure because customers who have remained longer generally have more time to accumulate total charges.

---

## 7. SQL Analysis Limitations

Although the SQL queries provide useful analytical insights, some limitations should be considered.

### 7.1 Descriptive Analysis

The SQL queries primarily describe observed customer behaviour.

They do not establish causal relationships between customer characteristics and churn.

### 7.2 Segment Size

A high churn rate does not necessarily mean that a segment contributes the largest number of churned customers.

Customer counts should always be considered alongside churn percentages.

### 7.3 Missing Total Charges

Query 16 excludes customers whose cleaned total charges are unavailable.

Consequently, its financial comparisons are based only on customers with recorded numerical total charges.

### 7.4 Correlation and Association

Observed differences across contract, payment, service, and demographic groups should not automatically be interpreted as evidence of causation.

Additional statistical analysis is required to investigate the strength of relationships.

### 7.5 Static Analysis

The SQL queries operate on the available dataset.

Their results will need to be refreshed when the underlying customer data changes.

---

## 8. SQL Project Outputs

The SQL folder is organized into two main directories.

### Schema

```text
sql/
└── schema/
    ├── 01_create_customer_churn_table.sql
    └── 02_create_customer_churn_view.sql
```

### Analytical Queries

```text
sql/
└── queries/
    ├── 01_overall_churn.sql
    ├── 02_churn_by_contract.sql
    ├── 03_churn_by_tenure.sql
    ├── 04_churn_by_contract_tenure.sql
    ├── 05_churn_by_contract_internet.sql
    ├── 06_churn_by_contract_payment.sql
    ├── 07_churn_by_contract_payment_tenure.sql
    ├── 08_churn_by_senior_citizen.sql
    ├── 09_churn_by_partner.sql
    ├── 10_churn_by_dependents.sql
    ├── 11_churn_by_tech_support.sql
    ├── 12_churn_by_online_security.sql
    ├── 13_churn_by_online_backup.sql
    ├── 14_churn_by_device_protection.sql
    ├── 15_churn_by_monthly_charges.sql
    ├── 16_churn_by_total_charges.sql
    ├── 17_month_to_month_churn_by_tenure.sql
    └── 18_high_risk_customer_segment.sql
```

---

## 9. Reproducibility

The SQL analysis can be reproduced using the following general sequence:

1. Create or select the `customer_churn_db` database.
2. Execute `01_create_customer_churn_table.sql`.
3. Load the cleaned customer dataset into `customer_churn`.
4. Execute `02_create_customer_churn_view.sql`.
5. Execute the analytical queries in the `sql/queries` directory.
6. Review the results and compare them with the Python analysis.
7. Use the validated analytical findings to support the Power BI dashboard.

The analytical queries depend on the database table and view being created and populated before execution.

The data-loading operation is a separate step from the two supplied schema scripts.

---

## 10. Overall SQL Stage Conclusion

The SQL stage provided a structured approach to investigating customer churn using relational database queries.

The analysis covered overall churn, contract type, customer tenure, demographic characteristics, service subscriptions, payment methods, financial charges, and combined high-risk customer segments.

The use of a dedicated customer table and analytical view provided a consistent foundation for the 18 queries.

The SQL findings complement the Python analysis by allowing customer behaviour to be examined through database-level aggregation and filtering.

Together, these analyses provide a stronger foundation for the Power BI dashboard and the project's final business recommendations.

The SQL stage demonstrates practical skills in:

- Relational database design.
- Table and view creation.
- Data aggregation.
- Customer segmentation.
- Conditional filtering.
- Financial analysis.
- Business-oriented SQL querying.
- Analytical result interpretation.

**The SQL stage therefore contributes an important component to the end-to-end Customer Churn Analytics project.**
