# Python Analysis Documentation

## Customer Churn Analytics Project

### Purpose

The Python analysis stage was designed to provide a reproducible analytical workflow for understanding customer churn and evaluating whether customer and service characteristics could be used to identify customers with a higher likelihood of churn.

The analysis was intentionally structured as a progression:

1. Data profiling
2. Data cleaning
3. Data validation
4. Descriptive churn analysis
5. Customer segment analysis
6. Feature association analysis
7. Statistical association analysis
8. Baseline churn prediction
9. Model refinement
10. Model comparison
11. Classification threshold analysis
12. Business impact analysis

The Python workflow reads the cleaned dataset from `data/processed/customer_churn_clean.csv` and saves analytical outputs to `data/analysis_outputs/`.

The raw dataset is never modified.

---

# 1. Python Environment

The analysis was conducted using a Python virtual environment.

Key libraries used include:

* pandas
* matplotlib
* scipy
* scikit-learn

The main purposes of these libraries were:

| Library      | Purpose                                                                        |
| ------------ | ------------------------------------------------------------------------------ |
| pandas       | Data loading, cleaning, transformation, grouping, and analysis                 |
| matplotlib   | Analytical visualizations                                                      |
| scipy        | Statistical association analysis                                               |
| scikit-learn | Machine learning, preprocessing, model evaluation, and classification analysis |

The project uses Python scripts rather than performing the analysis manually so that the workflow can be reproduced when the dataset is refreshed or additional records are added.

---

# 2. Dataset Overview

The original IBM Telco Customer Churn dataset contains:

* 7,043 customers
* 21 original columns
* 0 duplicate rows
* 0 duplicate customer IDs

The target variable is:

`Churn`

with two possible values:

* `Yes`
* `No`

The dataset contains:

* 1,869 churned customers
* 5,174 active customers

Overall churn rate:

**26.54%**

This means the churn target is imbalanced, with active customers representing the majority class.

Because of this imbalance, predictive model evaluation should not rely on accuracy alone. Precision, recall, F1-score, ROC-AUC, and confusion matrices were therefore included.

---

# 3. Script 01 — Data Profiling

File:

`python/01_data_profiling.py`

## Purpose

The first script was used to understand the structure and quality of the raw dataset before making any transformations.

The profiling stage examined:

* Dataset dimensions
* Column data types
* Missing values
* Duplicate rows
* Duplicate customer IDs
* Unique values
* Numerical ranges
* Category distributions
* Churn distribution

## Key findings

### Dataset structure

* Rows: 7,043
* Columns: 21

### Duplicate records

* Duplicate rows: 0
* Duplicate customer IDs: 0

The `customerID` field is therefore suitable as a unique customer identifier.

### TotalCharges issue

`TotalCharges` was originally stored as a text field.

There were:

* 11 blank `TotalCharges` values

After conversion to numeric, these became 11 missing numeric values.

All 11 affected customers had:

* `tenure = 0`
* `Churn = No`

This suggests that these records represent customers with no recorded accumulated charge at the time represented by the dataset.

The values were not blindly replaced with zero because "not recorded" and "zero charge" are not necessarily the same business meaning.

### Churn distribution

| Churn Status | Customers |
| ------------ | --------: |
| No           |     5,174 |
| Yes          |     1,869 |
| Total        |     7,043 |

Churn rate:

**26.54%**

### Important categorical observations

Contract:

* Month-to-month: 3,875
* One year: 1,473
* Two year: 1,695

Internet service:

* Fiber optic: 3,096
* DSL: 2,421
* No internet service: 1,526

Payment method:

* Electronic check: 2,365
* Mailed check: 1,612
* Bank transfer (automatic): 1,544
* Credit card (automatic): 1,522

### Numeric ranges

Tenure:

* Minimum: 0 months
* Maximum: 72 months

Monthly charges:

* Minimum: 18.25
* Maximum: 118.75

Total charges:

* Stored as text in the raw dataset

---

# 4. Script 02 — Data Cleaning

File:

`python/02_data_cleaning.py`

## Purpose

