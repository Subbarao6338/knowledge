# ETL / ELT Pipelines Cheatsheet

## ETL vs ELT

| | ETL | ELT |
|---|---|---|
| Order | Extract → **Transform** → Load | Extract → **Load** → Transform |
| Transform happens | Before loading, in a separate processing layer (Spark, Python) | After loading, inside the target warehouse (SQL, dbt) |
| Best for | Legacy systems, heavy pre-processing, sensitive data needing masking before storage | Modern cloud warehouses (Snowflake, BigQuery, Redshift) with cheap compute |
| Raw data retained? | Often not — only transformed data is kept | Yes — raw data lands first, transformations are reproducible/re-runnable |
| Tooling | Informatica, SSIS, custom Spark/Python jobs | Fivetran/Airbyte (extract+load) + dbt (transform) |
| Flexibility | Transform logic is harder to change after the fact | Easy to re-run transforms against raw data as requirements evolve |

Modern data platforms trend toward ELT: load raw data cheaply into a warehouse/lake, then transform with SQL-based tools (dbt) that version, test, and document the logic.

---

## Core Pipeline Stages

### 1. Extract

```text
Sources: databases (OLTP), APIs, event streams (Kafka), files (CSV/Parquet/JSON), SaaS apps (Salesforce, HubSpot)
```

- **Full extract** — pull entire dataset each run. Simple, but expensive at scale.
- **Incremental extract** — pull only new/changed records since last run, using:
  - A watermark column (`updated_at > last_run_timestamp`)
  - Change Data Capture (CDC) — reading database transaction logs (Debezium, AWS DMS) for row-level inserts/updates/deletes in near real time
  - Cursor-based API pagination with a stored "last seen" cursor/offset

```python
# Simple incremental extract pattern
last_run = get_last_watermark()
query = f"SELECT * FROM orders WHERE updated_at > '{last_run}'"
new_rows = run_query(query)
save_watermark(new_rows["updated_at"].max())
```

### 2. Load

- **Load raw/staged data first** (ELT) into a landing zone — object storage (S3/GCS) or a raw schema in the warehouse — before any transformation. Preserves an auditable source of truth.
- **Load patterns:**
  - **Append-only** — every run inserts new rows, nothing is overwritten. Good for immutable event data.
  - **Truncate-and-load** — wipe the target table and reload fully. Simple, safe for small reference tables.
  - **Upsert / merge** — insert new rows, update changed rows, based on a primary/business key. Standard for slowly-changing dimension data.
  - **SCD Type 2** — preserve history by inserting a new row with `valid_from`/`valid_to` timestamps instead of overwriting, when a tracked attribute changes.

```sql
-- Upsert pattern (MERGE), works in most modern warehouses
MERGE INTO target t
USING staging s
ON t.id = s.id
WHEN MATCHED THEN UPDATE SET t.value = s.value, t.updated_at = s.updated_at
WHEN NOT MATCHED THEN INSERT (id, value, updated_at) VALUES (s.id, s.value, s.updated_at);
```

### 3. Transform

- Cleaning: type casting, deduplication, null handling, standardizing formats (dates, currencies, casing).
- Enrichment: joins with reference/dimension tables, derived columns, business logic.
- Modeling: building fact/dimension tables (star schema), aggregations, rollups.
- In ELT, this is typically SQL run inside the warehouse (often via dbt), broken into layers:

```text
raw/staging  -->  intermediate  -->  marts (business-facing tables)
```

---

## Common Architecture Patterns

```text
Batch pipeline:
  Source DB --(scheduled extract)--> Landing (S3/GCS) --> Staging table --> Transform (dbt/SQL) --> Marts --> BI tool

Streaming pipeline:
  Source events --> Kafka/Kinesis --> Stream processor (Flink/Spark Structured Streaming) --> Sink (warehouse/lake)

CDC-based pipeline:
  DB transaction log --> Debezium/DMS --> Kafka topic --> Sink connector --> Raw table (mirrors source row-by-row changes)

Lakehouse pattern (medallion architecture):
  Bronze (raw, as-landed) --> Silver (cleaned, deduplicated, conformed) --> Gold (aggregated, business-ready)
```

## Medallion Architecture (Bronze / Silver / Gold)

| Layer | Purpose | Characteristics |
|---|---|---|
| **Bronze** | Raw ingested data | Untransformed, append-only, schema-on-read, full history |
| **Silver** | Cleaned & conformed | Deduplicated, typed, nulls handled, joined to reference data |
| **Gold** | Business-level aggregates | Star schema / wide tables, ready for BI and reporting |

---

## Idempotency & Reliability

A pipeline is **idempotent** if running it twice with the same input produces the same result — critical for safe retries.

```python
# Non-idempotent: re-running duplicates rows
INSERT INTO orders SELECT * FROM staging;

# Idempotent: MERGE/upsert based on a key, or delete-then-insert for a specific partition
DELETE FROM orders WHERE load_date = '2026-07-17';
INSERT INTO orders SELECT * FROM staging WHERE load_date = '2026-07-17';
```

