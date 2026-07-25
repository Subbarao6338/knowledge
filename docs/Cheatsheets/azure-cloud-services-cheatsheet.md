# Azure Cloud Services Cheatsheet

## Azure Storage (Blob & ADLS Gen2)

Azure Blob Storage handles unstructured binary assets, while Azure Data Lake Storage (ADLS Gen2) provides a hierarchical namespace optimized for massive analytic pipelines (e.g., Spark, Databricks).

```bash
# Upload block blob using az CLI
az storage blob upload \
    --account-name mystor_account \
    --container-name logs \
    --name system.log \
    --file ./system.log \
    --auth-mode login

# Fast synchronization of large directories using azcopy
azcopy sync "./local_assets" "https://mystor.blob.core.windows.net/assets?[SAS-TOKEN]" --recursive=true
```

---

## Azure Synapse (Pipelines, Spark & Views)

Azure Synapse Analytics integrates big data processing, data warehousing, and pipeline orchestration under one unified workspace.

- **Synapse Pipelines:** Low-code data integration tool (equivalent to Azure Data Factory) using activities to orchestrate copy tasks, stored procedures, and Notebooks.
- **Synapse Views:** Built over serverless SQL pools to query raw parquet files in the storage account on-the-fly.

```sql
-- Querying ADLS files using serverless OPENROWSET view
CREATE VIEW dbo.ProcessedSalesView AS
SELECT *
FROM OPENROWSET(
    BULK 'https://mystor.dfs.core.windows.net/silver/sales/year=*/month=*/*.parquet',
    FORMAT = 'PARQUET'
) AS [result];
```

---

## Azure Functions (Serverless Compute)

```python
# python HTTP function handler example
import azure.functions as func
import logging

app = func.FunctionApp()

@app.route(route="health_check", auth_level=func.AuthLevel.ANONYMOUS)
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processed an HTTP health check request.')
    return func.HttpResponse("Healthy", status_code=200)
```

---

## Azure AKS (Azure Kubernetes Service)

```bash
# Fetch credentials and merge into local kubeconfig
az aks get-credentials --resource-group my-rg --name prod-aks-cluster

# Confirm node statuses are Ready
kubectl get nodes
```
