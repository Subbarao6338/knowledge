---
layout: default
title: "OpenRefine Cheatsheet"
---

# OpenRefine Cheatsheet

OpenRefine is a powerful, free, open-source tool for working with messy data: cleaning it, transforming it from one format into another, and extending it with web services and external data.

---

## 1. General Refine Expression Language (GREL) Syntax

GREL is the native functional script engine inside OpenRefine, used to execute operations across table rows and columns.

### Core String Cleanups
```javascript
// Remove leading/trailing whitespaces and collapse multi-spaces
value.trim().replace(/\s+/, " ")

// Extract string elements using Regex split patterns
value.split("@")[1]

// Replace a specific character sequence
value.replace("-", "/")

// Convert text representations to Title Case format
value.toTitlecase()

// Capitalize only the first letter
value.toLowercase().replace(/^[a-z]/, function(m) { return m.toUpperCase(); })
```

### Type Conversions & Safe Checking
```javascript
// Convert messy string values to standard numbers or fallback
value.toNumber()

// Safe Datetime Parse from ISO format
value.toDate("yyyy-MM-dd")

// Conditional check (If blank or null, set a fallback value)
if(value == null, "Unknown", value)

// Check if cell is empty or contains only spaces
coalesce(value.trim(), "").length() == 0
```

### Advanced Array & JSON Manipulation
```javascript
// Parse a JSON string and extract a nested key
value.parseJson().get("address").get("postalCode")

// Filter array entries matching a regex pattern
filter(value.split(","), x, x.match(/.*@company\.com/)).join(",")

// Map across array elements to format each item
forEach(value.split(";"), item, item.trim().toTitlecase()).join("; ")
```

---

## 2. Advanced Multi-Row & Cross-Project Operations

OpenRefine allows you to toggle your dataset view between **Rows** and **Records** (for multi-row grouping/hierarchy).

- **Fill Down:** Copies the value of a populated parent cell down through all subsequent empty cell records. (Navigate to `Edit cells` -> `Fill down`).
- **Blank Out:** Converts duplicate sequential cells into blank fields to build structured parent-child groupings. (Navigate to `Edit cells` -> `Blank out`).
- **Transpose Columns to Rows:** Flattens wide tables into tall datasets.

### Cross-Project Data Matching (`cross`)
Retrieve matching cell data from a completely different open project in your OpenRefine instance:
```javascript
// Syntax: cell.cross("Other Project Name", "Matching Key Column")[0].cells["Target Column"].value
cell.cross("Customer Contacts", "Customer ID")[0].cells["Email Address"].value
```

---

## 3. Data Clustering & Phonetic Algorithms

OpenRefine offers powerful clustering algorithms to group near-duplicate spellings automatically.

### Key Collision Methods
These methods are extremely fast and group strings that resolve to the same "fingerprint" representation:
- **Fingerprint:** Lowercases, strips punctuation, splits into tokens, sorts alphabetically, and joins. Resolves `Rao, Subba` vs `Subba Rao`.
- **N-Gram Fingerprint:** Generates n-gram segments, removes duplicates, sorts, and joins. Perfect for catching minor typing gaps.
- **Metaphone3:** Phonetic algorithm that matches words by how they sound in English. Groups `Catherine` vs `Katherine`.
- **Cologne Phonetic:** Optimized phonetic matching specifically for German vocal structures.

### Nearest Neighbor Methods
Slower, but measures the actual distance metric between strings:
- **Levenshtein Distance:** Counts the minimum number of single-character edits (insertions, deletions, substitutions) required to change one string into another.
- **PPM (Prediction by Partial Matching):** Information-theoretic metric useful for long phrases and sentences.

---

## 4. HTML/XML Scraping and Element Extraction

Use GREL to parse raw web contents or files imported directly into a column:

```javascript
// Parse raw HTML and select all list item (<li>) text contents
value.parseHtml().select("li").join(" | ")

// Extract the "href" attribute of an anchor tag (<a>) inside a specific class div
value.parseHtml().select("div.profile-card a")[0].htmlAttr("href")

// Select the raw text of the first header tag (<h1>)
value.parseHtml().select("h1")[0].htmlText()
```

---

## 5. Reconciliation Service API Specification

Reconciliation lets you match your local unstructured string text to professional taxonomy registers (such as Wikidata, DBpedia, or corporate entities database).

A standard custom Reconciliation Service accepts standard JSON query objects:
```json
{
  "q0": {
    "query": "Google LLC",
    "limit": 3,
    "type": "/organization/company"
  },
  "q1": {
    "query": "Atlassian Corp",
    "limit": 3
  }
}
```

The service returns candidates matched with standard scores and IDs:
```json
{
  "q0": {
    "result": [
      {
        "id": "Q95",
        "name": "Google",
        "score": 98.5,
        "match": true,
        "type": [
          {"id": "/organization/company", "name": "Company"}
        ]
      }
    ]
  }
}
```
