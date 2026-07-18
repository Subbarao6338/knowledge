# Pandas vs Polars — Detailed Comparison

## Quick Take

| | Pandas | Polars |
|---|---|---|
| Language / core | Python + Cython, backed by NumPy | Rust, with Python bindings |
| Execution model | Eager only | Eager **and** lazy |
| Parallelism | Mostly single-threaded | Multi-threaded by default |
| Memory format | NumPy arrays / custom blocks | Apache Arrow |
| Null handling | Multiple inconsistent representations (`NaN`, `None`, `NaT`) | Single consistent `null` |
| API style | Index-centric, many ways to do the same thing | Expression-based, more consistent |
| Maturity / ecosystem | 15+ years, huge ecosystem | ~5 years, growing fast |
| Typical speed on large data | Baseline | 2–30x faster, often more on group-by/joins |
| Out-of-core / streaming | Limited | Built-in streaming engine |

---

## 1. Architecture & Performance

**Pandas** is built on NumPy arrays. Each column is typically a NumPy array (or an `ExtensionArray` for newer nullable types), and most operations run single-threaded in Cython/C. Pandas 2.0 added an optional Arrow-backed backend (`dtype_backend="pyarrow"`), but the default engine and most of the ecosystem still assume the classic NumPy-based internals.

**Polars** is written in Rust on top of Apache Arrow's columnar memory format. It uses:
- **Multi-threading by default** — operations are automatically parallelized across CPU cores.
- **Query optimization** — the lazy API builds a query plan and optimizes it (predicate pushdown, projection pushdown, common subexpression elimination) before executing.
- **SIMD vectorization** at the Rust level for many operations.

Practical effect: for large datasets (millions of rows, group-bys, joins, aggregations), Polars is commonly 5–30x faster than Pandas out of the box, without you tuning anything. For small dataframes (thousands of rows), the difference is often negligible or even in Pandas's favor due to Polars's fixed overhead.

---

## 2. Eager vs Lazy Execution

This is the single biggest conceptual difference.

**Pandas — eager only:**
```python
import pandas as pd

df = pd.read_csv("data.csv")
result = (
    df[df["value"] > 100]
    .groupby("category")["value"]
    .sum()
    .reset_index()
)
```
Every line executes immediately, materializing intermediate dataframes in memory.

**Polars — eager (similar to Pandas):**
```python
import polars as pl

df = pl.read_csv("data.csv")
result = (
    df.filter(pl.col("value") > 100)
    .group_by("category")
    .agg(pl.col("value").sum())
)
```

**Polars — lazy (the recommended way for real work):**
```python
result = (
    pl.scan_csv("data.csv")          # doesn't read the file yet
    .filter(pl.col("value") > 100)
    .group_by("category")
    .agg(pl.col("value").sum())
    .collect()                        # optimizes the whole plan, then executes
)
```