The cleaning script created the reusable analytical version of the dataset.

The raw dataset was preserved unchanged.

The cleaned dataset was saved as:

`data/processed/customer_churn_clean.csv`

## Cleaning and transformation steps

The script:

1. Loaded the raw dataset.
2. Converted `TotalCharges` to a numeric analytical field.
3. Preserved the distinction between recorded and unrecorded charges.
4. Created tenure bands.
5. Created a senior-citizen status label.
6. Created a binary churn flag.
7. Cleaned text fields.
8. Preserved meaningful business categories such as `No internet service`.
9. Saved the processed dataset.

## Derived fields

### TotalCharges_Clean

A numeric version of `TotalCharges`.

The 11 unrecorded values remain missing rather than being automatically converted to zero.

### TotalCharges_Status

Values:

* Recorded
* Not Recorded

### Tenure_Band

The following bands were created:

| Tenure Band  | Definition      |
| ------------ | --------------- |
| 0–6 Months   | 0 to 6 months   |
| 7–12 Months  | 7 to 12 months  |
| 13–24 Months | 13 to 24 months |
| 25–48 Months | 25 to 48 months |
| 49–72 Months | 49 to 72 months |

### SeniorCitizen_Status

Values:

* Senior Citizen
* Non-Senior Citizen

### Churn_Flag

Values:

* 1 = Churn
* 0 = No churn

---

# 5. Script 03 — Clean Data Validation

File:

`python/03_validate_clean_data.py`

## Purpose

The validation script confirmed that the cleaning process produced a reliable analytical dataset.

## Validation results

* Rows: 7,043
* Columns: 26
* Expected columns present: Yes
* Duplicate rows: 0
* Duplicate customer IDs: 0
* Recorded TotalCharges: 7,032
* Unrecorded TotalCharges: 11
* Numeric TotalCharges missing: 11
* Invalid churn flags: 0

Tenure bands:

| Tenure Band  | Customers |
| ------------ | --------: |
| 0–6 Months   |     1,481 |
| 7–12 Months  |       705 |
| 13–24 Months |     1,024 |
| 25–48 Months |     1,594 |
| 49–72 Months |     2,239 |

Senior-citizen status:

* Non-Senior Citizen: 5,901
* Senior Citizen: 1,142

The validation also confirmed that all 11 zero-tenure customers with missing `TotalCharges` had an unrecorded charge status.

**Validation result: PASSED**

---

# 6. Script 04 — Descriptive Churn Analysis

File:

`python/04_churn_analysis.py`

## Purpose

The descriptive analysis examined how churn varies across major customer characteristics.

The analysis covered:

* Overall churn
* Churn by contract
* Churn by tenure
* Average monthly charges by churn status

## Overall churn

| Metric          |  Value |
| --------------- | -----: |
| Total Customers |  7,043 |
| Churned         |  1,869 |
| Active          |  5,174 |
| Churn Rate      | 26.54% |

## Churn by contract

| Contract       | Customers | Churned | Churn Rate |
| -------------- | --------: | ------: | ---------: |
| Month-to-month |     3,875 |   1,655 |     42.71% |
| One year       |     1,473 |     166 |     11.27% |
| Two year       |     1,695 |      48 |      2.83% |

The observed churn rate differs substantially across contract types.

Month-to-month customers had an observed churn rate of 42.71%, while two-year customers had an observed churn rate of 2.83%.

This is an association in the dataset and should not be interpreted as proof that contract type independently causes churn.

## Churn by tenure

| Tenure Band  | Customers | Churned | Churn Rate |
| ------------ | --------: | ------: | ---------: |
| 0–6 Months   |     1,481 |     784 |     52.94% |
| 7–12 Months  |       705 |     253 |     35.89% |
| 13–24 Months |     1,024 |     294 |     28.71% |
| 25–48 Months |     1,594 |     325 |     20.39% |
| 49–72 Months |     2,239 |     213 |      9.51% |

The highest observed churn rate occurred among customers with 0–6 months of tenure.

The observed churn rate generally decreased as tenure increased.

## Monthly charges

