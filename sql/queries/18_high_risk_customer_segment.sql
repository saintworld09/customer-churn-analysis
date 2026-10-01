/*
=========================================================
18 - High-Risk Customer Segment
=========================================================

Business Question:
What is the observed churn rate among customers who have
a month-to-month contract, are within their first 6 months,
use fiber optic internet, and pay by electronic check?

Purpose:
Identify a concentrated customer segment with a high
observed churn rate for further business investigation.

Key Metrics:
- Segment Customers
- Churned Customers
- Segment Churn Rate

Source:
vw_customer_churn
=========================================================
*/

SELECT
    COUNT(*) AS segment_customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(
        SUM(churn_flag) * 100.0 / COUNT(*),
        2
    ) AS segment_churn_rate
FROM vw_customer_churn
WHERE contract = 'Month-to-month'
AND tenure_band = '0–6 Months'
AND internet_service = 'Fiber optic'
AND payment_method = 'Electronic check';