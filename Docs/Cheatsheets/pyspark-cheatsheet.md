# PySpark Cheatsheet

## Setup

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("MyApp")
    .config("spark.sql.shuffle.partitions", "200")
    .config("spark.executor.memory", "4g")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")
spark.version
spark.stop()
```

## Creating DataFrames

```python
from pyspark.sql import Row
import pyspark.sql.types as T

df = spark.createDataFrame([(1, "a"), (2, "b")], ["id", "name"])

schema = T.StructType([
    T.StructField("id", T.IntegerType(), nullable=False),
    T.StructField("name", T.StringType(), nullable=True),
])
df = spark.createDataFrame(data, schema=schema)

df = spark.read.csv("path.csv", header=True, inferSchema=True)
df = spark.read.parquet("path.parquet")
df = spark.read.json("path.json")
df = spark.read.format("jdbc").option("url", jdbc_url).option("dbtable", "table").load()
df = spark.table("catalog.schema.table")            # Delta/managed table
df = spark.sql("SELECT * FROM some_table")

df.write.mode("overwrite").parquet("out.parquet")
df.write.mode("append").saveAsTable("catalog.schema.table")
df.write.partitionBy("year", "month").parquet("out/")
df.write.format("delta").mode("overwrite").save("path/")
```

## Inspecting Data

```python
df.show()                    # default 20 rows
df.show(5, truncate=False)
df.printSchema()
df.columns
df.dtypes
df.count()
df.describe().show()
df.summary().show()             # more detailed stats incl. percentiles
df.explain()                       # physical/logical plan
df.explain(mode="formatted")          # readable query plan
df.rdd.getNumPartitions()
```

## Selecting & Filtering

```python
from pyspark.sql import functions as F

df.select("a", "b")
df.select(F.col("a"), F.col("b").alias("beta"))
df.select("*", (F.col("a") + F.col("b")).alias("c"))

df.filter(F.col("a") > 5)
df.where(F.col("a") > 5)                       # alias for filter
df.filter((F.col("a") > 5) & (F.col("b") < 10))
df.filter(F.col("cat").isin(["x", "y"]))
df.filter(F.col("name").rlike("^prefix.*"))
df.filter(F.col("a").isNull())
df.filter(F.col("a").isNotNull())

df.distinct()
df.dropDuplicates(["a"])
df.limit(10)
```

## Modifying Data

```python
df.withColumn("c", F.col("a") + F.col("b"))
df.withColumn("flag", F.when(F.col("a") > 5, "high").otherwise("low"))
df.withColumnRenamed("a", "alpha")
df.withColumns({"c": F.col("a") + 1, "d": F.col("b") * 2})    # multiple at once (Spark 3.3+)

df.drop("a")
df.na.drop()                     # drop rows with any null
df.na.drop(subset=["a"])
df.na.fill(0)
df.na.fill({"a": 0, "b": "unknown"})
df.na.replace(["old"], ["new"], "col")

df = df.withColumn("a", F.col("a").cast(T.IntegerType()))
df = df.withColumn("date", F.to_date("date_str", "yyyy-MM-dd"))

df.sort("a")
df.sort(F.col("a").desc())
df.orderBy(F.col("a").desc(), F.col("b").asc())
```

## Aggregation & GroupBy

```python
df.groupBy("category").sum("value")
df.groupBy("category").agg(
    F.sum("value").alias("total"),
    F.avg("value").alias("avg"),
    F.count("*").alias("n"),
    F.max("value").alias("max_val"),
    F.countDistinct("id").alias("unique_ids"),
)
df.groupBy("cat1", "cat2").agg(F.sum("value"))
df.groupBy("category").pivot("year").agg(F.sum("value"))     # pivot table
df.agg(F.sum("value"), F.avg("value"))                            # no grouping — whole df

# Window functions
from pyspark.sql.window import Window

w = Window.partitionBy("category").orderBy("date")
df.withColumn("running_total", F.sum("value").over(w))
df.withColumn("rank", F.rank().over(w))
df.withColumn("row_num", F.row_number().over(w))
df.withColumn("prev_value", F.lag("value", 1).over(w))
df.withColumn("next_value", F.lead("value", 1).over(w))

w_range = Window.partitionBy("category").orderBy("date").rowsBetween(-6, 0)
df.withColumn("rolling_7d_avg", F.avg("value").over(w_range))
```

## Joins

```python
df1.join(df2, on="key", how="inner")     # inner, left, right, outer/full, cross, left_semi, left_anti
df1.join(df2, df1.id1 == df2.id2, how="left")
df1.join(F.broadcast(df2), on="key")         # broadcast join hint for small df2 — avoids a shuffle