| Churn Status | Average Monthly Charges |
| ------------ | ----------------------: |
| No           |                   61.27 |
| Yes          |                   74.44 |

Churned customers had an average monthly charge approximately 13.18 higher than active customers.

This is an observed difference and does not establish that higher monthly charges cause churn.

## Outputs

The script produced:

* `churn_by_contract.csv`
* `churn_by_tenure.csv`
* `monthly_charges_by_churn.csv`
* `churn_rate_by_contract.png`
* `churn_rate_by_tenure.png`
* `average_monthly_charges_by_churn.png`

---

# 7. Script 05 — Customer Segment Analysis

File:

`python/05_customer_segment_analysis.py`

## Purpose

The analysis moved beyond individual features and examined combinations of:

* Contract
* Tenure Band
* Internet Service
* Payment Method

A minimum segment size of 100 customers was used to avoid highlighting extremely small groups.

## Overall churn rate

26.54%

## Highest observed segment

The highest observed segment was:

* Contract: Month-to-month
* Tenure: 0–6 months
* Internet: Fiber optic
* Payment: Electronic check

Results:

* Customers: 440
* Churned: 332
* Churn rate: 75.45%
* Difference from overall churn: +48.92 percentage points

This is a high observed-risk segment in this dataset.

## Other high-churn segments

| Segment                                              | Customers | Churn Rate |
| ---------------------------------------------------- | --------: | ---------: |
| Month-to-month, 7–12, Fiber optic, Electronic check  |       191 |     61.26% |
| Month-to-month, 13–24, Fiber optic, Electronic check |       255 |     58.82% |
| Month-to-month, 0–6, DSL, Electronic check           |       209 |     56.94% |
| Month-to-month, 25–48, Fiber optic, Electronic check |       286 |     48.95% |
| Month-to-month, 0–6, DSL, Mailed check               |       192 |     45.31% |

Nine valid segments had churn rates above the overall 26.54% rate.

The results indicate that churn risk is not evenly distributed across the customer base.

## Important interpretation

These segment results identify **observed high-churn groups**.

They do not establish that the combination of these characteristics causes churn.

---

# 8. Script 06 — Segment Analysis Validation

File:

`python/06_validate_segment_analysis.py`

The validation confirmed:

* Full segment analysis rows: 20
* High-churn segment rows: 9
* Missing required columns: 0
* Invalid customer counts: 0
* Invalid churn counts: 0
* Churned customers greater than total customers: 0
* Invalid churn rates: 0
* Segments below minimum size: 0
* High-churn output incorrectly containing below-average segments: 0

**Validation result: PASSED**

---

# 9. Script 07 — Feature Association Analysis

File:

`python/07_feature_association_analysis.py`

## Purpose

This analysis systematically examined how categorical and numeric variables differ across churn outcomes.

Categorical features included:

* Gender
* Senior citizen status
* Partner
* Dependents
* Phone service
* Multiple lines
* Internet service
* Online security
* Online backup
* Device protection
* Tech support
* Streaming TV
* Streaming movies
* Contract
* Paperless billing
* Payment method
* Tenure band
* Total charges status

Numeric features included:

* Tenure
* Monthly charges
* Total charges

## Largest categorical churn-rate ranges

The largest observed differences across categories were found for:

| Feature           | Churn Rate Range |
| ----------------- | ---------------: |
| Tenure Band       |         43.42 pp |
| Contract          |         39.88 pp |
| Internet Service  |         34.49 pp |
| Online Security   |         34.36 pp |
| Tech Support      |         34.23 pp |
| Online Backup     |         32.52 pp |
| Device Protection |         31.72 pp |
| Payment Method    |         30.04 pp |

Gender had a much smaller observed range:

0.76 percentage points.

Phone service also had a relatively small range:

1.78 percentage points.

## Numeric comparisons

| Feature         | Churned Average | Active Average | Difference |
| --------------- | --------------: | -------------: | ---------: |
| Tenure          |           17.98 |          37.57 |     -19.59 |
| Monthly Charges |           74.44 |          61.27 |     +13.18 |
| Total Charges   |        1,531.80 |       2,555.34 |  -1,023.55 |

