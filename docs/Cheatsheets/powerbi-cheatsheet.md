<!-- {% raw %} -->
# Power BI Cheatsheet

## Core Concepts & Architecture

```text
Power BI Desktop     Authoring tool — build data models, queries, visuals, reports (.pbix file)
Power Query (M)          The data transformation/ETL layer inside Desktop ("Get Data" + Query Editor)
Data Model / Tables         Loaded tables + relationships + measures, powered by the VertiPaq columnar engine
DAX                            Formula language for measures, calculated columns, calculated tables
Power BI Service                  app.powerbi.com — cloud platform for publishing, sharing, scheduled refresh
Power BI Report Builder              paginated (pixel-perfect) reports, separate from interactive Desktop reports
Power BI Gateway                        on-premises data gateway for refreshing data behind a firewall (e.g. on-prem SQL Server)
Power BI Mobile                            mobile apps for viewing published reports/dashboards
```

## File & Workspace Structure

```text
.pbix           Power BI Desktop report file (data model + queries + report pages)
.pbit               Power BI template (structure without data)
.pbids                  Power BI data source shortcut file

Workspace           A container in the Service for related reports/datasets/dashboards (like a folder + permissions unit)
App                    A polished, curated bundle of content from a workspace, published for end-user consumption
Dataset (Semantic Model)   The published data model — can be reused across multiple reports
Dashboard                     A single-page pinned-tile summary view, built from one or more reports
```

## Get Data — Common Sources

```text
Home > Get Data > choose source:
  Excel Workbook, CSV/Text, Folder (combine many files), SharePoint Folder
  SQL Server, PostgreSQL, MySQL, Oracle, Snowflake
  Azure SQL Database, Azure Synapse Analytics, Azure Data Lake Storage
  Google BigQuery
  Web (URL-based, incl. web scraping via HTML tables)
  OData Feed, REST API (via Web connector + custom headers)
  SharePoint List, Dataverse, Salesforce, Dynamics 365

Connectivity modes:
  Import        Data copied into Power BI's in-memory VertiPaq engine (fastest, most feature-complete, needs scheduled refresh)
  DirectQuery       Queries sent live to the source on each interaction (real-time, no data duplication, fewer DAX/modeling features)
  Live Connection       Connects directly to an existing Analysis Services / Power BI dataset (no local model, reuses the remote one)
  Composite Model           Mix of Import and DirectQuery tables in the same model (Power BI decides per-query which mode to use)
```

## Power Query (M) — Editor Basics

```text
Home > Transform Data          Opens the Power Query Editor
Applied Steps pane                 Every transformation is a recorded, reorderable, editable step
Advanced Editor                       View/edit the full M code for a query
```

```powerquery-m
// Basic M query structure
let
    Source = Sql.Database("myserver", "mydatabase"),
    FilteredRows = Table.SelectRows(Source, each [amount] > 100),
    RenamedColumns = Table.RenameColumns(FilteredRows, {{"old_name", "new_name"}}),
    AddedColumn = Table.AddColumn(RenamedColumns, "double_amount", each [amount] * 2)
in
    AddedColumn
```

## Common Power Query (M) Transformations

```powerquery-m
Table.SelectRows(Source, each [status] = "active")             // filter rows
Table.RemoveColumns(Source, {"col1", "col2"})                     // remove columns
Table.SelectColumns(Source, {"col1", "col2"})                        // keep only these columns
Table.RenameColumns(Source, {{"old", "new"}})
Table.AddColumn(Source, "NewCol", each [A] + [B])
Table.TransformColumnTypes(Source, {{"amount", type number}, {"date", type date}})
Table.Sort(Source, {{"amount", Order.Descending}})
Table.Distinct(Source)
Table.Group(Source, {"category"}, {{"Total", each List.Sum([amount]), type number}})
Table.PromoteHeaders(Source)                     // first row -> column headers
Table.Pivot(Source, List.Distinct(Source[Category]), "Category", "Value")
Table.Unpivot(Source, {"Jan", "Feb", "Mar"}, "Month", "Value")        // wide -> long/tall format
Table.Combine({Table1, Table2})                     // append (union) tables
Table.NestedJoin(Table1, "Key1", Table2, "Key2", "NewCol", JoinKind.LeftOuter)     // merge/join
Table.ExpandTableColumn(Merged, "NewCol", {"col_from_table2"})       // flatten a merged/nested column

Text.Trim([col])
Text.Upper([col]) / Text.Lower([col])
Text.Combine({[a], [b]}, " ")
Text.Split([col], ",")
Text.BeforeDelimiter([col], "@") / Text.AfterDelimiter([col], "@")

Date.Year([date]) / Date.Month([date]) / Date.Day([date])
Date.AddDays([date], 7)
DateTime.LocalNow()

if [amount] > 100 then "High" else "Low"          // conditional column logic
try [amount] / [qty] otherwise 0                      // error handling
```

