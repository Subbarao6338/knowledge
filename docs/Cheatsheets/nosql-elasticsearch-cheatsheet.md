---
layout: default
title: "NoSQL & Elasticsearch Cheatsheet"
---

# NoSQL & Elasticsearch Cheatsheet

## MongoDB (Document Store)

```javascript
// Connect and insert
db.users.insertOne({
  username: "rao_dev",
  role: "SRE",
  skills: ["Python", "Kubernetes", "AWS"],
  metadata: { active: true, created_at: new ISODate() }
});

// Query / Filter
db.users.find({ skills: "Kubernetes" });

// Update attribute safely in nested sub-documents
db.users.updateOne(
  { username: "rao_dev" },
  { $set: { "metadata.active": false } }
);

// Aggregate Pipeline (Match -> Group -> Sort)
db.users.aggregate([
  { $match: { "metadata.active": false } },
  { $group: { _id: "$role", total: { $sum: 1 } } },
  { $sort: { total: -1 } }
]);
```

---

## Redis (In-Memory Key-Value & Cache Store)

```bash
# Set key with TTL of 60 seconds
SET session_token "a9f3b7..." EX 60

# Retrieve key
GET session_token

# List append / queue patterns
LPUSH active_jobs "job_123"
RPOP active_jobs
```

---

## Elasticsearch (Search Engine / Document Store)

Elasticsearch is a distributed, JSON-based search and analytics engine.

```json
// Index (Create/Update) Document via REST API
PUT /users/_doc/1
{
  "username": "rao_dev",
  "role": "SRE",
  "bio": "Extremely skilled software and platform engineer specializing in cloud automation."
}

// Full Text Search Query
POST /users/_search
{
  "query": {
    "match": {
      "bio": "cloud automation"
    }
  }
}
```

---

## Advanced Elasticsearch Query DSL

Elasticsearch provides a rich Query Domain Specific Language (DSL) based on JSON.

### Match Query (Full-Text) vs Term Query (Exact Match)
* **Match:** Analyzes the search string and queries full-text fields (e.g., matching "Cloud Automation" in a bio).
* **Term:** Looks for exact values in keyword fields (e.g., UUIDs, statuses, or exact usernames).

### Compound Boolean Query (`bool`)
```json
POST /users/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "bio": "engineer" } }
      ],
      "should": [
        { "match": { "bio": "python" } }
      ],
      "must_not": [
        { "term": { "role.keyword": "Junior" } }
      ],
      "filter": [
        { "term": { "status": "active" } },
        { "range": { "created_at": { "gte": "now-30d/d" } } }
      ]
    }
  }
}
```
* **must:** Document must match. Affects search score.
* **should:** Document doesn't have to match, but if it does, it increases the relevance score.
* **must_not:** Document must NOT match.
* **filter:** Exact matching. Does NOT affect search score and is fully cached for speed.

---

## Index Mapping Configuration

Explicit mappings define how a document and its fields are stored and indexed under Lucene.

```json
PUT /users
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "username": { "type": "keyword" },
      "role": {
        "type": "text",
        "fields": {
          "keyword": { "type": "keyword", "ignore_above": 256 }
        }
      },
      "bio": { "type": "text", "analyzer": "standard" },
      "status": { "type": "keyword" },
      "created_at": { "type": "date" }
    }
  }
}
```

---

## Aggregations Reference

Aggregations summarize your data as metrics, statistics, or buckets (groupings).

```json
POST /users/_search
{
  "size": 0, // We only want aggregation results, not raw search hits
  "aggs": {
    "roles_distribution": {
      "terms": {
        "field": "role.keyword",
        "size": 10
      },
      "aggs": {
        "average_experience": {
          "avg": {
            "field": "years_experience"
          }
        }
      }
    }
  }
}
```

---

## Bulk Indexing API

Perform multiple indexing/deletion operations in a single network request for maximum performance.

```json
POST /_bulk
{ "index" : { "_index" : "users", "_id" : "2" } }
{ "username" : "jane_sre", "role" : "SRE", "bio": "Security analyst and cluster builder", "status": "active" }
{ "delete" : { "_index" : "users", "_id" : "1" } }
```

---

## Cluster Diagnostics

```bash
# Get overall cluster health status (Green, Yellow, Red)
GET /_cluster/health

# List all index allocations, statuses, document counts, and memory footprints
GET /_cat/indices?v

# List of all active cluster nodes
GET /_cat/nodes?v
```
