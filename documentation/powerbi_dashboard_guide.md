# Power BI Dashboard Guide

## 1. Introduction

The Power BI stage of the Customer Churn Analytics project transforms the results of the data preparation, SQL analysis, and Python analysis stages into an interactive business intelligence report.

The purpose of the report is to help stakeholders understand customer churn, identify customer groups with elevated churn risk, evaluate predictive model performance, and translate analytical findings into practical customer retention recommendations.

The report is organized into six analytical pages:

1. Executive Overview
2. Churn Drivers
3. High-Risk Segments
4. Predictive Intelligence
5. Retention Strategy
6. Insight & Recommendation

This guide documents the existing six-page report baseline. A separate redesign using Power BI HTML Content is planned. The redesign should be documented as implemented only after the new report has been built and validated.

## 2. Dashboard Objectives

The Power BI report is designed to achieve the following objectives:

- Present the overall customer churn situation.
- Communicate important business metrics clearly.
- Identify customer characteristics associated with churn.
- Compare churn behavior across customer segments.
- Highlight combinations of characteristics associated with elevated churn.
- Present predictive model performance in a business-friendly format.
- Translate analytical findings into retention recommendations.
- Support evidence-based decisions through interactive reporting.

The report connects descriptive analytics, diagnostic analysis, predictive analytics, and business recommendations.

## 3. Data and Analytical Foundation

The dashboard is supported by the cleaned customer churn dataset and analytical outputs developed throughout the project.

### 3.1 Source Dataset

The original dataset is the IBM Telco Customer Churn dataset.

| Attribute | Description |
|---|---|
| Original records | 7,043 customers |
| Original columns | 21 |
| Processed records | 7,043 customers |
| Processed columns | 26 |
| Target variable | Churn |
| Customer identifier | customerID |
| Primary business question | Which customers are more likely to leave the company? |

The processed dataset contains the original customer information alongside additional analytical fields created during data preparation.

### 3.2 Important Derived Fields

The following fields support analysis and reporting:

| Field | Purpose |
|---|---|
| TotalCharges_Clean | Numeric version of total charges |
| TotalCharges_Status | Identifies the status of total charges data |
| Tenure_Band | Groups customers according to their tenure |
| SeniorCitizen_Status | Provides readable senior citizen categories |
| Churn_Flag | Numeric representation of the churn outcome |

These fields support consistent grouping, aggregation, and analytical interpretation.

### 3.3 Key Analytical Results

The following project results provide important context for the report:

| Metric | Result |
|---|---:|
| Total customers | 7,043 |
| Churned customers | 1,869 |
| Active customers | 5,174 |
| Overall churn rate | 26.54% |
| Month-to-month churn rate | 42.71% |
| One-year contract churn rate | 11.27% |
| Two-year contract churn rate | 2.83% |
| Churn rate for customers with 0–6 months tenure | 52.94% |
| Churn rate for customers with 49–72 months tenure | 9.51% |

These figures are analytical findings from the project and should be used as validation references when checking the corresponding Power BI results.

## 4. Dashboard Structure

### 4.1 Executive Overview

**Purpose**

The Executive Overview provides a high-level summary of customer churn and the overall customer base.

It is intended for business stakeholders who need to understand the company's churn situation without examining every analytical detail.

**Main analytical questions**

- How many customers are represented in the dataset?
- How many customers have churned?
- How many customers remain active?
- What proportion of customers have churned?
- What are the most important patterns emerging from the analysis?

**Important metrics**

- Total Customers
- Churned Customers
- Active Customers
- Overall Churn Rate

**Interpretation**

The overall churn rate of 26.54% indicates that approximately one in four customers in the dataset has left the company.

The executive page should make this result immediately understandable and provide context for the more detailed analyses on subsequent pages.

**Business value**

This page establishes the scale of the churn problem and helps management understand why customer retention deserves attention.

### 4.2 Churn Drivers

