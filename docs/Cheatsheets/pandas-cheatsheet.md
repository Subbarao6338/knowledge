# Pandas Cheatsheet

## Creating DataFrames

```python
import pandas as pd
import numpy as np

pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
pd.DataFrame([[1, 2], [3, 4]], columns=["a", "b"])
pd.Series([1, 2, 3], name="values")
pd.Series({"a": 1, "b": 2})

pd.read_csv("file.csv")
pd.read_csv("file.csv", usecols=["a", "b"], dtype={"a": "int32"}, parse_dates=["date"])
pd.read_parquet("file.parquet")
pd.read_excel("file.xlsx", sheet_name="Sheet1")
pd.read_json("file.json")
pd.read_sql("SELECT * FROM table", con=engine)

df.to_csv("out.csv", index=False)
df.to_parquet("out.parquet")
df.to_excel("out.xlsx", index=False)
df.to_sql("table_name", con=engine, if_exists="replace")
```

## Inspecting Data

```python
df.head(); df.tail(); df.sample(5)
df.shape
df.info()
df.describe()                     # summary stats for numeric columns
df.describe(include="all")           # include categorical too
df.dtypes
df.columns; df.index
df.isnull().sum()                       # nulls per column
df.nunique()                              # unique values per column
df.memory_usage(deep=True)
df.value_counts()                            # for a Series
df["col"].unique()
```

## Selecting Data

```python
df["col"]                    # single column -> Series
df[["a", "b"]]                  # multiple columns -> DataFrame
df.loc[0]                          # row by label
df.loc[0:3]                          # rows by label range (inclusive)
df.iloc[0]                              # row by position
df.iloc[0:3]                              # rows by position (exclusive end)
df.loc[0:3, ["a", "b"]]                      # rows + columns by label
df.iloc[0:3, 0:2]                              # rows + columns by position
df.at[0, "a"]                                    # fast scalar access by label
df.iat[0, 0]                                       # fast scalar access by position

df.loc[df["a"] > 5]                # boolean filter
df.loc[(df["a"] > 5) & (df["b"] < 10)]   # combine with & | ~ and parentheses
df.query("a > 5 and b < 10")              # query syntax alternative
df[df["col"].isin(["x", "y"])]
df[df["col"].str.contains("pattern", na=False)]
df[df["col"].between(1, 10)]
```

## Modifying Data

```python
df["c"] = df["a"] + df["b"]
df["c"] = df["a"].apply(lambda x: x * 2)
df["c"] = np.where(df["a"] > 5, "high", "low")

df.assign(c=lambda d: d["a"] + d["b"])     # returns new df, chainable

df.rename(columns={"a": "alpha"})
df.rename(columns=str.upper)
df.drop(columns=["a"])
df.drop(index=[0, 1])
df.drop_duplicates()
df.drop_duplicates(subset=["a"], keep="first")

df["a"] = df["a"].astype("int32")
df["date"] = pd.to_datetime(df["date"])
df["num"] = pd.to_numeric(df["num"], errors="coerce")   # bad values -> NaN

df.set_index("id")
df.reset_index(drop=True)
df.sort_values("a")
df.sort_values(["a", "b"], ascending=[True, False])
df.sort_index()
```

## Missing Data

```python
df.isnull(); df.notnull()
df.isnull().sum()
df.dropna()                          # drop rows with any null
df.dropna(subset=["a"])                 # drop rows null in specific columns
df.dropna(how="all")                       # drop only fully-null rows
df.fillna(0)
df.fillna({"a": 0, "b": "unknown"})           # per-column fill
df["a"].fillna(df["a"].mean())
df.ffill(); df.bfill()                           # forward/backward fill
df.interpolate()                                   # interpolate missing numeric values
```

## GroupBy & Aggregation

```python
df.groupby("category")["value"].sum()
df.groupby("category")["value"].agg(["sum", "mean", "count"])
df.groupby("category").agg(
    total=("value", "sum"),
    avg=("value", "mean"),
    n=("value", "count"),
)
df.groupby(["cat1", "cat2"])["value"].sum()          # multi-level group
df.groupby("category").apply(lambda g: g.nlargest(3, "value"))
df.groupby("category").filter(lambda g: len(g) > 5)     # keep groups matching condition
df.groupby("category")["value"].transform("mean")          # broadcast agg back to rows
df.groupby("category").size()                                 # row count per group
df.groupby("category").first(); .last(); .nth(0)

# Window / rolling
df["rolling_mean"] = df["value"].rolling(window=7).mean()
df["expanding_sum"] = df["value"].expanding().sum()
df["ewm"] = df["value"].ewm(span=7).mean()
```

## Merging & Joining

