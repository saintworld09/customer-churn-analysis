/*
=========================================================
09 - Churn by Partner Status
=========================================================

Business Question:
How does customer churn vary between customers who have
a partner and those who do not?

Purpose:
This analysis compares customer volume, churned customers,
and churn rate based on partner status.

It helps identify whether having a partner is associated
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
    partner,
    COUNT(*) AS customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(
        SUM(churn_flag) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM vw_customer_churn
GROUP BY partner
ORDER BY churn_rate DESC;