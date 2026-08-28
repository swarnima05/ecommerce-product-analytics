-- ROW_NUMBER sequences a customer's delivered orders chronologically. SUM OVER then
-- produces each customer's running recognized revenue without moving data into pandas.
WITH order_totals AS (
    SELECT o.order_id, c.customer_unique_id, o.order_purchase_timestamp,
           SUM(oi.price + oi.freight_value) AS order_revenue
    FROM orders o JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY o.order_id, c.customer_unique_id, o.order_purchase_timestamp
)
SELECT customer_unique_id, order_id, order_purchase_timestamp,
       ROUND(order_revenue, 2) AS order_revenue,
       ROW_NUMBER() OVER (PARTITION BY customer_unique_id ORDER BY order_purchase_timestamp, order_id) AS customer_order_sequence,
       ROUND(SUM(order_revenue) OVER (PARTITION BY customer_unique_id ORDER BY order_purchase_timestamp, order_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS running_revenue
FROM order_totals
ORDER BY customer_unique_id, customer_order_sequence;
