/*
=========================================================
08 - Churn by Senior Citizen Status
=========================================================

Business Question:
How does customer churn vary between senior citizens and
non-senior citizens?

Purpose:
This analysis compares customer volume, churned customers,
and churn rate between senior citizens and non-senior
citizens.

It helps determine whether customer age group is associated
with different observed churn patterns.

Key Metrics:
- Customer count
- Churned customer count
- Churn rate

Source:
vw_customer_churn
=========================================================
*/

SELECT
    senior_citizen_status,
    COUNT(*) AS customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(
        SUM(churn_flag) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM vw_customer_churn
GROUP BY senior_citizen_status
ORDER BY churn_rate DESC;