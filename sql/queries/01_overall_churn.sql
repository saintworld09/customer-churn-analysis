SELECT
    COUNT(*) AS total_customers,
    SUM(churn_flag) AS churned_customers,
    COUNT(*) - SUM(churn_flag) AS active_customers,
    ROUND(
        SUM(churn_flag) * 100.0 / COUNT(*),
        2
    ) AS churn_rate
FROM vw_customer_churn;