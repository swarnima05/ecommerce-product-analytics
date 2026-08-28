-- Cohort month is the first delivered purchase month. Retention is the share of every
-- cohort that made a delivered purchase in each subsequent month (month_number = 0 is acquisition).
WITH customer_months AS (
    SELECT c.customer_unique_id, date(o.order_purchase_timestamp, 'start of month') AS order_month
    FROM orders o JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id, date(o.order_purchase_timestamp, 'start of month')
), cohorts AS (
    SELECT customer_unique_id, MIN(order_month) AS cohort_month FROM customer_months GROUP BY customer_unique_id
), cohort_sizes AS (
    SELECT cohort_month, COUNT(*) AS cohort_size FROM cohorts GROUP BY cohort_month
)
SELECT c.cohort_month, m.order_month,
       (CAST(strftime('%Y', m.order_month) AS INTEGER) - CAST(strftime('%Y', c.cohort_month) AS INTEGER)) * 12 +
       CAST(strftime('%m', m.order_month) AS INTEGER) - CAST(strftime('%m', c.cohort_month) AS INTEGER) AS month_number,
       COUNT(DISTINCT m.customer_unique_id) AS retained_customers, s.cohort_size,
       ROUND(100.0 * COUNT(DISTINCT m.customer_unique_id) / s.cohort_size, 2) AS retention_pct
FROM customer_months m JOIN cohorts c ON m.customer_unique_id = c.customer_unique_id
JOIN cohort_sizes s ON c.cohort_month = s.cohort_month
GROUP BY c.cohort_month, m.order_month, month_number, s.cohort_size
ORDER BY c.cohort_month, month_number;
