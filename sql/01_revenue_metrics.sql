-- Delivered orders only: cancelled/unavailable orders did not complete fulfillment.
-- Result set 1: monthly revenue and AOV from distinct order totals.
WITH delivered_order_totals AS (
    SELECT o.order_id, date(o.order_purchase_timestamp, 'start of month') AS order_month,
           SUM(oi.price + oi.freight_value) AS order_revenue
    FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY o.order_id, date(o.order_purchase_timestamp, 'start of month')
)
SELECT order_month, ROUND(SUM(order_revenue), 2) AS revenue,
       COUNT(*) AS orders, ROUND(AVG(order_revenue), 2) AS aov
FROM delivered_order_totals
GROUP BY order_month
ORDER BY order_month;

-- Result set 2: overall AOV = delivered order revenue / number of delivered orders.
WITH delivered_order_totals AS (
    SELECT o.order_id, SUM(oi.price + oi.freight_value) AS order_revenue
    FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered' GROUP BY o.order_id
)
SELECT ROUND(AVG(order_revenue), 2) AS overall_aov FROM delivered_order_totals;
