/*
=========================================================
06 - Churn by Contract and Payment Method
=========================================================

Business Question:
How does customer churn vary across different payment
methods within each contract type?

Purpose:
This analysis compares customer volume, churned customers,
and churn rate across contract and payment method
combinations.

It helps identify payment methods associated with higher
or lower observed churn within each contract type.

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
    payment_method,
    COUNT(*) AS customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(
        SUM(churn_flag) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM vw_customer_churn
GROUP BY
    contract,
    payment_method
ORDER BY
    contract,
    churn_rate DESC;