**Purpose**

The Churn Drivers page investigates how customer characteristics, service subscriptions, and payment arrangements relate to customer churn.

**Main analytical questions**

- How does churn differ across contract types?
- Which payment methods are associated with higher churn?
- How does churn vary by internet service?
- What patterns exist across customer support and security services?
- How do customer characteristics relate to churn?

**Areas of analysis**

The analysis considers variables such as:

- Contract
- InternetService
- PaymentMethod
- OnlineSecurity
- TechSupport
- OnlineBackup
- DeviceProtection
- Partner
- Dependents
- SeniorCitizen_Status

**Important reporting consideration**

This page focuses on explaining churn patterns across customer attributes. It should not repeat the overall Churn Rate KPI from the Executive Overview as a headline KPI.

The page should emphasize comparisons between categories and the differences in their churn behavior.

**Interpretation**

Contract type is one of the strongest categorical associations with churn in the project.

The observed churn rates are:

| Contract Type | Churn Rate |
|---|---:|
| Month-to-month | 42.71% |
| One year | 11.27% |
| Two year | 2.83% |

These results indicate that customers on month-to-month contracts have substantially higher observed churn than customers on longer contracts.

This is an association, not proof that contract duration alone causes customers to leave.

**Business value**

The page helps management identify customer attributes that deserve further investigation and may inform retention initiatives.

### 4.3 High-Risk Segments

**Purpose**

The High-Risk Segments page focuses on combinations of customer characteristics associated with elevated churn.

Rather than considering one variable at a time, this page supports a more detailed understanding of customer groups.

**Main analytical questions**

- Which customer segments have the highest observed churn?
- Which combinations of customer characteristics appear particularly risky?
- How does tenure affect churn within different groups?
- Which segments should be prioritized for retention attention?

**Important segmentation dimensions**

- Contract type
- Tenure band
- Internet service
- Payment method
- Customer service subscriptions
- Other relevant customer characteristics

**High-risk segment identified**

One of the project's important findings is the combination of:

- Month-to-month contract
- 0–6 months tenure
- Fiber optic internet service
- Electronic check payment method

The Python segmentation analysis reported a churn rate of 75.45% for this segment.

This finding should be interpreted alongside the segment's customer count. A high churn percentage based on a small number of customers may require more caution than a similarly high percentage supported by a large customer population.

**Business value**

The page helps identify customer groups that may benefit from more targeted retention attention.

### 4.4 Predictive Intelligence

**Purpose**

The Predictive Intelligence page presents the machine learning stage of the project.

It communicates how well the predictive models identify customers who are likely to churn and explains the implications of model performance.

**Main analytical questions**

- How accurately can the model identify churn?
- How many actual churners can the model detect?
- How reliable are its positive predictions?
- What is the balance between identifying churners and avoiding unnecessary retention interventions?
- How does changing the classification threshold affect business decisions?

**Baseline Logistic Regression results**

The project's baseline Logistic Regression model produced the following results:

| Evaluation Metric | Result |
|---|---:|
| Accuracy | 80.55% |
| Precision | 65.72% |
| Recall | 55.88% |
| F1-score | 0.6040 |
| ROC-AUC | 0.8419 |

**Metric interpretation**

- **Accuracy:** The proportion of all predictions that were correct.
- **Precision:** The proportion of customers predicted to churn who actually churned.
- **Recall:** The proportion of actual churners correctly identified by the model.
- **F1-score:** The harmonic balance between precision and recall.
- **ROC-AUC:** The model's ability to distinguish between customers who churn and those who remain.

**Classification threshold**

The classification threshold determines the probability at which a customer is classified as a predicted churner.

Changing the threshold creates a trade-off between identifying more actual churners and limiting the number of customers flagged for intervention.

Two examples from the project's threshold analysis are:

| Threshold | Customers Flagged | Actual Churners Captured |
|---|---:|---:|
| 0.30 | 543 | 282 |
| 0.70 | 92 | 68 |

