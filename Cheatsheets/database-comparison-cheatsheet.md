# MySQL vs PostgreSQL vs MSSQL vs BigQuery vs Azure Synapse

## Quick Classification

| | MySQL | PostgreSQL | MSSQL (SQL Server) | BigQuery | Azure Synapse |
|---|---|---|---|---|---|
| Category | OLTP (row-store RDBMS) | OLTP (row-store RDBMS) | OLTP (row-store RDBMS) | OLAP (serverless columnar warehouse) | OLAP (warehouse, dedicated or serverless pools) |
| Owner | Oracle (open source) | PostgreSQL Global Dev Group (open source) | Microsoft | Google Cloud | Microsoft (Azure) |
| Typical use | Web apps, transactional systems | Web apps, transactional + semi-analytical | Enterprise apps, .NET-heavy shops | Large-scale analytics, BI, ELT | Enterprise analytics, integrated with Power BI/ADF |
| Storage model | Row-based | Row-based (with some columnar extensions) | Row-based (+ columnar indexes) | Columnar, distributed | Columnar (dedicated SQL pools), row for serverless |
| Scaling | Vertical primarily; read replicas | Vertical primarily; read replicas | Vertical; Always On for HA | Automatic, massively horizontal | Horizontal via distribution + MPP |
| Pricing model | Free / managed service cost | Free / managed service cost | License or managed service cost | Pay per query (bytes scanned) or flat-rate slots | Pay per DWU (dedicated) or per query (serverless) |

---

## 1. MySQL

**Best for:** web applications, CMSs (WordPress), read-heavy OLTP workloads, simpler relational needs.

```sql
-- Distinctive syntax
SELECT * FROM orders LIMIT 10 OFFSET 20;
SELECT NOW();                                    -- current timestamp
SELECT CONCAT(first_name, ' ', last_name) FROM users;
SHOW TABLES;
SHOW DATABASES;
DESCRIBE orders;
SELECT * FROM orders WHERE amount BETWEEN 10 AND 100;

INSERT INTO orders (id, amount) VALUES (1, 100)
ON DUPLICATE KEY UPDATE amount = VALUES(amount);       -- MySQL's upsert syntax

-- Auto-increment
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    amount DECIMAL(10,2)
);

-- Storage engines matter
CREATE TABLE t (id INT) ENGINE=InnoDB;        -- default, supports transactions/FKs
CREATE TABLE t (id INT) ENGINE=MyISAM;           -- legacy, no transactions, faster for read-only

EXPLAIN SELECT * FROM orders WHERE customer_id = 5;
```

**Strengths:** simple to operate, huge ecosystem/community, fast for straightforward read-heavy workloads, widely supported by every hosting provider.

**Limitations:** historically weaker on complex queries, window functions, and strict standards compliance (improved significantly in 8.0+); JSON support is more limited than Postgres; less advanced indexing options.

---

## 2. PostgreSQL

**Best for:** applications needing advanced SQL features, strong data integrity, JSON/semi-structured data alongside relational data, geospatial (PostGIS), and extensibility.

```sql
-- Distinctive syntax
SELECT * FROM orders LIMIT 10 OFFSET 20;
SELECT NOW();
SELECT first_name || ' ' || last_name FROM users;          -- concatenation operator
\dt                              -- list tables (psql client)
\d orders                          -- describe table (psql client)

-- Upsert
INSERT INTO orders (id, amount) VALUES (1, 100)
ON CONFLICT (id) DO UPDATE SET amount = EXCLUDED.amount;

-- Serial / identity columns
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,                    -- classic
    id2 INT GENERATED ALWAYS AS IDENTITY,        -- SQL-standard modern equivalent
    amount NUMERIC(10,2)
);

-- Native JSON/JSONB support
SELECT data->>'name' FROM events WHERE data @> '{"type": "click"}';
CREATE INDEX idx_data ON events USING GIN (data);

-- Arrays as a native type
SELECT ARRAY[1,2,3];
SELECT * FROM t WHERE tags @> ARRAY['urgent'];

-- Window functions, CTEs, full support of advanced SQL (see the SQL cheatsheet)
WITH ranked AS (
    SELECT *, RANK() OVER (PARTITION BY category ORDER BY amount DESC) AS rnk
    FROM orders
)
SELECT * FROM ranked WHERE rnk = 1;

EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 5;
```

**Strengths:** best-in-class standards compliance, rich extension ecosystem (PostGIS, pg_cron, TimescaleDB), native JSONB, excellent for hybrid transactional/semi-analytical workloads, strong concurrency (MVCC).

**Limitations:** more operational tuning knobs than MySQL for high-throughput simple workloads; vertical scaling has practical ceilings for very large analytical workloads (though extensions like Citus help).

---

## 3. Microsoft SQL Server (MSSQL / T-SQL)

**Best for:** enterprise .NET environments, existing Microsoft stack shops, workloads needing tight Windows/Active Directory integration.

