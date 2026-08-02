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

// Check if string contains a substring (case-insensitive)
CONTAINS(LOWER([Product Name]), "pro")
```

### Date Calculations
```tableau
// Calculate difference in days between order and delivery date
DATEDIFF('day', [Order Date], [Ship Date])

// Extract year from a date field
YEAR([Order Date])

// Check if transaction happened in current month
DATEDIFF('month', [Transaction Date], TODAY()) = 0

// Find first day of the current month
DATETRUNC('month', TODAY())

// Add 30 days to order date
DATEADD('day', 30, [Order Date])
```

### Logic / Conditional
```tableau
// Create revenue classification buckets
IF [Sales] > 10000 THEN "High-Tier"
ELSEIF [Sales] > 1000 THEN "Mid-Tier"
ELSE "Low-Tier"
END

// Handle null values gracefully
ZN([Sales]) // Returns 0 if sales is null, otherwise returns sales value
IFNULL([Region], "Global") // Returns Global if Region is null
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

### Advanced LOD: Cohort Analysis (First Purchase Date)
Find the first purchase date for every customer, regardless of current filters:
```tableau
{ FIXED [Customer ID] : MIN([Order Date]) }
```

---

## 3. Advanced Table Calculations

Table calculations are computed locally in Tableau's cache based on the active rows and columns in the view.

```tableau
// 1. Calculate a running total of Sales across the view
RUNNING_SUM(SUM([Sales]))

// 2. Calculate a moving average of Sales (previous 2 periods + current period)
WINDOW_AVG(SUM([Sales]), -2, 0)

// 3. Percent of Total Sales in active partition
SUM([Sales]) / WINDOW_SUM(SUM([Sales]))

// 4. Retrieve value from the previous row or partition offset
LOOKUP(SUM([Sales]), -1)

// 5. Calculate percentage growth compared to previous period
(SUM([Sales]) - LOOKUP(SUM([Sales]), -1)) / ABS(LOOKUP(SUM([Sales]), -1))
```

---

## 4. Parameter Control & Custom Interactions

Parameters allow users to dynamically change variable values inside calculations and charts, making dashboards interactive.

### Dynamic Metric Selector Calculation
Use a string parameter named `[Select Metric]` containing values `"Sales"` and `"Profit"` to swap visual measures:
```tableau
CASE [Select Metric]
  WHEN "Sales" THEN [Sales]
  WHEN "Profit" THEN [Profit]
  ELSE 0
END
```

---

## 5. Dashboard Performance Optimization Checklist

- **Use Context Filters:** By default, all filters in Tableau are computed independently. Adding a filter "To Context" forces Tableau to compute that filter first, slicing the dataset before other filters run.
- **Limit Marks Count:** Avoid creating charts with 100,000+ points/marks, as rendering browser SVG points degrades visual rendering speeds.
- **Optimize Extracts:** Always aggregate data to visible dimensions and hide unused columns when creating `.hyper` local extracts.
- **Reduce Nested LODs:** FIXED LODs bypass the filter pipeline and trigger heavy underlying subqueries. Limit nesting FIXED LOD calculations.