The lower total-charge average among churned customers is strongly related to the lower tenure observed among churned customers and should not be interpreted independently.

---

# 10. Script 08 — Statistical Feature Association

File:

`python/08_statistical_feature_association.py`

## Purpose

The previous analysis showed observed differences. This stage added statistical association measures.

For categorical variables, Cramér's V was used.

For numeric variables against the binary churn target, point-biserial correlation was used.

These measures quantify association rather than causation.

## Cramér's V results

| Feature              | Cramér's V |
| -------------------- | ---------: |
| Contract             |     0.4101 |
| Tenure_Band          |     0.3629 |
| OnlineSecurity       |     0.3474 |
| TechSupport          |     0.3429 |
| InternetService      |     0.3225 |
| PaymentMethod        |     0.3034 |
| OnlineBackup         |     0.2923 |
| DeviceProtection     |     0.2816 |
| StreamingMovies      |     0.2310 |
| StreamingTV          |     0.2305 |
| PaperlessBilling     |     0.1915 |
| Dependents           |     0.1639 |
| SeniorCitizen_Status |     0.1505 |
| Partner              |     0.1501 |
| MultipleLines        |     0.0401 |
| TotalCharges_Status  |     0.0197 |
| PhoneService         |     0.0114 |
| Gender               |     0.0083 |

The largest measured categorical association was Contract at 0.4101.

## Numeric association

| Feature            | Point-Biserial Correlation |
| ------------------ | -------------------------: |
| Tenure             |                    -0.3522 |
| TotalCharges_Clean |                    -0.1995 |
| MonthlyCharges     |                     0.1934 |

The negative tenure correlation means that higher tenure values are associated with lower churn flags in this dataset.

The positive MonthlyCharges correlation indicates that higher monthly charges are associated with churn.

All three reported p-values were below the displayed precision threshold.

These statistical associations should still be interpreted as relationships in the observed dataset, not causal effects.

---

# 11. Script 09 — Baseline Churn Prediction Model

File:

`python/09_churn_prediction_model.py`

## Purpose

The baseline model tested whether customer characteristics could be used to predict churn.

A Logistic Regression model was selected because it provides:

* A classification framework
* Probability estimates
* Interpretable coefficients
* A useful baseline for structured tabular data

## Predictors

Numeric variables:

* SeniorCitizen
* tenure
* MonthlyCharges
* TotalCharges_Clean

Categorical variables:

* gender
* Partner
* Dependents
* PhoneService
* MultipleLines
* InternetService
* OnlineSecurity
* OnlineBackup
* DeviceProtection
* TechSupport
* StreamingTV
* StreamingMovies
* Contract
* PaperlessBilling
* PaymentMethod

The following were excluded from modeling:

* customerID
* Churn
* Churn_Flag
* Tenure_Band
* SeniorCitizen_Status
* TotalCharges_Status

## Train/test split

* Total rows: 7,043
* Training rows: 5,634
* Testing rows: 1,409
* Training churn rate: 26.54%
* Testing churn rate: 26.54%

The split used stratification so that the churn distribution remained consistent.

## Baseline performance

| Metric    | Result |
| --------- | -----: |
| Accuracy  | 0.8055 |
| Precision | 0.6572 |
| Recall    | 0.5588 |
| F1 Score  | 0.6040 |
| ROC-AUC   | 0.8419 |

## Confusion matrix

|            | Predicted No | Predicted Yes |
| ---------- | -----------: | ------------: |
| Actual No  |          926 |           109 |
| Actual Yes |          165 |           209 |

Therefore:

* True Negatives: 926
* False Positives: 109
* False Negatives: 165
* True Positives: 209

## Interpretation

The model correctly identifies approximately 56% of actual churners at the default 0.50 classification threshold.

The ROC-AUC of 0.8419 indicates useful discrimination between churn and non-churn customers on this test set.

Accuracy alone was not treated as sufficient because the churn target is imbalanced.

---

# 12. Script 10 — Refined Churn Model

File:

