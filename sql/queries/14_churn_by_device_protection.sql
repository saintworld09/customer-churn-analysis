/*
=========================================================
14 - Churn by Device Protection
=========================================================

Business Question:
How does customer churn vary between customers with
and without Device Protection?

Purpose:
This analysis compares customer volume, churned customers,
and churn rate based on Device Protection status.

It helps determine whether Device Protection is associated
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
    device_protection,
    COUNT(*) AS customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(
        SUM(churn_flag) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM vw_customer_churn
GROUP BY device_protection
ORDER BY churn_rate DESC;