**Common UI operations behind these:** Split Column (by delimiter/position), Merge Queries (join), Append Queries (union), Group By, Pivot/Unpivot Column, Fill Down/Up, Replace Values, Change Type, Remove Duplicates, Remove Errors, Conditional Column, Custom Column, Index Column, Extract (length/first chars/last chars).

## Query Parameters & Functions

```powerquery-m
// Parameters — reusable values referenced across queries (e.g. environment switching, date ranges)
// Manage Parameters in the ribbon > New Parameter

// Custom Functions — reusable M logic, e.g. to load a pattern of similarly-shaped files
let
    GetData = (fileName as text) =>
        let
            Source = Csv.Document(File.Contents(fileName)),
            Promoted = Table.PromoteHeaders(Source)
        in
            Promoted
in
    GetData
```

## Data Modeling — Relationships

```text
Model view > drag a column from one table to a related column in another table to create a relationship

Cardinality types:
  One-to-Many (most common — one dimension row relates to many fact rows)
  One-to-One
  Many-to-Many (supported directly since 2018, use cautiously — can cause ambiguous filter behavior)

Cross-filter direction:
  Single       Filters flow one direction only (dimension -> fact) — default and usually correct for star schemas
  Both            Filters flow both directions — can cause ambiguity/performance issues, use sparingly

Active vs Inactive relationships — only ONE active relationship between two tables at a time;
  additional relationships must be inactive and invoked explicitly in DAX via USERELATIONSHIP()

Star Schema (recommended pattern):
  Central Fact table (transactions/events) surrounded by Dimension tables (Date, Customer, Product, etc.)
  Avoid snowflaking (dimensions referencing other dimensions) where possible — flatten into the dimension instead
```

## DAX — Core Concepts

```text
Calculated Column         Computed row-by-row, stored in the model, uses row context
Measure                       Computed on the fly at query time, uses filter context — aggregates, NOT stored per row
Calculated Table                  A whole new table generated by a DAX expression

Row Context      "Which row am I currently evaluating?" — exists naturally in calculated columns, iterators (SUMX, etc.)
Filter Context       "Which filters are currently applied?" — comes from slicers, visual axes, other measures, page/report filters
Context Transition       CALCULATE() converts row context into filter context — the single most important DAX concept
```

## DAX — Aggregation Functions

```dax
Total Sales = SUM(Sales[Amount])
Order Count = COUNT(Sales[OrderID])
Distinct Customers = DISTINCTCOUNT(Sales[CustomerID])
Average Order = AVERAGE(Sales[Amount])
Max Amount = MAX(Sales[Amount])
Min Amount = MIN(Sales[Amount])

Weighted Total = SUMX(Sales, Sales[Quantity] * Sales[UnitPrice])          // row-by-row iterator, then sums
Filtered Avg = AVERAGEX(FILTER(Sales, Sales[Amount] > 100), Sales[Amount])
Count Rows = COUNTROWS(Sales)
```

## DAX — CALCULATE (the most important function)