The lower threshold identifies more customers but may also increase the number of customers who do not eventually churn.

The higher threshold produces a smaller intervention group but misses more actual churners.

**Important interpretation**

Predictive results should support business decisions rather than replace human judgment.

A model prediction is an estimate of risk, not confirmation that a customer will leave.

**Business value**

This page demonstrates how predictive analytics can help prioritize customer retention efforts and allocate intervention resources.

### 4.5 Retention Strategy

**Purpose**

The Retention Strategy page translates the project's analytical findings into practical business recommendations.

The objective is to move beyond identifying churn patterns and explain how a business could respond to them.

**Recommended retention priorities**

**1. Improve early customer engagement**

Customers within the first six months of service show substantially higher churn than long-tenure customers.

Recommended actions:

- Introduce a structured customer onboarding process.
- Contact new customers after activation.
- Identify early service problems.
- Provide clear guidance on available services.
- Monitor early customer satisfaction.

**2. Encourage longer-term customer relationships**

Month-to-month customers have a substantially higher observed churn rate than customers on one-year and two-year contracts.

Recommended actions:

- Communicate the benefits of longer-term plans.
- Offer suitable contract incentives.
- Explain contract options clearly.
- Identify customers who may benefit from a different plan.

**3. Review payment experience**

Electronic check payment is one of the payment categories examined in the project's churn analysis.

Recommended actions:

- Review payment-related complaints.
- Improve payment communication.
- Make alternative payment methods easy to understand.
- Monitor payment issues during the first months of service.

**4. Improve service adoption and support**

The project identified OnlineSecurity and TechSupport as important categorical variables associated with churn.

Recommended actions:

- Explain available security and support services.
- Identify customers who may need technical assistance.
- Improve awareness of relevant service features.
- Monitor recurring support problems.

**5. Prioritize high-risk customer segments**

The identified high-risk segment provides an opportunity for more focused retention attention.

Recommended actions:

- Create targeted engagement campaigns.
- Prioritize early-tenure customers with elevated risk.
- Monitor retention campaign outcomes.
- Compare intervention costs with the value of retained customers.

**Business value**

This page connects analytical evidence to actions that a telecommunications business could investigate or implement.

The recommendations are proposed responses to observed patterns. Their effectiveness must be measured through subsequent business testing.

### 4.6 Insight & Recommendation

**Purpose**

The Insight & Recommendation page brings together the major findings from the project and presents the conclusions in a decision-oriented format.

**Key insights**

1. Overall customer churn is 26.54%.
2. Month-to-month customers have substantially higher churn than customers on longer contracts.
3. Customers with shorter tenure show elevated churn.
4. Contract, tenure, internet service, and payment method are important categorical variables in the association analysis.
5. The identified high-risk customer segment has a reported churn rate of 75.45%.
6. The baseline Logistic Regression model achieved an ROC-AUC of 0.8419.
7. Classification threshold selection affects how many customers are flagged for retention intervention.

**Recommended business priorities**

- Improve onboarding and early customer engagement.
- Investigate the experience of month-to-month customers.
- Prioritize high-risk customer groups.
- Improve awareness and adoption of relevant support services.
- Evaluate payment-related customer experience.
- Use predictive risk scores to support targeted retention activities.
- Measure the actual results of retention interventions.

**Business value**

This page provides a concise conclusion to the analytical report and connects the project's technical findings to business decision-making.

## 5. Key Metric Definitions

The following definitions provide a consistent business interpretation of the metrics used throughout the project.

These are semantic definitions. The exact DAX measure names should be taken from the measures implemented in the Power BI model rather than assumed from the labels in this guide.

### 5.1 Total Customers

The number of distinct customers included in the current reporting context.

### 5.2 Churned Customers

The number of distinct customers whose churn status is Yes.

### 5.3 Active Customers

