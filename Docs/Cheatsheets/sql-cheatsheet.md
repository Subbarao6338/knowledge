# SQL Cheatsheet

## Query Execution Order (conceptual)

```text
FROM/JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT/OFFSET
```
This is why you can't reference a `SELECT` alias in `WHERE`, but you often can in `ORDER BY` — `WHERE` is evaluated before `SELECT` builds the output columns.

---

## Basic Queries

```sql
SELECT column1, column2 FROM table_name;
SELECT * FROM table_name;
SELECT DISTINCT category FROM orders;
SELECT column1 AS alias1 FROM table_name;

SELECT * FROM orders
WHERE status = 'completed'
  AND amount > 100
  AND created_at >= '2026-01-01';

SELECT * FROM orders WHERE status IN ('pending', 'shipped');
SELECT * FROM orders WHERE amount BETWEEN 100 AND 500;
SELECT * FROM orders WHERE customer_email LIKE '%@gmail.com';
SELECT * FROM orders WHERE notes IS NULL;
SELECT * FROM orders WHERE notes IS NOT NULL;

SELECT * FROM orders ORDER BY created_at DESC, amount ASC;
SELECT * FROM orders LIMIT 10 OFFSET 20;      -- pagination
```

## Joins

```sql
-- INNER JOIN: only matching rows in both tables
SELECT o.id, c.name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id;

-- LEFT JOIN: all rows from left, matched rows from right (NULLs if no match)
SELECT o.id, c.name
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.id;

-- RIGHT JOIN: all rows from right, matched rows from left
SELECT o.id, c.name
FROM orders o
RIGHT JOIN customers c ON o.customer_id = c.id;

-- FULL OUTER JOIN: all rows from both sides
SELECT o.id, c.name
FROM orders o
FULL OUTER JOIN customers c ON o.customer_id = c.id;

-- CROSS JOIN: cartesian product (every row x every row)
SELECT * FROM sizes CROSS JOIN colors;

-- SELF JOIN: table joined to itself
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;

-- Filtering for "no match" (anti-join pattern)
SELECT c.*
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;                    -- customers with no orders
```

## Aggregation

```sql
SELECT COUNT(*), SUM(amount), AVG(amount), MIN(amount), MAX(amount)
FROM orders;

SELECT category, COUNT(*) AS n, SUM(amount) AS total
FROM orders
GROUP BY category;

SELECT category, COUNT(*) AS n
FROM orders
GROUP BY category
HAVING COUNT(*) > 10;                 -- filter on aggregated result (WHERE can't do this)

SELECT COUNT(DISTINCT customer_id) FROM orders;

-- Multiple grouping levels
SELECT category, sub_category, SUM(amount)
FROM orders
GROUP BY category, sub_category;

-- ROLLUP / CUBE (subtotals + grand total)
SELECT category, sub_category, SUM(amount)
FROM orders
GROUP BY ROLLUP(category, sub_category);
```

## Subqueries & CTEs

```sql
-- Subquery in WHERE
SELECT * FROM orders
WHERE customer_id IN (SELECT id FROM customers WHERE country = 'DE');

-- Correlated subquery
SELECT * FROM orders o
WHERE amount > (SELECT AVG(amount) FROM orders WHERE customer_id = o.customer_id);

-- Subquery in FROM
SELECT category, avg_amount
FROM (
    SELECT category, AVG(amount) AS avg_amount
    FROM orders
    GROUP BY category
) t
WHERE avg_amount > 100;

-- Common Table Expression (CTE) — same result, more readable
WITH category_avg AS (
    SELECT category, AVG(amount) AS avg_amount
    FROM orders
    GROUP BY category
)
SELECT * FROM category_avg WHERE avg_amount > 100;

-- Multiple CTEs, chained
WITH filtered AS (
    SELECT * FROM orders WHERE status = 'completed'
),
by_customer AS (
    SELECT customer_id, SUM(amount) AS total
    FROM filtered
    GROUP BY customer_id
)
SELECT * FROM by_customer WHERE total > 1000;

-- Recursive CTE (e.g., org hierarchy traversal)
WITH RECURSIVE org_chart AS (
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL          -- anchor: top of hierarchy

    UNION ALL

    SELECT e.id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT * FROM org_chart ORDER BY level;
```