`python/10_refined_churn_model.py`

## Purpose

The baseline model contained both `tenure` and `TotalCharges_Clean`.

Because total charges accumulate over time and are therefore related to tenure, the analysis tested whether removing `TotalCharges_Clean` would simplify the model without materially reducing predictive performance.

## Results

| Metric    | Baseline | Refined |
| --------- | -------: | ------: |
| Accuracy  |   0.8055 |  0.7977 |
| Precision |   0.6572 |  0.6378 |
| Recall    |   0.5588 |  0.5508 |
| F1        |   0.6040 |  0.5911 |
| ROC-AUC   |   0.8419 |  0.8391 |

Removing `TotalCharges_Clean` resulted in a small reduction across the measured performance metrics.

Therefore, the experiment did not demonstrate a performance improvement from removing the variable.

---

# 13. Script 11 — Initial Model Comparison

File:

`python/11_compare_churn_models.py`

The baseline and refined models were compared directly.

Changes from baseline to refined model:

* Accuracy: -0.78 percentage points
* Precision: -1.94 percentage points
* Recall: -0.80 percentage points
* F1: -1.29 percentage points
* ROC-AUC: -0.28 percentage points

The confusion matrix also changed:

| Metric         | Baseline | Refined |
| -------------- | -------: | ------: |
| True Negative  |      926 |     918 |
| False Positive |      109 |     117 |
| False Negative |      165 |     168 |
| True Positive  |      209 |     206 |

The refined model used one fewer predictor.

The experiment demonstrated that reducing feature count did not automatically improve model performance.

---

# 14. Script 12 — Service Category Refinement

File:

`python/12_service_category_refinement.py`

## Purpose

Several service variables contained:

`No internet service`

This value represents a meaningful business state rather than generic missing data.

For interpretability, the following values were relabeled:

`No internet service` → `Not Applicable`

for:

* OnlineSecurity
* OnlineBackup
* DeviceProtection
* TechSupport
* StreamingTV
* StreamingMovies

## Result

The model produced exactly the same performance as the refined model:

| Metric    | Result |
| --------- | -----: |
| Accuracy  | 0.7977 |
| Precision | 0.6378 |
| Recall    | 0.5508 |
| F1        | 0.5911 |
| ROC-AUC   | 0.8391 |

This was expected because the transformation changed the category label but not the underlying information.

Therefore, this experiment is considered an **interpretability/data-labeling refinement**, not a predictive performance improvement.

---

# 15. Script 13 — Reduced Service Model

File:

`python/13_reduced_service_model.py`

## Purpose

The next experiment tested whether the seven detailed internet-service variables added predictive information beyond the broader `InternetService` variable.

The following were removed:

* OnlineSecurity
* OnlineBackup
* DeviceProtection
* TechSupport
* StreamingTV
* StreamingMovies

The model retained:

* SeniorCitizen
* tenure
* MonthlyCharges
* gender
* Partner
* Dependents
* PhoneService
* MultipleLines
* InternetService
* Contract
* PaperlessBilling
* PaymentMethod

## Results

| Metric    | Model 2 | Reduced Service Model |
| --------- | ------: | --------------------: |
| Accuracy  |  0.7977 |                0.7906 |
| Precision |  0.6378 |                0.6246 |
| Recall    |  0.5508 |                0.5294 |
| F1        |  0.5911 |                0.5731 |
| ROC-AUC   |  0.8391 |                0.8359 |

Compared with Model 2:

* Accuracy: -0.71 pp
* Precision: -1.32 pp
* Recall: -2.14 pp
* F1: -1.80 pp
* ROC-AUC: -0.32 pp

The reduction in performance indicates that the detailed service variables collectively contain predictive information beyond the broader InternetService variable in this model.

---

# 16. Script 14 — Three-Model Comparison

File:

`python/14_compare_churn_models.py`

Three materially different specifications were compared:

1. Baseline model
2. Refined model without TotalCharges_Clean
3. Reduced-service model

The category-label experiment was not treated as a separate predictive model because it produced identical results.

## Performance comparison

