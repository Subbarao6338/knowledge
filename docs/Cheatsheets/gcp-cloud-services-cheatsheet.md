---
layout: default
title: "GCP Cloud Services Cheatsheet"
---

# GCP Cloud Services Cheatsheet

## GCP Cloud Run & Cloud Run Functions

GCP Cloud Run runs highly scalable, stateless containerized workloads. GCP Cloud Run Functions (formerly Cloud Functions) allows deploying lightweight, event-driven snippet functions without managing docker containers directly.

```bash
# Deploy a container to Cloud Run
gcloud run deploy my-web-app \
    --image europe-west3-docker.pkg.dev/my-proj/repo/app:v1.0 \
    --platform managed \
    --region europe-west3 \
    --allow-unauthenticated

# Deploy a Cloud Run Function (Python 3.10 event-driven background function)
gcloud functions deploy my-event-handler \
    --gen2 \
    --runtime=python310 \
    --region=europe-west3 \
    --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
    --trigger-event-filters="bucket=my-events-bucket"
```

---

## GCP Vertex AI

Vertex AI is GCP's unified developer platform for training machine learning models, deploying APIs, and building generative AI applications.

```python
# Invoke Gemini Pro LLM using Vertex AI SDK
import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="my-project-id", location="us-central1")
model = GenerativeModel("gemini-1.5-pro")

response = model.generate_content(
    "Suggest 3 main target strategies for enterprise cost optimization in Cloud."
)
print(response.text)
```

---

## GCP BigQuery

BigQuery is an enterprise-scale serverless data warehouse using column store partitions.

```sql
-- Query partition table efficiently without full table scans
SELECT
  user_id,
  SUM(revenue) AS total_revenue
FROM `my-project.sales_dataset.daily_transactions`
WHERE _PARTITIONDATE = '2026-07-17' -- Partition filter (saves costs)
GROUP BY user_id
LIMIT 100;
```

---

## GCP GCS (Google Cloud Storage) & Cloud SQL

```bash
# Upload assets using gsutil (or gsutil rsync)
gsutil cp -v -r ./data_directory gs://my-assets-bucket/backups/

# Connect securely to private Cloud SQL database using proxy
./cloud-sql-proxy my-project:us-central1:my-instance --port 5432
```

---

## GCP GCE (Compute Engine) & GKE (Google Kubernetes Service)

```bash
# Start/Stop virtual machines
gcloud compute instances start prod-vm-worker --zone=europe-west3-a

# Fetch cluster access credentials for GKE
gcloud container clusters get-credentials my-cluster --zone=us-central1-a --project=my-project-id
```