Other reliability practices:
- **Partition by load date/batch id** so a failed run only affects one partition, making reprocessing safe and cheap.
- **Watermarking + checkpointing** — track exactly what's been processed so retries resume, not restart.
- **Dead-letter queues** — route malformed records to a separate table/topic instead of failing the whole batch.
- **Schema evolution handling** — decide upfront: fail loudly on unexpected schema changes, or evolve automatically (add columns, widen types).

---

## Data Quality Checks

```python
# Common checks to build into a pipeline
assert df["id"].is_unique
assert df["amount"].notnull().all()
assert (df["amount"] >= 0).all()
assert df["status"].isin(["active", "inactive", "pending"]).all()
row_count_today = len(df)
assert row_count_today > 0.5 * avg_row_count_last_7_days   # volume anomaly check
```

Common quality dimensions: **completeness** (no unexpected nulls), **uniqueness** (keys aren't duplicated), **validity** (values in expected ranges/enums), **consistency** (foreign keys resolve), **timeliness** (data isn't stale), **accuracy** (matches source of truth).

Tools: **dbt tests** (`unique`, `not_null`, `accepted_values`, `relationships`), **Great Expectations**, **Soda**, custom assertion scripts as pipeline steps that fail the DAG on violation.

```yaml
# dbt schema test example
models:
  - name: orders
    columns:
      - name: order_id
        tests: [unique, not_null]
      - name: status
        tests:
          - accepted_values:
              values: ['pending', 'shipped', 'delivered', 'cancelled']
```

---

## Orchestration Concepts

- **DAG (Directed Acyclic Graph)** — tasks with defined dependencies, no cycles. The backbone of tools like Airflow, Dagster, Prefect.
- **Scheduling** — cron-based (`0 6 * * *`) or event/sensor-triggered (e.g., "run when a file lands in S3").
- **Backfilling** — re-running a pipeline for historical date ranges, e.g., after a bug fix or new column addition.
- **Retries & alerting** — automatic retries with backoff on transient failures; alerting (Slack/email/PagerDuty) on final failure.
- **SLAs** — expected completion time for a pipeline/task; breaches should alert.

---

## Slowly Changing Dimensions (SCD)

| Type | Behavior |
|---|---|
| **Type 0** | Never update — original value retained forever |
| **Type 1** | Overwrite — old value is lost, no history |
| **Type 2** | Add new row with validity dates — full history preserved |
| **Type 3** | Add a new column for "previous value" — limited history (one prior value) |

```sql
-- SCD Type 2 pattern
UPDATE dim_customer
SET valid_to = CURRENT_DATE, is_current = FALSE
WHERE customer_id = :id AND is_current = TRUE AND (attribute changed);

INSERT INTO dim_customer (customer_id, attribute, valid_from, valid_to, is_current)
VALUES (:id, :new_attribute, CURRENT_DATE, NULL, TRUE);
```

---

## Star Schema Basics (common ELT target model)

```text
        dim_customer
             |
dim_date -- fact_orders -- dim_product
             |
         dim_store
```

- **Fact table** — transactional/event grain (one row per order, per event), holds foreign keys + measures (amounts, counts).
- **Dimension table** — descriptive attributes (customer name, product category), typically smaller, changes less often.
- Fact tables are usually append-heavy and large; dimension tables use SCD patterns to track attribute changes.

---

## Tooling Landscape

| Category | Examples |
|---|---|
| Extract & Load (managed) | Fivetran, Airbyte, Stitch |
| Orchestration | Apache Airflow, Dagster, Prefect, Azure Data Factory |
| Transformation (in-warehouse) | dbt, SQL scripts, Dataform |
| Processing engines (heavy transform) | Apache Spark, Flink, Beam/Dataflow |
| Streaming | Kafka, Kinesis, Pub/Sub |
| CDC | Debezium, AWS DMS, Fivetran CDC connectors |
| Warehouses/Lakehouses | Snowflake, BigQuery, Redshift, Databricks (Delta Lake) |
| Data quality | Great Expectations, dbt tests, Soda |
| Catalog / lineage | DataHub, Amundsen, OpenLineage |

---

## Practical Checklist for a New Pipeline

1. Define the grain of the target table (one row per what?).
2. Choose full vs incremental extraction; identify a reliable watermark/cursor.
3. Decide load strategy — append, upsert, or SCD Type 2 — based on how the target is used.
4. Make every load step idempotent (partition-based delete+insert or merge on a key).
5. Add data quality tests before data reaches downstream consumers.
6. Add monitoring: row counts, freshness, and failure alerting.
7. Document lineage — where data comes from, what transforms it, who consumes it.
8. Plan for backfill and schema evolution from day one, not as an afterthought.
