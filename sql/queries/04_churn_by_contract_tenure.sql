/*
=========================================================
04 - Churn by Contract and Tenure
=========================================================

Business Question:
How does customer churn vary across different tenure
bands within each contract type?

Purpose:
This analysis compares customer volume, churned customers,
and churn rate across contract and tenure combinations.

It helps identify whether churn patterns differ between
shorter- and longer-tenured customers within each contract
type.

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
    tenure_band,
    COUNT(*) AS customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(
        SUM(churn_flag) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM vw_customer_churn
GROUP BY
    contract,
    tenure_band
ORDER BY
    contract,
    CASE tenure_band
        WHEN '0–6 Months' THEN 1
        WHEN '7–12 Months' THEN 2
        WHEN '13–24 Months' THEN 3
        WHEN '25–48 Months' THEN 4
        WHEN '49–72 Months' THEN 5
    END;