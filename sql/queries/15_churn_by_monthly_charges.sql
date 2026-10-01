/*
=========================================================
15 - Churn by Monthly Charges
=========================================================

Business Question:
How does customer churn vary across monthly charge
levels?

Purpose:
This analysis compares average monthly charges and
customer counts between customers who churned and
customers who remained active.

It helps determine whether customers with different
monthly spending levels show different observed churn
patterns.

Key Metrics:
- Customer count
- Churned customers
- Average monthly charges
- Minimum monthly charges
- Maximum monthly charges
- Churn rate

Source:
vw_customer_churn
=========================================================
*/

SELECT
    churn,
    COUNT(*) AS customers,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges,
    ROUND(MIN(monthly_charges), 2) AS min_monthly_charges,
    ROUND(MAX(monthly_charges), 2) AS max_monthly_charges
FROM vw_customer_churn
GROUP BY churn;