```dax
Sales This Category = CALCULATE(SUM(Sales[Amount]), Sales[Category] = "Electronics")

Sales YTD = CALCULATE(SUM(Sales[Amount]), DATESYTD(Calendar[Date]))

Sales Excluding Filter = CALCULATE(SUM(Sales[Amount]), ALL(Sales[Category]))     // ignore an existing filter
Sales All Except Year = CALCULATE(SUM(Sales[Amount]), ALLEXCEPT(Calendar, Calendar[Year]))

Sales With Both Conditions = CALCULATE(
    SUM(Sales[Amount]),
    Sales[Category] = "Electronics",
    Sales[Region] = "EMEA"
)                                            // multiple filter args are combined with AND

Sales With Or Logic = CALCULATE(
    SUM(Sales[Amount]),
    Sales[Category] = "Electronics" || Sales[Category] = "Furniture"
)
```

## DAX — Time Intelligence

```dax
Sales YTD = TOTALYTD(SUM(Sales[Amount]), Calendar[Date])
Sales QTD = TOTALQTD(SUM(Sales[Amount]), Calendar[Date])
Sales MTD = TOTALMTD(SUM(Sales[Amount]), Calendar[Date])

Sales PY = CALCULATE(SUM(Sales[Amount]), SAMEPERIODLASTYEAR(Calendar[Date]))
Sales PY (alt) = CALCULATE(SUM(Sales[Amount]), DATEADD(Calendar[Date], -1, YEAR))
Sales Prior Month = CALCULATE(SUM(Sales[Amount]), DATEADD(Calendar[Date], -1, MONTH))

YoY Growth % = DIVIDE([Sales This Year] - [Sales PY], [Sales PY])

Sales Last 30 Days = CALCULATE(SUM(Sales[Amount]), DATESINPERIOD(Calendar[Date], MAX(Calendar[Date]), -30, DAY))

FirstDate = FIRSTDATE(Calendar[Date])
LastDate = LASTDATE(Calendar[Date])
```

**Note:** time intelligence functions require a proper Date table marked as the model's official date table (Model view > right-click table > "Mark as Date Table"), with one contiguous row per calendar date.

## DAX — Filter Functions

```dax
FILTER(Sales, Sales[Amount] > 100)          // returns a filtered table, used inside CALCULATE/iterators
ALL(Sales)                                       // removes all filters on a table (or column)
ALLSELECTED(Sales)                                  // removes filters added by the visual, keeps ones from slicers/page filters
ALLEXCEPT(Sales, Sales[Region])                        // remove all filters except on specified column(s)
REMOVEFILTERS(Sales[Category])                            // explicit modern alternative to ALL for clarity
KEEPFILTERS(...)                                              // combine with existing filters instead of overriding them

VALUES(Sales[Category])          // distinct values respecting current filter context
DISTINCT(Sales[Category])           // similar, slightly different NULL handling
HASONEVALUE(Sales[Category])           // TRUE if filter context has narrowed to exactly one value
SELECTEDVALUE(Sales[Category], "Multiple")     // returns the single selected value, or a default if 0/many are selected
ISFILTERED(Sales[Category])
ISCROSSFILTERED(Sales)
```

## DAX — Relationship Functions

```dax
RELATED(Calendar[Year])              // pull a value from the "one" side of a relationship, used in calculated columns
RELATEDTABLE(Sales)                     // pull related rows from the "many" side
CALCULATE(SUM(Sales[Amount]), USERELATIONSHIP(Sales[ShipDate], Calendar[Date]))    // activate an inactive relationship for this calc
CROSSFILTER(Sales[CustomerID], Customer[CustomerID], Both)     // override cross-filter direction for one calculation
```

## DAX — Logical & Text Functions

```dax
IF(Sales[Amount] > 100, "High", "Low")
SWITCH(TRUE(), Sales[Amount] > 1000, "High", Sales[Amount] > 100, "Medium", "Low")
AND(cond1, cond2) / OR(cond1, cond2) / NOT(cond)
COALESCE(Sales[Discount], 0)
IFERROR(Sales[Amount] / Sales[Qty], 0)

CONCATENATE(Sales[First], Sales[Last])
Sales[First] & " " & Sales[Last]
FORMAT(Sales[Amount], "$#,##0.00")
FORMAT(Calendar[Date], "yyyy-MM")
UPPER([Name]) / LOWER([Name]) / TRIM([Name])
LEFT([Name], 3) / RIGHT([Name], 3) / MID([Name], 2, 5)
LEN([Name])
```

