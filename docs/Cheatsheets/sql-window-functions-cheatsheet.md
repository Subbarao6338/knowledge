---
layout: default
title: "SQL Window Functions Cheatsheet"
---

# SQL Window Functions Cheatsheet

Window functions in SQL compute an aggregate value based on a group of rows, called a "window" or partition, which are related to the current row. Unlike regular group-by aggregates, window functions do not collapse rows; each row retains its unique identity.

---

## 1. Core Syntax & Anatomy

```sql
SELECT
  column_name,
  window_function() OVER (
    PARTITION BY partition_column
    ORDER BY sort_column
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS calculated_alias
FROM table_name;
```

- **`PARTITION BY`**: Groups rows into subsets. If omitted, the window function processes the entire table as a single partition.
- **`ORDER BY`**: Sorts rows inside each partition, defining the sequence of operation.
- **`ROWS/RANGE` Frame**: Restricts the subset of rows processed relative to the current row.

---

## 2. Standard Ranking Functions

Ranking functions assign sequential or relational numeric identifiers to rows within each partition.

```sql
SELECT
  employee_id,
  department_id,
  salary,
  -- 1. Sequential numbering without gaps (e.g., 1, 2, 3, 4)
  ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS row_num,

  -- 2. Rank with gaps for equal values (e.g., 1, 2, 2, 4)
  RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rank_with_gaps,

  -- 3. Rank without gaps for equal values (e.g., 1, 2, 2, 3)
  DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dense_rank_no_gaps,

  -- 4. Distribute rows into N equal tiles (e.g., quartiles 1, 2, 3, 4)
  NTILE(4) OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_quartile
FROM employees;
```

---

## 3. Value-Based Functions

Value functions retrieve specific cell entries from adjacent or distant rows within the partition.

```sql
SELECT
  product_id,
  sale_date,
  revenue,
  -- 1. Retrieve value from the previous row (defaults to offset 1)
  LAG(revenue, 1, 0) OVER (PARTITION BY product_id ORDER BY sale_date) AS prev_day_revenue,

  -- 2. Retrieve value from the next row
  LEAD(revenue, 1, 0) OVER (PARTITION BY product_id ORDER BY sale_date) AS next_day_revenue,

  -- 3. Get the first entry of the partition window
  FIRST_VALUE(revenue) OVER (
    PARTITION BY product_id
    ORDER BY sale_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS first_sale_revenue,

  -- 4. Get the last entry of the partition window
  LAST_VALUE(revenue) OVER (
    PARTITION BY product_id
    ORDER BY sale_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS last_sale_revenue
FROM sales;
```

---

## 4. Advanced Window Frames (Running Aggregates)

Window frame boundary definitions allow precise calculation of rolling averages, running sums, and cumulative metrics.

```sql
SELECT
  transaction_id,
  account_id,
  transaction_date,
  amount,
  -- 1. Running total from partition start to current row
  SUM(amount) OVER (
    PARTITION BY account_id
    ORDER BY transaction_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_balance,

  -- 2. 7-day Moving Average (current row + 6 preceding rows)
  AVG(amount) OVER (
    PARTITION BY account_id
    ORDER BY transaction_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS moving_avg_7day,

  -- 3. Total partition sum (summing all rows in partition regardless of frame)
  SUM(amount) OVER (
    PARTITION BY account_id
  ) AS total_account_volume
FROM bank_transactions;
```

### Frame Boundaries Reference:
- `UNBOUNDED PRECEDING`: First row of the partition.
- `UNBOUNDED FOLLOWING`: Last row of the partition.
- `CURRENT ROW`: The row currently being processed.
- `N PRECEDING`: `N` rows before the current row.
- `N FOLLOWING`: `N` rows after the current row.