```sql
-- Distinctive syntax (T-SQL)
SELECT TOP 10 * FROM orders ORDER BY amount DESC;      -- TOP instead of LIMIT
SELECT GETDATE();                                          -- current timestamp
SELECT CONCAT(first_name, ' ', last_name) FROM users;
SELECT * FROM orders WHERE amount BETWEEN 10 AND 100;

SELECT * FROM sys.tables;
EXEC sp_help 'orders';                    -- describe table
EXEC sp_helpdb;

-- Identity columns
CREATE TABLE orders (
    id INT IDENTITY(1,1) PRIMARY KEY,
    amount DECIMAL(10,2)
);

-- Upsert (MERGE, ANSI-standard, also common in Snowflake/BigQuery)
MERGE INTO orders AS target
USING staging AS source
ON target.id = source.id
WHEN MATCHED THEN UPDATE SET target.amount = source.amount
WHEN NOT MATCHED THEN INSERT (id, amount) VALUES (source.id, source.amount);

-- OFFSET/FETCH for pagination (SQL-standard style, also works)
SELECT * FROM orders ORDER BY id OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;

-- T-SQL procedural extensions
DECLARE @total INT;
SET @total = (SELECT COUNT(*) FROM orders);
PRINT @total;

CREATE PROCEDURE GetOrdersByCustomer @CustomerId INT
AS
BEGIN
    SELECT * FROM orders WHERE customer_id = @CustomerId;
END;
EXEC GetOrdersByCustomer @CustomerId = 5;

SET STATISTICS IO ON;
SELECT * FROM orders WHERE customer_id = 5;    -- shows execution stats
```

**Strengths:** mature enterprise tooling (SSMS, SQL Server Agent, Always On), strong T-SQL procedural language, tight integration with the Microsoft ecosystem (Azure, .NET, Power BI), columnstore indexes for hybrid analytical workloads.

**Limitations:** licensing costs can be significant outside the free Express/Developer editions; historically Windows-centric (though Linux support has improved); less common in open-source/startup stacks.

---

## 4. Google BigQuery

**Best for:** large-scale, serverless analytics; ELT workloads where you load raw data and transform in SQL; ad hoc analysis over massive datasets without managing infrastructure.

```sql
-- Standard SQL (default dialect since BigQuery's Standard SQL became default)
SELECT * FROM `my_project.my_dataset.my_table` LIMIT 10;   -- backtick-quoted fully-qualified names

SELECT category, SUM(value) AS total
FROM `my_project.my_dataset.orders`
GROUP BY category
ORDER BY total DESC;

-- Partitioned / clustered tables (critical for cost control)
CREATE TABLE my_dataset.orders (
    id INT64,
    amount NUMERIC,
    order_date DATE
)
PARTITION BY order_date
CLUSTER BY category;

SELECT * FROM my_dataset.orders
WHERE order_date BETWEEN '2026-01-01' AND '2026-01-31';   -- partition pruning reduces bytes scanned/cost

-- Arrays and structs are first-class
SELECT ARRAY_AGG(order_id) AS order_ids FROM orders GROUP BY customer_id;
SELECT * FROM UNNEST([1, 2, 3]) AS num;

-- Nested/repeated fields (common in BigQuery due to denormalized schemas)
SELECT customer.name, item.product_id
FROM orders, UNNEST(items) AS item;

-- Cost estimation before running
-- (bq CLI: bq query --dry_run 'SELECT ...')

-- Scripting (BigQuery supports procedural SQL scripting)
DECLARE total INT64 DEFAULT 0;
SET total = (SELECT COUNT(*) FROM my_dataset.orders);

-- User-defined functions
CREATE TEMP FUNCTION AddOne(x INT64) AS (x + 1);
SELECT AddOne(5);
```

**Strengths:** zero infrastructure management, scales automatically to petabytes, pay-per-query (or flat-rate) pricing, excellent for ELT with dbt, native ML (`BQML`), tight GCP integration (Vertex AI, Dataflow, Looker).