## DAX — Common Patterns

```dax
% of Total = DIVIDE(SUM(Sales[Amount]), CALCULATE(SUM(Sales[Amount]), ALL(Sales)))

Rank by Sales = RANKX(ALL(Product[ProductName]), [Total Sales])

Running Total = CALCULATE(
    SUM(Sales[Amount]),
    FILTER(ALLSELECTED(Calendar[Date]), Calendar[Date] <= MAX(Calendar[Date]))
)

New Customers = CALCULATE(
    DISTINCTCOUNT(Sales[CustomerID]),
    FILTER(Customer, Customer[FirstPurchaseDate] = MIN(Calendar[Date]))
)

Top N Products = TOPN(10, ALL(Product), [Total Sales], DESC)

Dynamic Title = "Sales for " & SELECTEDVALUE(Calendar[Year], "All Years")
```

## Calculated Tables

```dax
DateTable = CALENDAR(DATE(2020,1,1), DATE(2026,12,31))
DateTableAuto = CALENDARAUTO()                                   // auto-detects range from model's date columns

TopCustomers = TOPN(100, Customer, Customer[LifetimeValue], DESC)
SummaryTable = SUMMARIZE(Sales, Sales[Category], "Total", SUM(Sales[Amount]))
```

## Visualizations — Common Types & Uses

```text
Bar/Column Chart              Compare categories
Line Chart                       Trends over time
Pie/Donut Chart                     Part-to-whole (use sparingly — bar charts are usually clearer)
Area Chart                             Trends + magnitude over time
Scatter Chart                             Correlation between two (or three, via size) measures
Map / Filled Map                             Geographic distribution
Table / Matrix                                  Detailed tabular data, Matrix supports row/column pivoting + drill-down
Card / Multi-row Card                              Single KPI or a small set of KPIs
Gauge                                                 Progress toward a target
KPI visual                                               Trend + target + current value in one compact visual
Slicer                                                      Interactive filter control (list, dropdown, date range, numeric range)
Waterfall Chart                                                Sequential positive/negative contributions to a total
Funnel Chart                                                      Sequential stage drop-off (e.g. sales pipeline)
Treemap                                                             Hierarchical part-to-whole
Decomposition Tree                                                     AI-assisted drill-down to explain a metric
Key Influencers                                                           AI-assisted analysis of what drives a metric
Python/R visual                                                              Embed custom Python/R-generated charts
```

## Formatting & Interactivity

```text
Format pane (paint roller icon) — per-visual title, axis, data labels, colors, borders
Visual > Edit interactions (Format tab > Edit Interactions) — control how one visual filters/highlights others on click
Drill Down/Up — right-click or use the ⌄⌃ chevrons on a visual with a hierarchy (e.g. Year > Quarter > Month)
Tooltips — customize default tooltips, or design a whole report page as a custom tooltip
Bookmarks (View > Bookmarks pane) — save a snapshot of filter/visual state, use for guided navigation or toggle views
Selection Pane (View > Selection) — show/hide and reorder individual visual layers, useful for bookmark-driven UI toggling
Buttons + Bookmarks — common pattern for building interactive navigation, tab-like UI, or show/hide toggles
```

## Filters

```text
Filter pane levels (top to bottom priority for troubleshooting):
  Filters on this visual        Applies only to the selected visual
  Filters on this page              Applies to all visuals on the current page
  Filters on all pages                 Applies report-wide
  Drillthrough filters                    Passed when a user right-click > drills through to a detail page

Filter types: Basic (checklist), Advanced (condition-based, e.g. > 100), Top N, Relative Date, Relative Time
```

## Row-Level Security (RLS)