The number of distinct customers whose churn status is No.

### 5.4 Overall Churn Rate

The percentage of customers who have churned.

\[
\text{Churn Rate} =
\frac{\text{Churned Customers}}{\text{Total Customers}}
\times 100
\]

For the complete project dataset:

\[
\frac{1,869}{7,043}\times100 = 26.54\%
\]

### 5.5 Segment Churn Rate

The percentage of customers who have churned within a selected customer segment.

\[
\text{Segment Churn Rate} =
\frac{\text{Churned Customers in Segment}}
{\text{Total Customers in Segment}}
\times 100
\]

The denominator should be the customer count within the same segment and filter context.

### 5.6 Average Monthly Charges

The average monthly charge across customers included in the current reporting context.

This metric can help compare the monthly billing characteristics of different customer groups.

### 5.7 Total Charges

The sum of valid cleaned total charges across the selected customers.

Missing cleaned total charges should remain missing rather than being automatically interpreted as zero.

### 5.8 Predictive Model Metrics

The Predictive Intelligence page may present model evaluation metrics such as accuracy, precision, recall, F1-score, and ROC-AUC.

These metrics describe different aspects of model performance and should not be treated as interchangeable.

## 6. Report Interaction and Filter Context

Power BI allows report users to interact with supported visuals, filters, and slicers.

The interpretation of a displayed metric depends on the filters and selections currently applied.

### 6.1 Filter Context

When a report filter or slicer is applied, measures may recalculate using only the records that remain in the selected context.

For example, a churn rate displayed after selecting a contract category should represent that category if the underlying measure respects the filter context.

### 6.2 Visual Interactions

Where visual interactions are enabled, selecting a category or data point may filter or highlight related visuals.

Users should consider these interactions when interpreting results.

### 6.3 Reading Report Results

Recommended reporting practices include:

- Check the active filters before interpreting a result.
- Compare percentages alongside customer counts.
- Avoid comparing percentages calculated from very different population sizes without considering volume.
- Distinguish actual churn from predicted churn.
- Treat predictive risk as an estimate rather than a confirmed outcome.
- Confirm whether a result represents the entire dataset or a filtered subset.

This guide does not assume that a particular slicer, filter, or navigation control exists unless it has been confirmed in the actual PBIX report.

## 7. Design and Presentation Principles

The report should communicate analytical findings clearly and consistently.

The following principles guide its design and future improvements.

### 7.1 Visual Hierarchy

Important business metrics should be easy to identify.

The Executive Overview should communicate the overall churn situation before users move into detailed analysis.

### 7.2 Consistent Formatting

Use consistent formatting for:

- Percentages
- Customer counts
- Monetary values
- Tenure periods
- Model evaluation metrics

Churn rates should use percentage formatting with consistent decimal precision.

### 7.3 Clear Titles and Labels

Every visual should have a meaningful title that explains what is being compared or measured.

Avoid unexplained abbreviations and technical labels where business-friendly alternatives are available.

### 7.4 Appropriate Comparisons

Comparisons should use consistent categories and definitions.

For example, contract churn comparisons should use the same churn-rate calculation across all contract categories.

### 7.5 Accessible Presentation

Use sufficient contrast, readable labels, clear legends, and a consistent visual language.

Color should support interpretation rather than serve as the only way to communicate a result.

### 7.6 Evidence-Based Conclusions

Every major recommendation should be traceable to an analytical finding.

The report should distinguish observed relationships, predictive estimates, and proposed business actions.

## 8. Validation and Quality Checks

Before publishing or presenting the Power BI report, the following checks should be performed.