## Window Functions

```sql
-- Ranking
SELECT id, category, amount,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount DESC) AS rn,
    RANK()       OVER (PARTITION BY category ORDER BY amount DESC) AS rnk,       -- ties get same rank, gaps after
    DENSE_RANK() OVER (PARTITION BY category ORDER BY amount DESC) AS dense_rnk  -- ties get same rank, no gaps
FROM orders;

-- Running totals / moving aggregates
SELECT id, order_date, amount,
    SUM(amount) OVER (ORDER BY order_date) AS running_total,
    AVG(amount) OVER (ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_7d_avg
FROM orders;

-- Lag / Lead
SELECT id, order_date, amount,
    LAG(amount, 1)  OVER (ORDER BY order_date) AS prev_amount,
    LEAD(amount, 1) OVER (ORDER BY order_date) AS next_amount
FROM orders;

-- First/last value in a window
SELECT category, amount,
    FIRST_VALUE(amount) OVER (PARTITION BY category ORDER BY order_date) AS first_order_amount,
    LAST_VALUE(amount)  OVER (PARTITION BY category ORDER BY order_date
                              ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_order_amount
FROM orders;

-- NTILE — split into N buckets
SELECT id, amount, NTILE(4) OVER (ORDER BY amount) AS quartile
FROM orders;
```

**Window frame clauses:** `ROWS BETWEEN n PRECEDING AND CURRENT ROW`, `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` (whole partition).

## Set Operations

```sql
SELECT id FROM table_a
UNION                       -- combines + removes duplicates
SELECT id FROM table_b;

SELECT id FROM table_a
UNION ALL                   -- combines, keeps duplicates (faster, no dedup step)
SELECT id FROM table_b;

SELECT id FROM table_a
INTERSECT                   -- rows in both
SELECT id FROM table_b;

SELECT id FROM table_a
EXCEPT                      -- rows in A but not in B (MINUS in Oracle)
SELECT id FROM table_b;
```

## Conditional Logic

```sql
SELECT
    id,
    CASE
        WHEN amount > 1000 THEN 'high'
        WHEN amount > 100 THEN 'medium'
        ELSE 'low'
    END AS amount_tier
FROM orders;

SELECT COALESCE(nickname, first_name, 'Unknown') AS display_name FROM users;
SELECT NULLIF(amount, 0) AS amount_or_null FROM orders;      -- returns NULL if amount = 0
SELECT IFNULL(amount, 0) FROM orders;                          -- MySQL/BigQuery shorthand for COALESCE(x, default)
```

## String Functions

```sql
SELECT CONCAT(first_name, ' ', last_name) FROM users;
SELECT first_name || ' ' || last_name FROM users;      -- ANSI/Postgres concatenation operator
SELECT UPPER(name), LOWER(name), TRIM(name) FROM users;
SELECT LENGTH(name) FROM users;
SELECT SUBSTRING(name FROM 1 FOR 3) FROM users;
SELECT REPLACE(name, 'old', 'new') FROM users;
SELECT SPLIT_PART(email, '@', 2) FROM users;             -- Postgres/Snowflake
SELECT name LIKE '%smith%' FROM users;                     -- case-sensitive pattern match
SELECT name ILIKE '%smith%' FROM users;                       -- case-insensitive (Postgres)
SELECT REGEXP_REPLACE(name, '[0-9]+', '') FROM users;
```

## Date/Time Functions

```sql
SELECT CURRENT_DATE, CURRENT_TIMESTAMP;
SELECT DATE_TRUNC('month', order_date) FROM orders;         -- Postgres/Snowflake
SELECT EXTRACT(YEAR FROM order_date) FROM orders;
SELECT order_date + INTERVAL '7 days' FROM orders;
SELECT DATEDIFF(day, start_date, end_date) FROM orders;        -- Snowflake/SQL Server style
SELECT DATE_ADD(order_date, INTERVAL 1 MONTH) FROM orders;        -- MySQL
SELECT TO_CHAR(order_date, 'YYYY-MM') FROM orders;                   -- Postgres/Oracle formatting
SELECT FORMAT_DATE('%Y-%m', order_date) FROM orders;                    -- BigQuery
```