| Metric    | Baseline | Refined | Reduced Service |
| --------- | -------: | ------: | --------------: |
| Accuracy  |   0.8055 |  0.7977 |          0.7906 |
| Precision |   0.6572 |  0.6378 |          0.6246 |
| Recall    |   0.5588 |  0.5508 |          0.5294 |
| F1        |   0.6040 |  0.5911 |          0.5731 |
| ROC-AUC   |   0.8419 |  0.8391 |          0.8359 |

## Confusion matrix comparison

| Metric         | Baseline | Refined | Reduced Service |
| -------------- | -------: | ------: | --------------: |
| True Negative  |      926 |     918 |             916 |
| False Positive |      109 |     117 |             119 |
| False Negative |      165 |     168 |             176 |
| True Positive  |      209 |     206 |             198 |

## Model complexity

| Model           | Predictors | Main Change                     |
| --------------- | ---------: | ------------------------------- |
| Baseline        |         19 | Reference model                 |
| Refined         |         18 | Removed TotalCharges_Clean      |
| Reduced Service |         12 | Removed seven service variables |

## Conclusion from model comparison

The feature-removal experiments did not improve predictive performance on the fixed test set.

Removing `TotalCharges_Clean` caused a small performance reduction.

Removing the seven detailed service variables caused a larger performance reduction.

This provides evidence that the detailed service variables collectively contribute predictive information in this modeling setup.

The baseline model was therefore retained as the reference model for threshold analysis.

---

# 17. Script 15 — Classification Threshold Analysis

File:

`python/15_threshold_analysis.py`

## Purpose

The Logistic Regression model produces a probability of churn.

The default classification threshold is 0.50, but the threshold can be changed depending on the operational purpose.

Threshold analysis was therefore performed using:

* 0.30
* 0.35
* 0.40
* 0.45
* 0.50
* 0.55
* 0.60
* 0.65
* 0.70

The same baseline model and the same train/test split were retained.

ROC-AUC remained:

**0.8419**

ROC-AUC does not change when the classification threshold changes because it evaluates the ranking of predicted probabilities rather than one particular classification cutoff.

## Threshold results

| Threshold | Accuracy | Precision | Recall |     F1 |
| --------: | -------: | --------: | -----: | -----: |
|      0.30 |   0.7495 |    0.5193 | 0.7540 | 0.6150 |
|      0.35 |   0.7651 |    0.5443 | 0.7059 | 0.6147 |
|      0.40 |   0.7779 |    0.5695 | 0.6684 | 0.6150 |
|      0.45 |   0.7892 |    0.6005 | 0.6150 | 0.6077 |
|      0.50 |   0.8055 |    0.6572 | 0.5588 | 0.6040 |
|      0.55 |   0.7991 |    0.6784 | 0.4626 | 0.5501 |
|      0.60 |   0.7991 |    0.7177 | 0.4011 | 0.5146 |
|      0.65 |   0.7885 |    0.7468 | 0.3075 | 0.4356 |
|      0.70 |   0.7658 |    0.7391 | 0.1818 | 0.2918 |

## Key observations

Lower thresholds:

* Flag more customers.
* Increase recall.
* Reduce the number of missed churners.
* Also increase false positives.

Higher thresholds:

* Flag fewer customers.
* Increase precision.
* Reduce unnecessary contacts.
* Increase the number of missed churners.

The highest observed F1 score was 0.6150 at both 0.30 and 0.40.

However, F1 alone was not used to declare an operational threshold because the appropriate threshold depends on the business's retention capacity and the relative consequences of false positives and false negatives.

---

# 18. Script 16 — Threshold Business Impact Analysis

File:

`python/16_threshold_business_impact.py`

## Purpose

The threshold analysis was translated into business-oriented metrics.

The analysis focused on:

* Customers flagged
* Churners captured
* Churners missed
* Unnecessary contacts
* Capture rate
* Miss rate
* Contact efficiency

The test set contains:

**374 actual churners**

## Business impact results