**Limitations:** cost can spike unpredictably on unpartitioned/large-scan queries if not carefully managed; not designed for high-frequency single-row transactional writes (it's OLAP, not OLTP); some SQL dialect quirks vs ANSI standard (e.g., backtick-quoted table names, `INT64`/`FLOAT64` type names).

---

## 5. Azure Synapse Analytics

**Best for:** enterprises already on Azure wanting a unified analytics platform combining data warehousing (SQL pools), big data (Spark pools), and pipelines (integrated with Azure Data Factory) in one workspace.

```sql
-- Dedicated SQL Pool (T-SQL dialect, MSSQL-derived)
SELECT TOP 10 * FROM orders ORDER BY amount DESC;
SELECT GETDATE();

-- Distribution strategy is a first-class concept (MPP architecture)
CREATE TABLE orders (
    id INT,
    customer_id INT,
    amount DECIMAL(10,2)
)
WITH (
    DISTRIBUTION = HASH(customer_id),     -- or ROUND_ROBIN, or REPLICATE
    CLUSTERED COLUMNSTORE INDEX
);

-- Serverless SQL pool — query files directly in a data lake without loading
SELECT *
FROM OPENROWSET(
    BULK 'https://mystorageacct.dfs.core.windows.net/container/data/*.parquet',
    FORMAT = 'PARQUET'
) AS rows;

-- CETAS — export query results back to the data lake
CREATE EXTERNAL TABLE dbo.summary
WITH (LOCATION = 'summary/', DATA_SOURCE = my_datasource, FILE_FORMAT = my_fileformat)
AS SELECT category, SUM(amount) AS total FROM orders GROUP BY category;

-- Statistics matter heavily for MPP query optimization
CREATE STATISTICS stat_customer_id ON orders(customer_id);
```

**Strengths:** unifies SQL-based warehousing and Spark-based big data processing in one workspace, strong Azure ecosystem integration (Data Factory, Power BI, Purview), serverless pool lets you query data lake files without ETL first, dedicated pools give predictable performance for heavy, consistent workloads.

**Limitations:** distribution key choice is a critical, hard-to-change design decision (poor choice causes data skew and slow joins); dedicated pools have a real ongoing cost even when idle unless paused; steeper learning curve than a fully serverless system like BigQuery; being progressively superseded in Microsoft's roadmap by **Microsoft Fabric**, which is worth checking for new projects.

---

## OLTP vs OLAP — the Real Dividing Line

| | MySQL / PostgreSQL / MSSQL | BigQuery / Synapse |
|---|---|---|
| Optimized for | Many small, fast reads/writes (single rows) | Few large, complex reads (aggregations over millions/billions of rows) |
| Storage | Row-oriented — efficient for fetching a full row | Column-oriented — efficient for scanning specific columns across many rows |
| Transactions | Full ACID, row-level locking | Limited or no traditional transaction support; append/batch-oriented |
| Typical query | `SELECT * FROM orders WHERE id = 5` | `SELECT category, SUM(amount) FROM orders GROUP BY category` |
| Scaling approach | Mostly vertical, some read replicas | Horizontal, massively parallel (MPP) |

**In practice:** OLTP databases (MySQL/Postgres/MSSQL) run the application; OLAP warehouses (BigQuery/Synapse) power analytics and BI, typically fed by an ELT pipeline pulling data out of the OLTP systems (see the ETL/ELT cheatsheet).

---

## Syntax Differences Cheat Table

| Task | MySQL | PostgreSQL | MSSQL | BigQuery | Synapse (dedicated pool) |
|---|---|---|---|---|---|
| Limit rows | `LIMIT 10` | `LIMIT 10` | `TOP 10` (before columns) | `LIMIT 10` | `TOP 10` |
| Current timestamp | `NOW()` | `NOW()` | `GETDATE()` | `CURRENT_TIMESTAMP()` | `GETDATE()` |
| String concat | `CONCAT(a,b)` | `a \|\| b` | `CONCAT(a,b)` or `+` | `CONCAT(a,b)` | `CONCAT(a,b)` or `+` |
| Auto-increment PK | `AUTO_INCREMENT` | `SERIAL` / `GENERATED ALWAYS AS IDENTITY` | `IDENTITY(1,1)` | N/A (no PK concept) | `IDENTITY(1,1)` |
| Upsert | `ON DUPLICATE KEY UPDATE` | `ON CONFLICT DO UPDATE` | `MERGE` | `MERGE` | `MERGE` |
| Boolean type | `TINYINT(1)` / `BOOLEAN` alias | `BOOLEAN` | `BIT` | `BOOL` | `BIT` |
| Auto string type | `VARCHAR(n)` | `VARCHAR(n)` / `TEXT` | `VARCHAR(n)` / `NVARCHAR(n)` | `STRING` | `VARCHAR(n)` |
| Show tables | `SHOW TABLES;` | `\dt` (psql) | `sys.tables` / SSMS UI | `INFORMATION_SCHEMA.TABLES` | `sys.tables` |
| Fully qualified table | `db.table` | `schema.table` | `db.schema.table` | `` `project.dataset.table` `` | `db.schema.table` |

---

## Choosing Between Them

- **Need a transactional backend for an app?** MySQL or PostgreSQL are the default choices; PostgreSQL if you need advanced SQL features, JSON, or extensions; MySQL if you want the simplest, most widely-hosted option.
- **Already a Microsoft/.NET shop, need enterprise support and tooling?** MSSQL.
- **Need to analyze massive datasets without managing any infrastructure, already on GCP?** BigQuery.
- **Already on Azure, want a unified warehouse + big data + pipeline platform, or need to query data lake files directly?** Azure Synapse (or evaluate Microsoft Fabric for new builds).
- **Hybrid pattern most teams actually use:** OLTP database (Postgres/MySQL/MSSQL) for the application → CDC/batch ELT → OLAP warehouse (BigQuery/Synapse/Snowflake) for analytics and BI, exactly as described in the ETL/ELT cheatsheet's medallion architecture.
