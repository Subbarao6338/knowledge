---
layout: default
title: "Databricks Cheatsheet"
---

# Databricks Cheatsheet

Databricks is a unified, cloud-based data analytics platform built on Apache Spark. It provides an interactive workspace for data engineers, data scientists, and business analysts to collaborate.

---

## 1. Delta Lake Optimization Commands

Delta Lake is the default storage layer in Databricks, providing ACID transactions, version control, and performance enhancements over raw Parquet files.

```sql
-- Compact small files automatically in Delta Tables (major performance boost)
OPTIMIZE delta_db.sales_data;

-- Z-Ordering by high-cardinality search columns to accelerate downstream queries
OPTIMIZE delta_db.sales_data
ZORDER BY (customer_id, country);

-- Purge old file versions no longer needed (defaults to keeping 7 days of history)
-- CAUTION: Bypasses the "Time Travel" version restore feature
VACUUM delta_db.sales_data RETAIN 168 HOURS;
```

## 2. Spark/Delta Table Time Travel Queries

Delta Lake keeps transaction histories, allowing you to query historical table states or roll back errors.

```sql
-- Query table exactly as it looked on a specific timestamp
SELECT * FROM delta_db.sales_data TIMESTAMP AS OF '2026-07-10 10:00:00';

-- Query table by specific sequential version number
SELECT * FROM delta_db.sales_data VERSION AS OF 12;

-- Restore a broken table state
RESTORE TABLE delta_db.sales_data TO VERSION AS OF 10;
```

## 3. Unity Catalog (UC) Governance

Unity Catalog is a unified governance solution for files, databases, tables, and AI assets across your Databricks workspace.

```sql
-- Grant read permission to an engineering group
GRANT SELECT ON TABLE main_catalog.silver_schema.sales_facts TO `data-engineering-group`;

-- Standardized UC namespace mapping:
-- catalog.schema.table
```