| Threshold | Customers Flagged | Churners Captured | Churners Missed | Unnecessary Contacts | Capture Rate |
| --------: | ----------------: | ----------------: | --------------: | -------------------: | -----------: |
|      0.30 |               543 |               282 |              92 |                  261 |       75.40% |
|      0.35 |               485 |               264 |             110 |                  221 |       70.59% |
|      0.40 |               439 |               250 |             124 |                  189 |       66.84% |
|      0.45 |               383 |               230 |             144 |                  153 |       61.50% |
|      0.50 |               318 |               209 |             165 |                  109 |       55.88% |
|      0.55 |               255 |               173 |             201 |                   82 |       46.26% |
|      0.60 |               209 |               150 |             224 |                   59 |       40.11% |
|      0.65 |               154 |               115 |             259 |                   39 |       30.75% |
|      0.70 |                92 |                68 |             306 |                   24 |       18.18% |

## Operational interpretation

At a threshold of 0.30:

* 543 customers would be flagged.
* 282 actual churners would be captured.
* 92 actual churners would be missed.
* 261 flagged customers would not ultimately churn.

At the default threshold of 0.50:

* 318 customers would be flagged.
* 209 actual churners would be captured.
* 165 actual churners would be missed.
* 109 flagged customers would not ultimately churn.

At a threshold of 0.65:

* 154 customers would be flagged.
* 115 actual churners would be captured.
* 259 actual churners would be missed.
* 39 flagged customers would not ultimately churn.

These results demonstrate that threshold selection is an operational decision involving a trade-off between intervention capacity and the cost of missed churners.

No universal threshold was selected from the dataset alone.

---

# 19. Major Findings From the Python Analysis

The complete Python analysis produced several consistent findings.

## Finding 1 — Churn is concentrated in particular customer groups

The overall churn rate is 26.54%, but observed churn rates vary substantially across customer characteristics and combinations of characteristics.

For example, the highest observed segment examined had a 75.45% churn rate.

---

## Finding 2 — Contract type is strongly associated with churn

Month-to-month customers had an observed churn rate of 42.71%.

One-year customers had an observed churn rate of 11.27%.

Two-year customers had an observed churn rate of 2.83%.

Contract also had the highest Cramér's V among the categorical variables analyzed:

**0.4101**

---

## Finding 3 — Early-tenure customers show substantially higher observed churn

Customers with 0–6 months of tenure had a 52.94% observed churn rate.

Customers with 49–72 months had a 9.51% observed churn rate.

Tenure had a point-biserial correlation of:

**-0.3522**

with the churn flag.

---

## Finding 4 — Several service-related variables are associated with churn

Online Security, Tech Support, Internet Service, Online Backup, and Device Protection all showed meaningful observed differences across churn groups.

The statistical association analysis also showed relatively high Cramér's V values for these variables.

---

## Finding 5 — Customer charges differ between churn groups

Churned customers had:

* Higher average monthly charges
* Lower average tenure
* Lower average total recorded charges

The lower total charges among churned customers should be interpreted in the context of their shorter tenure.

---

## Finding 6 — Gender shows very little observed association with churn

Gender had:

* Churn-rate range: 0.76 percentage points
* Cramér's V: 0.0083

This indicates very little observed association between gender and churn in this dataset.

---

## Finding 7 — The baseline predictive model provides useful discrimination

The baseline Logistic Regression model achieved:

* Accuracy: 80.55%
* Precision: 65.72%
* Recall: 55.88%
* F1: 0.6040
* ROC-AUC: 0.8419

The model therefore provides useful predictive separation, while still missing a substantial proportion of actual churners at the default 0.50 threshold.

---

## Finding 8 — Feature removal did not improve performance

Removing `TotalCharges_Clean` slightly reduced performance.

Removing seven detailed service variables produced a larger reduction.

This suggests that simplifying the model by removing these variables did not provide a predictive advantage under the current modeling setup.

---

## Finding 9 — Threshold selection materially changes operational outcomes

The same model can identify very different numbers of potential churners depending on the classification threshold.

At 0.30:

* 543 customers flagged
* 282 churners captured

At 0.70:

* 92 customers flagged
* 68 churners captured

