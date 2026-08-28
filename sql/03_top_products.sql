-- Top products/categories by delivered revenue and units sold.
SELECT p.product_id, COALESCE(p.product_category_name, 'unknown') AS category,
       ROUND(SUM(oi.price + oi.freight_value), 2) AS revenue, COUNT(*) AS units_sold
FROM order_items oi JOIN orders o ON oi.order_id = o.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_id, COALESCE(p.product_category_name, 'unknown')
ORDER BY revenue DESC LIMIT 10;

SELECT COALESCE(p.product_category_name, 'unknown') AS category,
       ROUND(SUM(oi.price + oi.freight_value), 2) AS revenue, COUNT(*) AS units_sold
FROM order_items oi JOIN orders o ON oi.order_id = o.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_status = 'delivered'
GROUP BY COALESCE(p.product_category_name, 'unknown')
ORDER BY revenue DESC LIMIT 10;
