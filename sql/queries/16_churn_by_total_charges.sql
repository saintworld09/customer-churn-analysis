/*
=========================================================
16 - Churn by Total Charges
=========================================================

Business Question:
How do accumulated customer charges differ between
customers who churned and customers who remained active?

Purpose:
This analysis compares the total accumulated charges
and average accumulated charges of churned and active
customers.

Customers with unrecorded TotalCharges are excluded
from the financial calculations because their accumulated
charge amount is not available.

Key Metrics:
- Customers with recorded charges
- Total accumulated charges
- Average total charges
- Minimum total charges
- Maximum total charges

Source:
vw_customer_churn
=========================================================
*/

SELECT
    churn,
    COUNT(total_charges_clean) AS customers_with_recorded_charges,
    ROUND(SUM(total_charges_clean), 2) AS total_accumulated_charges,
    ROUND(AVG(total_charges_clean), 2) AS avg_total_charges,
    ROUND(MIN(total_charges_clean), 2) AS min_total_charges,
    ROUND(MAX(total_charges_clean), 2) AS max_total_charges
FROM vw_customer_churn
WHERE total_charges_clean IS NOT NULL
GROUP BY churn
ORDER BY churn;