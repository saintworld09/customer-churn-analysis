/*
=========================================================
12 - Churn by Online Security
=========================================================

Business Question:
How does customer churn vary between customers with
and without Online Security?

Purpose:
This analysis compares customer volume, churned customers,
and churn rate based on Online Security status.

It helps determine whether Online Security is associated
with different observed churn patterns in the customer base.

Key Metrics:
- Customer count
- Churned customer count
- Churn rate

Source:
vw_customer_churn
=========================================================
*/

SELECT
    online_security,
    COUNT(*) AS customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(
        SUM(churn_flag) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM vw_customer_churn
GROUP BY online_security
ORDER BY churn_rate DESC;