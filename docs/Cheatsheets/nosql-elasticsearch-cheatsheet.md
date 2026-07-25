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
