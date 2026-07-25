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
```

### Type Conversions & Safe Checking
```javascript
// Convert messy string values to standard numbers or fallback
value.toNumber()

// Safe Datetime Parse from ISO format
value.toDate("yyyy-MM-dd")

// Conditional check (If blank or null, set a fallback value)
if(value == null, "Unknown", value)
```

---

## 2. Advanced Multi-Row Transformations

OpenRefine allows you to toggle your dataset view between **Rows** and **Records** (for multi-row grouping/hierarchy).

- **Fill Down:** Copies the value of a populated parent cell down through all subsequent empty cell records. (Navigate to `Edit cells` -> `Fill down`).
- **Blank Out:** Converts duplicate sequential cells into blank fields to build structured parent-child groupings. (Navigate to `Edit cells` -> `Blank out`).
- **Transpose Columns to Rows:** Flattens wide tables into tall datasets.