df1.join(df2, on="key", how="left_semi")        # rows in df1 that HAVE a match (filter-style join)
df1.join(df2, on="key", how="left_anti")           # rows in df1 with NO match
```

## SQL Interface

```python
df.createOrReplaceTempView("my_table")
spark.sql("SELECT category, SUM(value) as total FROM my_table GROUP BY category").show()

# Mixing SQL and DataFrame API freely is common and idiomatic in PySpark
```

## User-Defined Functions (UDFs)

```python
from pyspark.sql.types import IntegerType

# Regular UDF — row-by-row Python execution, relatively slow (serialization overhead)
@F.udf(returnType=IntegerType())
def add_one(x):
    return x + 1

df.withColumn("b", add_one("a"))

# Pandas UDF (vectorized) — MUCH faster, operates on batches via Arrow
import pandas as pd
from pyspark.sql.functions import pandas_udf

@pandas_udf(IntegerType())
def add_one_vectorized(s: pd.Series) -> pd.Series:
    return s + 1

df.withColumn("b", add_one_vectorized("a"))

# Prefer built-in F.* functions over UDFs whenever possible —
# they run in the JVM without Python serialization overhead at all.
```

## Repartitioning & Performance

```python
df.repartition(200)                       # full shuffle to N partitions
df.repartition(10, "category")               # hash-partition by column
df.coalesce(10)                                 # reduce partitions WITHOUT a full shuffle (no increase)

df.cache()                     # persist in memory across actions
df.persist(StorageLevel.MEMORY_AND_DISK)
df.unpersist()

spark.conf.set("spark.sql.shuffle.partitions", "200")     # default post-shuffle partition count
spark.conf.set("spark.sql.adaptive.enabled", "true")         # adaptive query execution (AQE)

df.explain(mode="cost")           # inspect cost-based plan
```

## Common Column Functions

```python
F.col("a")
F.lit(5)                          # literal value as a column
F.when(cond, val).otherwise(default)
F.coalesce(F.col("a"), F.col("b"), F.lit(0))       # first non-null
F.concat(F.col("a"), F.lit("_"), F.col("b"))
F.concat_ws("-", "a", "b", "c")
F.split(F.col("a"), ",")
F.explode(F.col("list_col"))               # unnest array column into rows
F.array(F.col("a"), F.col("b"))
F.struct(F.col("a"), F.col("b"))
F.to_json(F.col("struct_col"))
F.from_json(F.col("json_col"), schema)
F.regexp_extract(F.col("a"), r"(\d+)", 1)
F.regexp_replace(F.col("a"), "old", "new")
F.date_add(F.col("date"), 7)
F.datediff(F.col("end"), F.col("start"))
F.date_format(F.col("date"), "yyyy-MM")
F.current_date(); F.current_timestamp()
```

## RDD Basics (lower-level API, rarely needed directly)

```python
rdd = spark.sparkContext.parallelize([1, 2, 3, 4])
rdd.map(lambda x: x * 2).collect()
rdd.filter(lambda x: x > 2).collect()
rdd.reduce(lambda a, b: a + b)
rdd.flatMap(lambda x: [x, x*2]).collect()
df.rdd.map(lambda row: row.asDict())              # DataFrame -> RDD when needed
```

## Common Gotchas & Tips

- Spark is **lazy** — transformations (`select`, `filter`, `withColumn`, etc.) build a plan; only actions (`show`, `count`, `collect`, `write`) trigger execution.
- `.collect()` pulls all data to the driver — never call it on large DataFrames; use `.show()`, `.take(n)`, or write to storage instead.
- Avoid Python UDFs when a built-in `F.*` function exists — UDFs serialize data between JVM and Python, which is slow. Prefer Pandas UDFs over row-at-a-time UDFs when a UDF is unavoidable.
- Watch for data skew in joins/group-bys — a few oversized partitions can dominate runtime; consider salting keys or broadcast joins for small tables.
- `df.count()` triggers a full job — avoid calling it repeatedly just to check progress.
- Use `explain()` to check whether a join is a broadcast join, shuffle hash join, or sort-merge join when debugging performance.
- Enable Adaptive Query Execution (`spark.sql.adaptive.enabled=true`, default on in modern Spark) to let Spark re-optimize shuffle partitions and joins at runtime.
