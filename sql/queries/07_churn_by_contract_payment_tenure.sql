/*
=========================================================
07 - Churn by Contract, Payment Method, and Tenure
=========================================================

Business Question:
Among month-to-month customers who use electronic check,
how does churn vary across different tenure bands?

Purpose:
This analysis combines three customer characteristics:
- Contract type
- Payment method
- Tenure

It helps identify whether the high-churn segment observed
among month-to-month electronic-check customers is
concentrated among newer or longer-tenured customers.

Key Metrics:
- Customer count
- Churned customer count
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
  AND payment_method = 'Electronic check'
GROUP BY tenure_band
ORDER BY
    CASE tenure_band
        WHEN '0–6 Months' THEN 1
        WHEN '7–12 Months' THEN 2
        WHEN '13–24 Months' THEN 3
        WHEN '25–48 Months' THEN 4
        WHEN '49–72 Months' THEN 5
    END;