```text
Modeling > Manage Roles > Create Role > add a DAX filter expression per table, e.g.:
  [Region] = USERNAME()
  [Region] = LOOKUPVALUE(UserRegionMap[Region], UserRegionMap[Email], USERPRINCIPALNAME())

View As Roles — test a role's effect before publishing
In the Service: Dataset > Security > add users/groups to each role
```

## Power BI Service — Publishing & Refresh

```text
Home > Publish (from Desktop)               push the .pbix to a workspace in the Service
Dataset > Settings > Scheduled Refresh          configure refresh frequency (up to 8x/day on Pro, 48x/day on Premium)
Dataset > Settings > Gateway Connection             required for on-premises data sources
Dataset > Refresh Now                                  manual on-demand refresh
Dataset > Refresh History                                 view past refresh successes/failures, duration, errors

Workspaces > New Workspace                Create a collaborative workspace (requires Pro/PPU licensing for most features)
Publish App                                  Bundle workspace content into a curated app for broad distribution
Manage Permissions                              Control who can view/edit/build-on datasets and reports

Incremental Refresh (Desktop > Table > Incremental Refresh policy)     only refresh recent partitions instead of the full table — critical for large fact tables
```

## Power BI Premium / Fabric-Related Concepts

```text
Premium Capacity (P SKUs) / Fabric Capacity (F SKUs)     dedicated compute for larger datasets, paginated reports, AI features, XMLA endpoint access
Deployment Pipelines          Dev/Test/Prod promotion workflow for content within the Service
XMLA Endpoint                    Connect external tools (Tabular Editor, DAX Studio, SSMS) directly to a published dataset for advanced modeling
Dataflows                           Reusable Power Query ETL logic, shared across multiple datasets, stored in the Service
Shared Datasets                        One published dataset reused as the source for multiple separate reports
```

## Performance Tips

```text
- Prefer Star Schema over Snowflake or a single wide/flat table — VertiPaq compresses and queries star schemas much more efficiently.
- Use Measures over Calculated Columns wherever possible — measures compute at query time and don't bloat the model's stored size.
- Avoid bidirectional ("Both") cross-filtering unless specifically needed — it can create ambiguous paths and slow queries.
- Reduce cardinality — high-cardinality columns (e.g. raw timestamps, GUIDs) hurt compression; split datetime into Date + Time, or truncate precision where full precision isn't needed.
- Disable Auto Date/Time (File > Options > Data Load) — it silently creates a hidden date table PER date column, bloating the model; use one shared, explicit Date table instead.
- Use Performance Analyzer (View tab) to identify slow visuals/DAX queries.
- Use DAX Studio (external tool) to profile and tune individual DAX measures.
- Import mode is almost always faster than DirectQuery for interactive dashboards — reserve DirectQuery for genuinely real-time or too-large-to-import datasets.
```

## Common Gotchas

- `ALL()` inside `CALCULATE` removes filters — a common mistake is expecting it to "clear the visual" when it actually changes what the *measure* computes, independent of what's displayed elsewhere.
- Calculated columns are computed once at refresh time and stored — they don't respond to report-level filter context the way measures do; use a measure if the value needs to react to slicers/filters.
- `SUM()` vs `SUMX()` — `SUM` aggregates a single column directly; `SUMX` iterates row-by-row and is required whenever you need to multiply/combine columns before summing (e.g., quantity × price).
- Relationships must have a single active path between two tables — ambiguous/circular relationship chains will be silently deactivated or cause modeling errors; use `USERELATIONSHIP` to invoke an inactive one explicitly when needed.
- `DISTINCTCOUNT` and other DAX aggregations respect the current filter context — including filters from slicers on OTHER pages if using `ALLSELECTED` incorrectly; test with Performance Analyzer or by manually applying filters to confirm expected behavior.
- Power Query steps execute in order, and later steps depending on column names/types from earlier steps will break if you reorder or delete an earlier step — check the Applied Steps pane carefully after any edit.
- Auto Date/Time hierarchies (if not disabled) can cause every single date-type column in the model to spawn a hidden calendar table, dramatically increasing model size for no benefit — disable it early in a project.

<!-- {% endraw %} -->
