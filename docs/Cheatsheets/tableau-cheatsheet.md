---
layout: default
title: "Tableau Cheatsheet"
---

# Tableau Cheatsheet

Tableau is a popular business intelligence and data visualization tool used to analyze and present complex data.

---

## 1. Common Tableau Calculation Functions

Tableau uses calculated fields to execute dynamic math, data transformations, and custom logic.

### String Manipulation
```tableau
// Extract email domain name
MID([Email], FIND([Email], "@") + 1)

// Title case naming standard
UPPER(LEFT([First Name], 1)) + LOWER(MID([First Name], 2))
```

### Date Calculations
```tableau
// Calculate difference in days between order and delivery date
DATEDIFF('day', [Order Date], [Ship Date])

// Extract year from a date field
YEAR([Order Date])

// Check if transaction happened in current month
DATEDIFF('month', [Transaction Date], TODAY()) = 0
```

### Logic / Conditional
```tableau
// Create revenue classification buckets
IF [Sales] > 10000 THEN "High-Tier"
ELSEIF [Sales] > 1000 THEN "Mid-Tier"
ELSE "Low-Tier"
END
```

---

## 2. Level of Detail (LOD) Expression Syntaxes

LOD expressions allow you to compute values at the data source level and visualization level without having to pull all details into your charts.

- **FIXED:** Computes the aggregate value using only the specified dimensions, ignoring any filters or visualized detail level.
  ```tableau
  { FIXED [Region] : SUM([Sales]) }
  ```
- **INCLUDE:** Computes the aggregate value using the specified dimensions *plus* whatever dimensions are currently in the visualization.
  ```tableau
  { INCLUDE [Product Category] : AVG([Sales]) }
  ```
- **EXCLUDE:** Ignores the specified dimensions when calculating the aggregate value, even if they are shown in the visualization.
  ```tableau
  { EXCLUDE [Segment] : SUM([Sales]) }
  ```
