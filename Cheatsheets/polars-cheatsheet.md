# Polars Cheatsheet

## Creating DataFrames

```python
import polars as pl

pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
pl.Series("values", [1, 2, 3])

pl.read_csv("file.csv")
pl.read_parquet("file.parquet")
pl.read_json("file.json")
pl.read_excel("file.xlsx")
pl.read_database(query="SELECT * FROM table", connection=conn)

# Lazy readers — build a query plan without loading data yet
pl.scan_csv("file.csv")
pl.scan_parquet("file.parquet")
pl.scan_ndjson("file.jsonl")

df.write_csv("out.csv")
df.write_parquet("out.parquet")
df.write_json("out.json")
df.write_excel("out.xlsx")
```

## Eager vs Lazy

```python
# Eager: executes immediately, like pandas
df = pl.read_csv("data.csv")
result = df.filter(pl.col("a") > 5).group_by("cat").agg(pl.col("val").sum())

# Lazy: builds an optimized query plan, executes on .collect()
lf = pl.scan_csv("data.csv")
result = (
    lf.filter(pl.col("a") > 5)
      .group_by("cat")
      .agg(pl.col("val").sum())
      .collect()
)

# Inspect the optimized plan before running it
lf.explain()

# Convert between eager and lazy
df.lazy()             # DataFrame -> LazyFrame
lf.collect()             # LazyFrame -> DataFrame

# Streaming (out-of-core) execution for data larger than RAM
result = lf.collect(streaming=True)
```

## Inspecting Data

```python
df.head(); df.tail(); df.sample(5)
df.shape
df.schema                # column names + dtypes
df.describe()
df.null_count()
df.n_unique()
df["col"].value_counts()
df.estimated_size("mb")     # memory footprint
```

## Selecting & Filtering

```python
df.select("a", "b")
df.select(pl.col("a"), pl.col("b"))
df.select(pl.all())                       # all columns
df.select(pl.all().exclude("a"))              # all except one
df.select(pl.col("^prefix_.*$"))                 # regex column selection
df.select(pl.col(pl.Float64))                       # select by dtype

df.filter(pl.col("a") > 5)
df.filter((pl.col("a") > 5) & (pl.col("b") < 10))
df.filter(pl.col("cat").is_in(["x", "y"]))
df.filter(pl.col("name").str.contains("pattern"))

df[0]                       # row by position
df[0:5]                        # row slice
df.row(0)                         # returns a tuple
df.to_dicts()                        # list of dicts
```

## Modifying Data — the Expression API

```python
df.with_columns(
    (pl.col("a") + pl.col("b")).alias("c"),
    pl.col("a").cast(pl.Int32),
    pl.when(pl.col("a") > 5).then(pl.lit("high")).otherwise(pl.lit("low")).alias("flag"),
)

df.rename({"a": "alpha"})
df.drop("a")
df.drop_nulls()
df.drop_nulls(subset=["a"])
df.unique()
df.unique(subset=["a"], keep="first")

df.sort("a")
df.sort(["a", "b"], descending=[True, False])
df.with_row_index("row_num")             # add a row-number column (formerly with_row_count)
```

**Key idea:** every transformation is a `pl.col(...)`-based **expression**. Multiple expressions inside one `.with_columns()` or `.select()` run in parallel automatically, since Polars knows they're independent.

## Missing Data

```python
df.null_count()
df.drop_nulls()
df.fill_null(0)
df.fill_null(strategy="forward")            # forward fill
df.fill_null(strategy="backward")
df.with_columns(pl.col("a").fill_null(pl.col("a").mean()))
df.filter(pl.col("a").is_null())
df.filter(pl.col("a").is_not_null())
```

## GroupBy & Aggregation

```python
df.group_by("category").agg(pl.col("value").sum())

df.group_by("category").agg(
    pl.col("value").sum().alias("total"),
    pl.col("value").mean().alias("avg"),
    pl.col("value").count().alias("n"),
    pl.col("value").max().alias("max_val"),
)

df.group_by(["cat1", "cat2"]).agg(pl.col("value").sum())

df.group_by("category").agg(pl.col("value").top_k(3))     # aggregate into a list

# Window functions (no separate transform needed — use .over())
df.with_columns(
    pl.col("value").sum().over("category").alias("cat_total")
)
df.with_columns(
    (pl.col("value") / pl.col("value").sum().over("category")).alias("pct_of_cat")
)

# Group-by maintaining order (avoids implicit resort)
df.group_by("category", maintain_order=True).agg(...)
```

