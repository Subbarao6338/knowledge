---
layout: default
title: "Qdrant Cheatsheet"
---

# Qdrant Cheatsheet

Qdrant is a production-grade, high-performance vector database written in Rust. It excels in managing dense vectors, sparse vectors, payloads, and complex filtering rules for Retrieval-Augmented Generation (RAG).

---

## 1. Collection Management

Collections are equivalent to relational tables. They group vectors of a specific dimension and distance metric.

### Python API Setup
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Initialize local or cloud client
client = QdrantClient(url="http://localhost:6333")

# Create a collection for dense embeddings
client.create_collection(
    collection_name="knowledge_vault",
    vectors_config=VectorParams(
        size=1536,  # Matches text-embedding-3-small dimensions
        distance=Distance.COSINE
    )
)
```

### Distance Metrics Reference
- **Cosine:** `Distance.COSINE` — Measures angular similarity (best for normalized embeddings).
- **Dot Product:** `Distance.DOT` — Fast, useful if vectors are pre-normalized.
- **Euclidean:** `Distance.EUCLID` — Classic L2 distance (best for structural/coordinates vectors).

---

## 2. Ingesting Vectors with Payloads

Insert high-dimensional vectors accompanied by structured payload metadata (JSON format) to support precise pre-filtering.

```python
from qdrant_client.models import PointStruct

# Upsert sample documents with payloads
client.upsert(
    collection_name="knowledge_vault",
    wait=True,
    points=[
        PointStruct(
            id=1,
            vector=[0.05] * 1536,  # 1536-dimensional embedding vector
            payload={
                "document_title": "Enterprise SRE Manual",
                "department": "infrastructure",
                "severity_level": "critical",
                "revision_year": 2026,
                "is_active": True
            }
        ),
        PointStruct(
            id=2,
            vector=[0.12] * 1536,
            payload={
                "document_title": "Marketing Pipeline Guidelines",
                "department": "growth",
                "severity_level": "low",
                "revision_year": 2025,
                "is_active": True
            }
        )
    ]
)
```

---

## 3. Advanced Filtering & Search Queries

Qdrant supports highly advanced logical filtering (Pre-filtering) before executing the approximate nearest neighbor (ANN) vector search.

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range

# Perform vector search with combined metadata pre-filtering
search_result = client.search(
    collection_name="knowledge_vault",
    query_vector=[0.05] * 1536,
    query_filter=Filter(
        must=[
            FieldCondition(
                key="department",
                match=MatchValue(value="infrastructure")
            ),
            FieldCondition(
                key="is_active",
                match=MatchValue(value=True)
            )
        ],
        must_not=[
            FieldCondition(
                key="severity_level",
                match=MatchValue(value="low")
            )
        ],
        should=[
            FieldCondition(
                key="revision_year",
                range=Range(gte=2025)
            )
        ]
    ),
    limit=5,
    with_payload=True,
    with_vectors=False
)

# Output results
for hit in search_result:
    print(f"ID: {hit.id} | Score: {hit.score:.4f} | Title: {hit.payload['document_title']}")
```

---

## 4. Payload Indexing for Scaling

To maintain sub-millisecond query latency at scale (millions of points), create indexes on payload fields to bypass linear scanning.

| Index Type | Use Case | Python Command |
| :--- | :--- | :--- |
| **Keyword Index** | Exact matches, tags, categories. | `client.create_payload_index(..., field_name="department", field_schema="keyword")` |
| **Integer / Float Index** | Numeric range filtering (`gte`, `lt`). | `client.create_payload_index(..., field_name="revision_year", field_schema="integer")` |
| **Boolean Index** | Binary status flags (`True`/`False`). | `client.create_payload_index(..., field_name="is_active", field_schema="bool")` |
| **Full-text Index** | Wildcards, token matches on titles. | `client.create_payload_index(..., field_name="document_title", field_schema="text")` |
