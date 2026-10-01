/*
=========================================================
05 - Churn by Contract and Internet Service
=========================================================

Business Question:
How does customer churn vary across internet service
types within each contract type?

Purpose:
This analysis compares customer volume, churned customers,
and churn rate across contract and internet service
combinations.

It helps identify customer segments with higher or lower
observed churn rates based on their contract and internet
service.

Key Metrics:
- Customer count
- Churned customer count
- Churn rate

Source:
vw_customer_churn
=========================================================
*/

SELECT
    contract,
    internet_service,
    COUNT(*) AS customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(
        SUM(churn_flag) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM vw_customer_churn
GROUP BY
    contract,
    internet_service
ORDER BY
    contract,
    churn_rate DESC;