| Validation Area | Expected Check |
|---|---|
| Customer count | 7,043 customers in the complete dataset |
| Churned customers | 1,869 |
| Active customers | 5,174 |
| Overall churn rate | 26.54% |
| Month-to-month churn rate | 42.71% |
| One-year contract churn rate | 11.27% |
| Two-year contract churn rate | 2.83% |
| Tenure segmentation | Matches the processed dataset |
| Missing total charges | 11 records remain missing |
| Filter behavior | Measures respond appropriately to supported filters |
| Percentage formatting | Rates are displayed consistently |
| Predictive metrics | Match the validated Python model evaluation outputs |

The expected values above refer to the complete dataset without additional filters.

If a displayed result differs, investigate the data source, filter context, relationships, aggregation logic, and measure definitions before changing the expected value.

## 9. Limitations and Interpretation Considerations

The following limitations should be considered when using the report.

### 9.1 Observational Dataset

The dataset describes customer characteristics and churn outcomes. It does not establish that a particular customer attribute directly causes churn.

### 9.2 Dataset Scope

The analysis is based on the supplied IBM Telco Customer Churn dataset. Results should not automatically be generalized to every telecommunications company or customer population.

### 9.3 Missing Total Charges

Eleven records have missing cleaned total charges. These values were not automatically replaced with zero.

### 9.4 Predictive Model Limitations

Model performance is based on the project's evaluation data and methodology.

Predictive performance may change when the model is applied to new customer populations or future periods.

### 9.5 Threshold Trade-offs

A classification threshold affects the number of customers identified for intervention.

The most suitable threshold depends on business capacity, intervention costs, and the relative cost of missing an actual churner.

### 9.6 Recommendations Require Testing

Retention recommendations are based on observed analytical patterns. Their actual business impact should be evaluated through controlled experiments or structured performance monitoring where practical.

## 10. Planned HTML Content Dashboard Redesign

A redesigned Power BI report using HTML Content is planned as a future improvement to the current dashboard.

The intention is to create a more advanced and cohesive reporting experience while reducing the need to build every visual individually using traditional Power BI visual configuration.

The planned redesign may include:

- Custom HTML-based KPI cards.
- More advanced analytical layouts.
- Improved visual hierarchy.
- Interactive customer segment summaries.
- More polished predictive analytics presentation.
- Consistent styling across report pages.
- More efficient reuse of HTML and CSS components.

**Implementation status:** Planned. This section describes the intended direction and does not claim that the HTML Content redesign has already been implemented.

After the redesigned report is completed, this guide should be updated to document:

1. The final page structure.
2. The actual HTML Content components used.
3. The DAX measures connected to each component.
4. The data fields and filter context used.
5. Interactive behavior and navigation.
6. Performance and refresh considerations.
7. Validation results for the redesigned report.

The redesigned report should preserve the analytical definitions and validated findings established in the earlier project stages.

## 11. Reproducibility and Maintenance

The Power BI report should remain connected to the validated processed dataset and any analytical outputs required by its model.

Recommended maintenance practices include:

- Preserve the original raw dataset.
- Keep the processed dataset reproducible through the documented cleaning process.
- Validate customer counts after data refresh.
- Recheck missing values and data types.
- Confirm that churn calculations remain consistent.
- Revalidate predictive metrics whenever model outputs are updated.
- Review recommendations when new analytical evidence becomes available.
- Update this guide whenever report pages, measures, or interactions change.

The report should not be considered validated merely because it refreshes successfully. Its results must also agree with the project's documented analytical outputs.

## 12. Conclusion

The Power BI stage provides the business intelligence layer of the Customer Churn Analytics project.

The six-page report moves from an executive summary of churn performance to detailed churn drivers, high-risk segments, predictive intelligence, retention strategy, and final recommendations.

The overall churn rate of 26.54%, the higher churn observed among month-to-month customers, the elevated churn among early-tenure customers, and the predictive model's ROC-AUC of 0.8419 provide important evidence for understanding and prioritizing customer retention.

The planned HTML Content redesign represents the next presentation improvement. Regardless of the visual design, the report must preserve consistent metric definitions, accurate calculations, transparent limitations, and recommendations supported by the underlying analysis.