## Data Definition (DDL)

```sql
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    amount DECIMAL(10, 2) DEFAULT 0,
    status VARCHAR(20) CHECK (status IN ('pending', 'completed', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

ALTER TABLE orders ADD COLUMN notes TEXT;
ALTER TABLE orders DROP COLUMN notes;
ALTER TABLE orders RENAME COLUMN amount TO total_amount;
ALTER TABLE orders ALTER COLUMN amount TYPE NUMERIC(12,2);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE UNIQUE INDEX idx_orders_ref ON orders(reference_number);

DROP TABLE orders;
TRUNCATE TABLE orders;              -- fast full delete, resets identity, minimal logging
```

## Data Manipulation (DML)

```sql
INSERT INTO orders (customer_id, amount, status) VALUES (1, 99.99, 'pending');
INSERT INTO orders (customer_id, amount) SELECT customer_id, amount FROM staging_orders;

UPDATE orders SET status = 'completed' WHERE id = 5;
UPDATE orders SET amount = amount * 1.1 WHERE category = 'premium';

DELETE FROM orders WHERE status = 'cancelled';

-- Upsert (dialect-specific)
INSERT INTO orders (id, amount) VALUES (1, 100)
ON CONFLICT (id) DO UPDATE SET amount = EXCLUDED.amount;      -- Postgres

MERGE INTO orders t USING staging s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET t.amount = s.amount
WHEN NOT MATCHED THEN INSERT (id, amount) VALUES (s.id, s.amount);  -- ANSI standard, most warehouses
```

## Views & Materialized Views

```sql
CREATE VIEW active_customers AS
SELECT * FROM customers WHERE status = 'active';

CREATE MATERIALIZED VIEW monthly_sales AS
SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS total
FROM orders
GROUP BY 1;

REFRESH MATERIALIZED VIEW monthly_sales;    -- must be manually/scheduled refreshed
```

## Transactions

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;                     -- or ROLLBACK; on error

-- Savepoints for partial rollback
BEGIN;
SAVEPOINT before_risky_op;
...
ROLLBACK TO SAVEPOINT before_risky_op;
COMMIT;
```

## Indexes & Performance

```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 5;
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 5;    -- Postgres: actual execution stats

-- Index types
CREATE INDEX idx_btree ON orders(customer_id);                 -- default, good for equality & range
CREATE INDEX idx_partial ON orders(customer_id) WHERE status = 'pending';  -- partial index
CREATE INDEX idx_composite ON orders(customer_id, order_date);    -- composite — order matters for usage
```

**General tips:**
- Index columns used in `WHERE`, `JOIN`, and `ORDER BY` — but every index adds write overhead, so don't over-index.
- Composite index column order matters: an index on `(a, b)` helps queries filtering on `a` alone or `a AND b`, but not `b` alone.
- Avoid functions on indexed columns in `WHERE` (`WHERE YEAR(date) = 2026`) — it prevents index usage; rewrite as a range (`WHERE date >= '2026-01-01' AND date < '2027-01-01'`).
- `SELECT *` fetches unnecessary columns — select only what's needed, especially in wide tables.
- Prefer `EXISTS` over `IN` with large subqueries in many engines — the optimizer can short-circuit as soon as one match is found.

```sql
-- EXISTS vs IN
SELECT * FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```

## Common Gotchas

- `NULL` is never equal to anything, including itself — use `IS NULL` / `IS NOT NULL`, never `= NULL`.
- `COUNT(column)` skips nulls; `COUNT(*)` counts all rows.
- Integer division truncates in many engines (`5 / 2 = 2`) — cast one operand to a decimal/float to avoid this.
- `GROUP BY` requires every non-aggregated `SELECT` column to appear in the `GROUP BY` clause (strict in Postgres/most engines; MySQL historically more lenient).
- `HAVING` filters after aggregation; `WHERE` filters before — using `WHERE` to filter an aggregate value is a common mistake.
- Be careful with `UNION` vs `UNION ALL` performance — `UNION` always dedups, which requires a sort/hash step.