## Joins

```python
df1.join(df2, on="key", how="inner")     # inner, left, outer, cross, semi, anti
df1.join(df2, left_on="id1", right_on="id2")
df1.join(df2, on="key", suffix="_right")

df1.join(df2, on="key", how="semi")         # rows in df1 that HAVE a match in df2 (like a filter)
df1.join(df2, on="key", how="anti")            # rows in df1 that have NO match in df2

df1.join_asof(df2, on="timestamp", by="id")       # nearest-match time-series join
```

## Reshaping

```python
df.pivot(index="date", columns="category", values="value", aggregate_function="sum")
df.melt(id_vars=["id"], value_vars=["a", "b"], variable_name="metric", value_name="value")
df.transpose()
df.explode("list_col")           # unnest a list column into multiple rows
```

## String Operations (`.str` namespace)

```python
pl.col("col").str.to_lowercase()
pl.col("col").str.to_uppercase()
pl.col("col").str.strip_chars()
pl.col("col").str.contains("pattern")
pl.col("col").str.replace("old", "new")
pl.col("col").str.replace_all("old", "new")
pl.col("col").str.split(",")
pl.col("col").str.extract(r"(\d+)")
pl.col("col").str.len_chars()
pl.col("col").str.starts_with("prefix")
pl.col("col").str.zfill(5)
pl.col("col").str.slice(0, 3)
```

## Datetime Operations (`.dt` namespace)

```python
df.with_columns(pl.col("date").str.to_date("%Y-%m-%d"))
pl.col("date").dt.year()
pl.col("date").dt.month()
pl.col("date").dt.weekday()
pl.col("date").dt.strftime("%Y-%m")
pl.col("date") + pl.duration(days=7)

df.sort("date").group_by_dynamic("date", every="1mo").agg(pl.col("value").sum())    # resample
df.sort("date").rolling("date", period="7d").agg(pl.col("value").mean())               # rolling window by time
```

## Struct & List Columns

```python
# Nested/struct columns
df.select(pl.col("info").struct.field("name"))
df.unnest("info")                       # expand a struct column into top-level columns

# List columns
df.select(pl.col("tags").list.len())
df.select(pl.col("tags").list.get(0))
df.select(pl.col("tags").list.contains("x"))
df.explode("tags")                          # one row per list element
```

## Combining / Stacking

```python
pl.concat([df1, df2])                              # vertical stack (union rows), same schema
pl.concat([df1, df2], how="diagonal")                 # union rows, fill missing columns with null
pl.concat([df1, df2], how="horizontal")                  # side-by-side column concat
```

## Custom Functions

```python
# Prefer native expressions — they vectorize and parallelize
df.with_columns((pl.col("a") * 2).alias("b"))

# Escape hatch for arbitrary Python logic (slower — avoid in hot paths)
df.with_columns(
    pl.col("a").map_elements(lambda x: my_func(x), return_dtype=pl.Int64).alias("b")
)

# Apply a function across a whole group (still Python-level, use sparingly)
df.group_by("cat").map_groups(lambda g: g.head(3))
```

## SQL Interface

```python
ctx = pl.SQLContext(my_table=df)
ctx.execute("SELECT category, SUM(value) FROM my_table GROUP BY category").collect()

# Or directly on a DataFrame/LazyFrame
df.sql("SELECT * FROM self WHERE a > 5")
```

## Configuration & Performance

```python
pl.Config.set_tbl_rows(50)                # display more rows
pl.Config.set_fmt_str_lengths(100)          # longer string previews

pl.thread_pool_size()                          # check thread count in use

# Streaming for datasets larger than RAM
lf.collect(streaming=True)

# Prefer scan_* + lazy chains over read_* + eager for big files —
# enables predicate/projection pushdown and query optimization.
```

## Common Gotchas

- No index like pandas — reference everything by column name; there's no implicit row alignment.
- `group_by` (underscore) not `groupby`.
- Eager `.filter()`/`.select()` on a `read_*`-loaded DataFrame won't get query optimization — use `scan_*` + lazy chain + `.collect()` for that.
- `.map_elements()` (row-wise Python callback) is much slower than native expressions — treat it as a last resort, not a default like `.apply()` in pandas.
- Joins default to keeping both key columns unless you use `on=` with matching names — check for `_right`-suffixed duplicate columns after joins with differently named keys.
- `pl.col("x")` inside an expression refers to the column in the *current* context — some pandas patterns (referencing a previously-created column mid-chain) require chaining `.with_columns()` calls in sequence rather than one big expression.
