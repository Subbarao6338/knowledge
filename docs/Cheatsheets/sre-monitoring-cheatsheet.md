# SRE, Monitoring & Time Series Cheatsheet

## Grafana & Prometheus (Flux & PromQL)

PromQL (Prometheus Query Language) is used to filter and aggregate time-series metric data on the fly.

```promql
# 1. CPU Usage rate over the last 5 minutes grouped by instance
sum(rate(node_cpu_seconds_total{mode!="idle"}[5m])) by (instance)

# 2. Memory usage percentage calculation
(node_memory_MemTotal_bytes - node_memory_MemFree_bytes) / node_memory_MemTotal_bytes * 100

# 3. HTTP Request failure rate (> 5xx status codes)
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))
```

---

## InfluxDB (Flux Query Engine)

Flux is the functional scripting language used in InfluxDB 2.0+ to query and manipulate time-series points.

```flux
// Query metric points from a specific bucket
from(bucket: "system_metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "cpu")
  |> filter(fn: (r) => r["_field"] == "usage_idle")
  |> filter(fn: (r) => r["cpu"] == "cpu-total")
  // Aggregate data in 5-minute windows calculating the mean
  |> aggregateWindow(every: 5m, fn: mean, createEmpty: false)
  // Calculate raw CPU usage percentage
  |> map(fn: (r) => ({ r with _value: 100.0 - r._value }))
```
