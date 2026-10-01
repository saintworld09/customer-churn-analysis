/*
=========================================================
17 - Month-to-Month Churn by Tenure
=========================================================

Business Question:
Among month-to-month customers, how does churn vary
across different tenure bands?

Purpose:
This analysis focuses on month-to-month customers and
compares customer volume, churned customers, and churn
rate across tenure bands.

Key Metrics:
- Customer count
- Churned customers
- Churn rate

Source:
vw_customer_churn
=========================================================
*/

SELECT
    tenure_band,
    COUNT(*) AS customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(
        SUM(churn_flag) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM vw_customer_churn
WHERE contract = 'Month-to-month'
GROUP BY tenure_band
ORDER BY
    CASE tenure_band
        WHEN '0–6 Months' THEN 1
        WHEN '7–12 Months' THEN 2
        WHEN '13–24 Months' THEN 3
        WHEN '25–48 Months' THEN 4
        WHEN '49–72 Months' THEN 5
    END;