```python
pd.merge(df1, df2, on="key", how="inner")     # inner, left, right, outer, cross
pd.merge(df1, df2, left_on="id1", right_on="id2")
pd.merge(df1, df2, on="key", suffixes=("_left", "_right"))
pd.merge(df1, df2, on="key", indicator=True)    # adds "_merge" column showing source

df1.join(df2, how="left")                          # join on index
pd.concat([df1, df2])                                 # stack vertically (union rows)
pd.concat([df1, df2], axis=1)                            # stack horizontally (union cols)
pd.concat([df1, df2], ignore_index=True)                    # reset index after concat
```

## Reshaping

```python
df.pivot(index="date", columns="category", values="value")
df.pivot_table(index="date", columns="category", values="value", aggfunc="sum", fill_value=0)
df.melt(id_vars=["id"], value_vars=["a", "b"], var_name="metric", value_name="value")
df.stack()                    # columns -> rows (MultiIndex)
df.unstack()                     # rows -> columns
df.transpose()                      # swap rows/columns
pd.crosstab(df["a"], df["b"])          # frequency cross-tabulation
```

## String Operations (`.str` accessor)

```python
df["col"].str.lower(); .str.upper(); .str.strip()
df["col"].str.contains("pattern", case=False, na=False)
df["col"].str.replace("old", "new", regex=False)
df["col"].str.split(",")
df["col"].str.split(",", expand=True)     # split into separate columns
df["col"].str.extract(r"(\d+)")
df["col"].str.len()
df["col"].str.startswith("prefix")
df["col"].str.cat(sep=", ")
df["col"].str.zfill(5)
```

## Datetime Operations (`.dt` accessor)

```python
df["date"] = pd.to_datetime(df["date"])
df["date"].dt.year; .dt.month; .dt.day
df["date"].dt.day_name()
df["date"].dt.dayofweek
df["date"].dt.quarter
df["date"].dt.is_month_end
df["date"] + pd.Timedelta(days=7)
df["date"].dt.to_period("M")

df.set_index("date").resample("D").sum()          # daily resample
df.set_index("date").resample("M").mean()             # monthly resample
df.set_index("date").resample("W").agg({"a": "sum", "b": "mean"})

pd.date_range("2026-01-01", "2026-12-31", freq="D")
pd.date_range("2026-01-01", periods=12, freq="MS")
```

## Categorical Data

```python
df["cat"] = df["cat"].astype("category")            # saves memory, speeds up groupby
df["cat"].cat.categories
df["cat"] = df["cat"].cat.set_categories(["low", "med", "high"], ordered=True)
df["cat"].cat.codes                                     # integer codes
pd.cut(df["value"], bins=[0, 10, 50, 100], labels=["low", "med", "high"])
pd.qcut(df["value"], q=4)                                  # quantile-based binning
```

## Applying Functions

```python
df["col"].apply(func)                     # element-wise on a Series
df.apply(func, axis=1)                       # row-wise across a DataFrame (slow — vectorize if possible)
df.apply(func, axis=0)                          # column-wise
df.applymap(func)                                  # element-wise on entire DataFrame (deprecated, use .map)
df["col"].map({"a": 1, "b": 2})                       # value mapping via dict
df["col"].map(func)
df.pipe(custom_func, arg1=1)                             # chain a custom function into a pipeline
```

## Performance Tips

```python
# Vectorize instead of .apply()/loops where possible
df["c"] = df["a"] + df["b"]              # fast
df["c"] = df.apply(lambda r: r["a"] + r["b"], axis=1)   # slow — avoid

# Use categorical dtype for low-cardinality string columns
df["status"] = df["status"].astype("category")

# Use vectorized string/datetime accessors, not .apply(lambda x: x.method())

# Read only needed columns
pd.read_csv("file.csv", usecols=["a", "b"])

# Use chunked reading for huge CSVs
for chunk in pd.read_csv("huge.csv", chunksize=100_000):
    process(chunk)

# Downcast numeric types to save memory
df["a"] = pd.to_numeric(df["a"], downcast="integer")

# Use .loc for assignment to avoid SettingWithCopyWarning
df.loc[df["a"] > 5, "flag"] = "high"          # correct
# df[df["a"] > 5]["flag"] = "high"            # WRONG — chained indexing, may silently fail

# Use eval/query for large numeric expressions (uses numexpr under the hood)
df.eval("c = a + b", inplace=True)
df.query("a > 5 and b < 10")
```

## Common Gotchas

- Chained indexing (`df[cond]["col"] = x`) may raise `SettingWithCopyWarning` and silently not modify `df` — use `.loc[cond, "col"] = x` instead.
- `df.copy()` — modifying a slice without `.copy()` may or may not affect the original; be explicit.
- Integer columns silently become `float64` if they contain `NaN` — use nullable `Int64` (capital I) dtype to keep them as integers with nulls.
- `==` on floating point columns is fragile — use `np.isclose()` for comparisons.
- `groupby` drops `NaN` group keys by default — pass `dropna=False` to keep them.
- Merge can silently produce duplicate rows if keys aren't unique on one side — check with `validate="one_to_many"` etc. on `pd.merge`.
