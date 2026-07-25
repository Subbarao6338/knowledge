---
layout: default
title: "Data Engineering Cheatsheet"
---

# Data Engineering Cheatsheet

Data Engineering is the practice of designing, building, and maintaining systems for collecting, storing, transforming, and analyzing data at scale.

---

## 1. Relational (OLTP) vs Analytical (OLAP) Systems

| Feature | OLTP (On-Line Transactional Processing) | OLAP (On-Line Analytical Processing) |
|---|---|---|
| **Primary Use** | Real-time database operations (Inserts/Updates) | Heavy analytics, trend analysis, reporting |
| **Data Schema** | Highly normalized (3rd Normal Form) to avoid redundancy | Denormalized (Star / Snowflake schemas) |
| **Storage Style** | Row-oriented (e.g., PostgreSQL, MySQL) | Column-oriented (e.g., Snowflake, BigQuery, Redshift) |
| **Query Profile** | Fast lookup of single records by primary key | Multi-column aggregations over millions of rows |

---

## 2. Distributed Compute Core Concepts

To process massive datasets that exceed the memory and storage capacity of a single machine, analytical systems distribute the workload across a cluster of nodes.

```text
               Driver / Master Node
             /          |           \
     Worker Node    Worker Node    Worker Node
```

- **Partitioning:** Splitting a massive table into smaller physical chunks (files/directories) based on a partition column (e.g., `year` or `date`). This allows query engines to skip unneeded data, speeding up execution and reducing costs.
- **Shuffling:** The process of redistributing data across worker nodes in a cluster (typically during a join or group-by operation). Shuffling requires heavy network I/O and is the most common performance bottleneck in distributed compute engines like Apache Spark.
- **Broadcast Join:** An optimized join strategy where the master node sends a copy of a small table to all worker nodes. This allows them to join the small table to partition subsets of a large table locally, completely avoiding a shuffle step.