With `scan_*` + `.collect()`, Polars builds a full query plan first. It can push the filter down to the CSV reader itself (skipping rows it doesn't need), only read the columns actually used, and fuse operations — all before touching disk. Pandas has no equivalent; every operation reads/processes the full intermediate result.

---

## 3. API Design Philosophy

**Pandas** revolves around the **index** — a labeled axis that persists across operations and often causes confusing behavior (implicit alignment, `reset_index()` calls scattered everywhere, `SettingWithCopyWarning`). There are frequently multiple ways to do the same thing (`.loc`, `.iloc`, `.at`, `.iat`, chained indexing), which is flexible but inconsistent.

**Polars** has **no index concept**. Every row is just a row; every column is just a column. Instead of index-based alignment, Polars uses an **expression API** — you build expressions (`pl.col("x") * 2`) that are composable and can run in parallel across columns.

```python
# Pandas: multiple columns, index-based
df["total"] = df["price"] * df["qty"]
df.loc[df["total"] > 1000, "flag"] = "high"

# Polars: expression-based, no index
df = df.with_columns(
    (pl.col("price") * pl.col("qty")).alias("total")
).with_columns(
    pl.when(pl.col("total") > 1000).then(pl.lit("high")).otherwise(pl.lit("low")).alias("flag")
)
```

Polars expressions can also run **multiple transformations in parallel in a single `.with_columns()` call**, since each expression is independent — something Pandas can't easily do.

---

## 4. Syntax Cheat-Sheet (Side by Side)

| Task | Pandas | Polars |
|---|---|---|
| Read CSV | `pd.read_csv("f.csv")` | `pl.read_csv("f.csv")` / `pl.scan_csv("f.csv")` |
| Select columns | `df[["a", "b"]]` | `df.select("a", "b")` |
| Filter rows | `df[df["a"] > 5]` | `df.filter(pl.col("a") > 5)` |
| Add column | `df["c"] = df["a"] + df["b"]` | `df.with_columns((pl.col("a")+pl.col("b")).alias("c"))` |
| Group + aggregate | `df.groupby("k")["v"].sum()` | `df.group_by("k").agg(pl.col("v").sum())` |
| Sort | `df.sort_values("a")` | `df.sort("a")` |
| Join | `df1.merge(df2, on="k")` | `df1.join(df2, on="k")` |
| Drop nulls | `df.dropna()` | `df.drop_nulls()` |
| Fill nulls | `df.fillna(0)` | `df.fill_null(0)` |
| Apply custom function | `df["a"].apply(fn)` (slow, row-wise) | `df.select(pl.col("a").map_elements(fn))` (still slower — prefer native expressions) |
| Value counts | `df["a"].value_counts()` | `df["a"].value_counts()` |
| Pivot | `df.pivot_table(...)` | `df.pivot(...)` |
| Window function | `df.groupby("k")["v"].transform("sum")` | `pl.col("v").sum().over("k")` |
| Rename column | `df.rename(columns={"a":"b"})` | `df.rename({"a":"b"})` |
| To pandas / from pandas | n/a | `df.to_pandas()` / `pl.from_pandas(pdf)` |

---

## 5. Null / Missing Data Handling

Pandas has historically used several representations depending on dtype:
- `NaN` (float) for numeric missing values
- `None` for object dtype
- `NaT` for datetime
- `pd.NA` for newer nullable dtypes (`Int64`, `boolean`, etc.)

This inconsistency causes subtle bugs (e.g., an integer column silently upcasts to float when it gets a `NaN`).

Polars uses a **single, consistent `null`** across all dtypes, backed by Arrow's validity bitmap. An integer column with missing values stays an integer column — no silent upcasting.

---

## 6. Memory Usage

- Pandas duplicates data more often during operations (many methods return copies), and string columns (`object` dtype) are notoriously memory-heavy — each string is a separate Python object with overhead.
- Polars stores strings in Arrow's compact columnar format and generally uses significantly less memory, especially for string-heavy data. Its lazy engine also enables **streaming** (`.collect(streaming=True)`), letting you process datasets larger than RAM by processing them in batches.

---

## 7. Ecosystem & Interop

**Pandas advantages:**
- Deep integration with almost everything: scikit-learn, statsmodels, matplotlib/seaborn, most plotting and ML libraries expect Pandas DataFrames or NumPy arrays natively.
- Enormous body of Stack Overflow answers, tutorials, and existing production code.
- `.plot()` accessor built in.

**Polars advantages:**
- First-class Arrow interop — zero-copy or near-zero-copy conversion to/from Arrow, DuckDB, and increasingly other tools.
- Growing but smaller plotting/ML integration; you often convert to Pandas (`.to_pandas()`) or NumPy at the boundary when a library expects it.
- SQL context: `pl.SQLContext` lets you run SQL directly against Polars frames.

---

## 8. When to Use Which

**Reach for Pandas when:**
- You're doing exploratory work in a notebook and want maximum compatibility with plotting/ML libraries.
- Your dataset is small-to-medium (fits comfortably in memory, not performance-critical).
- You're working in a codebase that already has heavy Pandas dependencies.
- You need a specific Pandas-only feature (e.g., certain time-series resampling edge cases, `MultiIndex`-heavy workflows).

**Reach for Polars when:**
- You're processing large datasets (millions+ rows) and performance/memory matter.
- You want predictable, parallelized performance without manual tuning.
- You're building a data pipeline where you can use the lazy API end-to-end (scan → transform → collect).
- You want stricter, more consistent typing and null semantics to reduce silent bugs.
- You need to process data larger than RAM (streaming mode).

**In practice:** many teams use both — Polars for the heavy lifting/ETL, then `.to_pandas()` at the end for compatibility with a plotting or ML library that doesn't yet support Polars natively.

---

## 9. Migration Notes (Pandas → Polars)

- No index — drop any code relying on `.loc`/`.iloc`/index alignment; reference columns by name instead.
- `.apply(fn)` row-wise loops are an anti-pattern in both, but especially in Polars — prefer native expressions (`pl.col(...)`) which vectorize and parallelize; `map_elements` is the escape hatch, not the default.
- Chained `.with_columns()` calls replace most `df["new_col"] = ...` assignment patterns.
- `group_by` (with underscore) instead of `groupby`.
- Joins use `join`, similar to Pandas's `merge`, with similar `how=` options (`inner`, `left`, `outer`, `semi`, `anti`, etc. — Polars adds `semi`/`anti` joins natively).
- Get comfortable with `scan_csv`/`scan_parquet` + `.collect()` rather than `read_csv` if you want the optimizer to kick in.

---

## 10. Summary

Polars is generally the better default for new, performance-sensitive data engineering work, especially at scale, thanks to its lazy query optimizer, multi-threading, and Arrow-native memory model. Pandas remains extremely strong for exploratory analysis, notebook-driven work, and anywhere deep ecosystem compatibility (ML/plotting libraries) matters more than raw throughput. Neither is strictly obsolete — the choice mostly comes down to data size, performance needs, and what the rest of your stack expects.
