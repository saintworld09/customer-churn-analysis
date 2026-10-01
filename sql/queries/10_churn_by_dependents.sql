/*
=========================================================
10 - Churn by Dependents Status
=========================================================

Business Question:
How does customer churn vary between customers with
dependents and customers without dependents?

Purpose:
This analysis compares customer volume, churned customers,
and churn rate based on dependents status.

It helps identify whether having dependents is associated
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
    dependents,
    COUNT(*) AS customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(
        SUM(churn_flag) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM vw_customer_churn
GROUP BY dependents
ORDER BY churn_rate DESC;