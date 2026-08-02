---
layout: default
title: "Databricks Cheatsheet"
---

# Databricks Cheatsheet

Databricks is a unified, cloud-based data analytics platform built on Apache Spark. It provides an interactive workspace for data engineers, data scientists, and business analysts to collaborate.

---

## 1. Delta Lake Optimization & Storage Engine

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

### Table Properties for Auto-Optimization (Auto-Compact & Optimize Write)
Configure tables to automatically manage files sizes on insert:
```sql
ALTER TABLE delta_db.sales_data SET TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);
```

---

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

---

## 3. DBUtils Workspace & Storage Utilities

`dbutils` is a native suite of helper tools inside Databricks to manage file systems, secret scopes, and notebook parameters.

### DBUtils File System (`fs`) Examples (Python)
```python
# List files in a DBFS path
dbutils.fs.ls("/mnt/data-lake/raw/")

# Copy a directory or file recursively
dbutils.fs.cp("/mnt/data-lake/raw/", "/mnt/data-lake/backup/", recurse=True)

# Mount an Azure Blob storage or AWS S3 Bucket
dbutils.fs.mount(
  source = "wasbs://container@storageaccount.blob.core.windows.net",
  mount_point = "/mnt/my-container",
  extra_configs = {"fs.azure.account.key.storageaccount.blob.core.windows.net": dbutils.secrets.get(scope="my-scope", key="storage-key")}
)
```

### DBUtils Secrets Management
```python
# Fetch a password/token safely from Databricks Secrets Scope (bypassing plaintext configs)
api_token = dbutils.secrets.get(scope="finance-scope", key="stripe-api-token")
```

---

## 4. Performance Tuning & Adaptive Query Execution (AQE)

Adaptive Query Execution (AQE) is a Spark 3.x technology that optimizes query plans dynamically at runtime based on intermediate metrics.

```python
# Enable Adaptive Query Execution (Default: True in modern runtimes)
spark.conf.set("spark.sql.adaptive.enabled", "true")

# Dynamically coalesce shuffle partitions to match sizes (prevents thousands of empty tasks)
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

# Automatically switch to broadcast joins if dynamic partition data is below limit
spark.conf.set("spark.sql.adaptive.localShuffleReader.enabled", "true")
```

---

## 5. MLflow Tracking & Model Registry Integration

MLflow is natively integrated inside Databricks for tracking AI/ML training experiments, hyper-parameters, and model registration.

```python
import mlflow
import mlflow.spark
from sklearn.ensemble import RandomForestRegressor

# Set active experiment path in Workspace
mlflow.set_experiment("/Users/developer@company.com/Sales_Forecasting_RF")

# Start an active training logging run
with mlflow.start_run() as run:
    # Model configuration
    n_estimators = 100
    model = RandomForestRegressor(n_estimators=n_estimators)
    model.fit(X_train, y_train)

    # Log parameters and evaluation metrics
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_metric("rmse", 0.1452)

    # Log the trained model object
    mlflow.sklearn.log_model(model, "random-forest-model")

    # Register the logged model directly to the Unity Catalog / Databricks Registry
    model_uri = f"runs:/{run.info.run_id}/random-forest-model"
    mlflow.register_model(model_uri, "prod_sales_forecaster")
```

---

## 6. Unity Catalog (UC) Governance

Unity Catalog is a unified governance solution for files, databases, tables, and AI assets across your Databricks workspace.

```sql
-- Create a catalogs structure
CREATE CATALOG IF NOT EXISTS prod_catalog;
USE CATALOG prod_catalog;

-- Create schemas inside the catalogs
CREATE SCHEMA IF NOT EXISTS silver_schema;
USE SCHEMA silver_schema;

-- Grant read permission to an engineering group
GRANT SELECT ON TABLE prod_catalog.silver_schema.sales_facts TO `data-engineering-group`;

-- Grant read/write permissions for specific schemas
GRANT USAGE, CREATE ON SCHEMA prod_catalog.silver_schema TO `data-science-group`;

-- Standardized UC namespace mapping:
-- catalog.schema.table
```
