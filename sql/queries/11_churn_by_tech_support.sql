/*
=========================================================
11 - Churn by Tech Support
=========================================================

Business Question:
How does customer churn vary between customers with
and without Tech Support?

Purpose:
This analysis compares customer volume, churned customers,
and churn rate based on Tech Support status.

It helps determine whether Tech Support is associated
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
    tech_support,
    COUNT(*) AS customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(
        SUM(churn_flag) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM vw_customer_churn
GROUP BY tech_support
ORDER BY churn_rate DESC;