Therefore, model deployment should consider not only predictive performance but also the organization's ability to act on predictions.

---

# 20. Analytical Limitations

The Python analysis has several important limitations.

### Association is not causation

Observed relationships between features and churn do not prove that those features cause churn.

### Dataset limitations

The analysis is based on the available Telco Customer Churn dataset and its historical observations.

Results should not automatically be assumed to represent another telecom company or a different customer population.

### Single train/test split

The predictive models used a fixed stratified 80/20 train/test split with:

`random_state=42`

This provides a reproducible comparison, but it does not measure performance across multiple independent samples.

### Threshold analysis

The threshold results describe the current test set.

An operational threshold should ideally be validated against business intervention capacity and the actual cost of:

* Missing a potential churner
* Contacting a customer who would not churn

### Model interpretation

Logistic Regression coefficients represent conditional model relationships. They should not be interpreted as causal effects.

---

# 21. Python Analysis Outputs

The Python stage generated the following analytical outputs.

## Descriptive analysis

```text
data/analysis_outputs/
├── churn_by_contract.csv
├── churn_by_tenure.csv
├── monthly_charges_by_churn.csv
├── churn_rate_by_contract.png
├── churn_rate_by_tenure.png
└── average_monthly_charges_by_churn.png
```

## Customer segmentation

```text
data/analysis_outputs/
├── customer_segment_churn_analysis.csv
└── high_churn_customer_segments.csv
```

## Feature association

```text
data/analysis_outputs/
├── feature_association_analysis.csv
├── numeric_feature_churn_comparison.csv
└── statistical_feature_association.csv
```

## Predictive modeling

```text
data/analysis_outputs/
├── model_performance.csv
├── logistic_regression_coefficients.csv
├── refined_model_performance.csv
├── refined_logistic_regression_coefficients.csv
├── service_refined_model_performance.csv
├── service_refined_logistic_regression_coefficients.csv
├── reduced_service_model_performance.csv
├── reduced_service_logistic_regression_coefficients.csv
├── three_model_comparison.csv
├── three_model_confusion_matrix_comparison.csv
└── three_model_complexity_comparison.csv
```

## Threshold analysis

```text
data/analysis_outputs/
├── churn_threshold_analysis.csv
└── churn_threshold_business_impact.csv
```

---

# 22. Reproducibility

The Python workflow was designed so that the analysis can be repeated without manually modifying the raw dataset.

The general workflow is:

```text
Raw CSV
   ↓
01_data_profiling.py
   ↓
02_data_cleaning.py
   ↓
customer_churn_clean.csv
   ↓
03_validate_clean_data.py
   ↓
Descriptive Analysis
   ↓
Segment Analysis
   ↓
Association Analysis
   ↓
Statistical Analysis
   ↓
Predictive Modeling
   ↓
Model Comparison
   ↓
Threshold Analysis
   ↓
Business Impact Analysis
```

If additional valid customer records are added to the raw dataset, the cleaning and analytical scripts can be rerun to regenerate the processed dataset and analytical outputs.

This supports the project's goal of creating a refreshable and maintainable analytics workflow.

---

# 23. Overall Python Stage Conclusion

The Python analysis established a complete analytical foundation for the customer churn project.

The analysis showed that churn is not evenly distributed across the customer base. Contract type, tenure, internet service, several service features, payment method, and other customer characteristics show varying levels of association with churn.

The predictive analysis demonstrated that a Logistic Regression model can provide useful churn discrimination, achieving a ROC-AUC of 0.8419 on the fixed test set.

Feature-removal experiments did not improve predictive performance, so the baseline model was retained as the reference specification.

Threshold analysis then demonstrated that the same predictive model can support different operational strategies. Lower thresholds identify more potential churners but require contacting more customers, while higher thresholds produce smaller and more selective intervention lists but miss more actual churners.

The appropriate operational threshold therefore depends on business capacity, intervention cost, and the relative importance assigned to missed churners versus unnecessary interventions.

The Python stage is now complete enough to serve as the analytical foundation for the Power BI reporting layer.
