---
layout: default
title: "AWS Cloud Services Cheatsheet"
---

# AWS Cloud Services Cheatsheet

## AWS Lambda (Serverless Compute)

```bash
# Deploy / Update Lambda code package
aws lambda update-function-code \
    --function-name my-serverless-function \
    --zip-file fileb://function_payload.zip

# Invoke function from local CLI
aws lambda invoke \
    --function-name my-serverless-function \
    --payload '{"key": "value"}' \
    output_response.json
```

- **Concurrency types:** Reserved concurrency (assigns specific execution pool limits to ensure no system starvation) vs Provisioned concurrency (keeps runtimes warm to completely bypass cold starts).

---

## AWS S3 (Simple Storage Service)

```bash
# Copy file to s3 bucket with server-side encryption
aws s3 cp local_report.pdf s3://my-enterprise-bucket/reports/ --sse AES256

# Synchronize directories (mirroring files)
aws s3 sync ./local_assets s3://my-enterprise-bucket/assets/ --delete

# LifeCycle Rules structure configuration
# Transitions items automatically to S3 Glacier Deep Archive after N days for optimal cost efficiency.
```

---

## AWS EC2 (Elastic Compute Cloud) & RDS (Relational Database Service)

```bash
# Start and Stop EC2 instances safely
aws ec2 start-instances --instance-ids i-0123456789abcdef0
aws ec2 stop-instances --instance-ids i-0123456789abcdef0

# Create manual RDS Snapshot for Disaster Recovery backup
aws rds create-db-snapshot \
    --db-instance-identifier my-prod-database \
    --db-snapshot-identifier my-manual-snapshot-july-2026
```

---

## AWS Athena (Serverless SQL Query Engine)

Athena enables fast, serverless query execution directly against raw storage (S3/Parquet/CSV) using standard ANSI SQL.

```sql
-- DDL schema creation for partition queries
CREATE EXTERNAL TABLE IF NOT EXISTS flight_database.raw_logs (
  flight_id string,
  origin string,
  destination string,
  passengers int
)
PARTITIONED BY (year string, month string)
STORED AS PARQUET
LOCATION 's3://my-enterprise-bucket/raw_flight_logs/';

-- Refresh database partition structure
MSCK REPAIR TABLE flight_database.raw_logs;
```

---

## AWS EKS (Elastic Kubernetes Service)

```bash
# Update local kubeconfig context to point securely to your cluster
aws eks update-kubeconfig --region us-east-1 --name prod-cluster-eks

# Verify connection and namespace states
kubectl get namespaces
```
