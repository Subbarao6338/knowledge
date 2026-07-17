# Apache Airflow Cheatsheet

## Core Concepts

| Concept | Meaning |
|---|---|
| **DAG** | Directed Acyclic Graph — a workflow defined as Python code, describing tasks and their dependencies |
| **Task** | A single unit of work (an Operator instance) within a DAG |
| **Operator** | A template defining what a task does (`PythonOperator`, `BashOperator`, `SQLExecuteQueryOperator`, etc.) |
| **Task Instance** | A specific run of a task, for a specific `execution_date`/logical date |
| **DAG Run** | A specific execution of the whole DAG, for a specific schedule interval |
| **Scheduler** | The process that parses DAGs and decides when to trigger DAG runs/tasks |
| **Executor** | Determines *how* tasks actually run (LocalExecutor, CeleryExecutor, KubernetesExecutor) |
| **XCom** | "Cross-communication" — small pieces of data passed between tasks |
| **Sensor** | A special operator that waits for a condition (file exists, external DAG finished, etc.) before proceeding |
| **Hook** | A reusable interface to an external system (database, API, cloud service) used inside operators |

---

## Minimal DAG

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "subbarao",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": True,
    "email": ["you@example.com"],
}

with DAG(
    dag_id="my_first_dag",
    default_args=default_args,
    description="A simple example DAG",
    schedule="0 6 * * *",             # cron expression: 6 AM daily
    start_date=datetime(2026, 1, 1),
    catchup=False,                       # don't backfill missed runs on deploy
    tags=["finops", "daily"],
) as dag:

    def extract():
        print("extracting...")

    def transform():
        print("transforming...")

    extract_task = PythonOperator(task_id="extract", python_callable=extract)
    transform_task = PythonOperator(task_id="transform", python_callable=transform)
    load_task = BashOperator(task_id="load", bash_command="echo loading data")

    extract_task >> transform_task >> load_task    # dependency chaining
```

## Modern Style: TaskFlow API (`@dag` / `@task`)

Preferred in Airflow 2.x+ for Python-heavy pipelines — automatically handles XCom passing.

```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["finops"],
)
def finops_pipeline():

    @task
    def extract():
        return {"rows": 100}

    @task
    def transform(data: dict):
        return {"rows": data["rows"] * 2}

    @task
    def load(data: dict):
        print(f"Loading {data['rows']} rows")

    load(transform(extract()))          # dependencies inferred from function calls

finops_pipeline()
```

## Task Dependencies

```python
task_a >> task_b                      # a runs before b
task_a << task_b                      # b runs before a (reversed)
task_a >> [task_b, task_c]            # a before both b and c (parallel branches)
[task_a, task_b] >> task_c            # c runs after both a and b complete

task_a.set_downstream(task_b)
task_a.set_upstream(task_b)

# Chain helper (list version)
from airflow.models.baseoperator import chain
chain(task_a, task_b, task_c)
chain(task_a, [task_b, task_c], task_d)   # fan-out then fan-in
```

## Common Operators

```python
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.amazon.aws.operators.athena import AthenaOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.providers.docker.operators.docker import DockerOperator

start = EmptyOperator(task_id="start")              # no-op, useful as a DAG anchor point

run_bash = BashOperator(task_id="run_bash", bash_command="echo hello")

run_python = PythonOperator(
    task_id="run_python",
    python_callable=my_func,
    op_kwargs={"param": "value"},
)

bq_task = BigQueryInsertJobOperator(
    task_id="bq_query",
    configuration={"query": {"query": "SELECT 1", "useLegacySql": False}},
)

k8s_task = KubernetesPodOperator(
    task_id="run_in_k8s",
    name="my-pod",
    image="my-image:latest",
    cmds=["python", "script.py"],
    namespace="default",
)
```

## Sensors

```python
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

wait_for_file = FileSensor(
    task_id="wait_for_file",
    filepath="/data/incoming/file.csv",
    poke_interval=30,          # seconds between checks
    timeout=60 * 60,             # give up after 1 hour
    mode="reschedule",              # frees the worker slot between pokes (vs "poke", which blocks)
)

wait_for_upstream_dag = ExternalTaskSensor(
    task_id="wait_for_upstream",
    external_dag_id="upstream_dag",
    external_task_id="final_task",
)

wait_for_s3 = S3KeySensor(
    task_id="wait_for_s3_file",
    bucket_name="my-bucket",
    bucket_key="data/{{ ds }}/file.parquet",
)
```

## XComs (passing small data between tasks)

```python
# Classic operators — push/pull explicitly
def extract(**context):
    context["ti"].xcom_push(key="row_count", value=100)

def transform(**context):
    count = context["ti"].xcom_pull(task_ids="extract", key="row_count")
    print(count)

extract_task = PythonOperator(task_id="extract", python_callable=extract)
transform_task = PythonOperator(task_id="transform", python_callable=transform)

# TaskFlow API — automatic, just return/pass values
@task
def extract():
    return 100

@task
def transform(count):
    print(count)

transform(extract())
```
**Note:** XComs are stored in the metadata database — keep them small (IDs, counts, short strings), never pass large DataFrames through XCom.

## Templating & Jinja Macros

Airflow renders Jinja templates in many operator fields (e.g., `bash_command`, SQL strings).

```python
BashOperator(
    task_id="templated",
    bash_command="echo {{ ds }} {{ execution_date }} {{ prev_ds }} {{ next_ds }}",
)
```

| Macro | Meaning |
|---|---|
| `{{ ds }}` | Logical date as `YYYY-MM-DD` |
| `{{ ds_nodash }}` | Logical date as `YYYYMMDD` |
| `{{ execution_date }}` / `{{ logical_date }}` | Full timestamp of the DAG run |
| `{{ prev_ds }}` / `{{ next_ds }}` | Previous/next scheduled date |
| `{{ dag.dag_id }}` | Current DAG's ID |
| `{{ ti }}` | Current TaskInstance object |
| `{{ params.my_param }}` | Custom params passed to the DAG |
| `{{ var.value.my_var }}` | Airflow Variable lookup |

## Branching & Conditional Logic

```python
from airflow.operators.python import BranchPythonOperator

def choose_branch(**context):
    if some_condition:
        return "path_a"
    return "path_b"

branch = BranchPythonOperator(task_id="branch", python_callable=choose_branch)
path_a = EmptyOperator(task_id="path_a")
path_b = EmptyOperator(task_id="path_b")
join = EmptyOperator(task_id="join", trigger_rule="none_failed_min_one_success")

branch >> [path_a, path_b] >> join
```

**Trigger rules** (control when a task runs based on upstream state):
`all_success` (default), `all_failed`, `all_done`, `one_success`, `one_failed`, `none_failed`, `none_failed_min_one_success`, `always`.

## Dynamic Task Mapping (Airflow 2.3+)

```python
@task
def get_files():
    return ["a.csv", "b.csv", "c.csv"]

@task
def process_file(filename):
    print(f"processing {filename}")

process_file.expand(filename=get_files())     # creates one mapped task instance per item
```

## Scheduling

```python
schedule="@daily"          # presets: @once, @hourly, @daily, @weekly, @monthly, @yearly
schedule="0 6 * * *"          # cron: 6 AM every day
schedule="0 */4 * * *"           # every 4 hours
schedule=timedelta(hours=2)         # every 2 hours, relative
schedule=None                          # DAG only runs when manually/externally triggered

# Datasets (data-aware scheduling, Airflow 2.4+) — trigger a DAG when another DAG updates a dataset
from airflow.datasets import Dataset

my_dataset = Dataset("s3://bucket/path/")

# Producer DAG task
@task(outlets=[my_dataset])
def produce():
    ...

# Consumer DAG — triggered automatically when my_dataset is updated
with DAG(dag_id="consumer", schedule=[my_dataset], start_date=..., catchup=False):
    ...
```

## Variables & Connections

```python
from airflow.models import Variable
from airflow.hooks.base import BaseHook

my_var = Variable.get("my_key")
my_var_json = Variable.get("my_key", deserialize_json=True)
Variable.set("my_key", "value")

conn = BaseHook.get_connection("my_conn_id")   # retrieves host/login/password/extra from Airflow Connections

# Better: use provider-specific hooks
from airflow.providers.postgres.hooks.postgres import PostgresHook
pg_hook = PostgresHook(postgres_conn_id="my_postgres")
records = pg_hook.get_records("SELECT * FROM table")
```

## Error Handling & Callbacks

```python
def on_failure_callback(context):
    task_instance = context["task_instance"]
    print(f"Task {task_instance.task_id} failed")
    # send Slack/PagerDuty alert here

default_args = {
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=30),
    "on_failure_callback": on_failure_callback,
    "on_success_callback": None,
    "execution_timeout": timedelta(hours=1),      # kill the task if it runs too long
    "sla": timedelta(hours=2),                       # SLA miss triggers a separate alert (doesn't fail the task)
}
```

## CLI Commands

```bash
airflow dags list
airflow dags trigger my_dag_id
airflow dags backfill my_dag_id -s 2026-01-01 -e 2026-01-31
airflow dags pause my_dag_id
airflow dags unpause my_dag_id

airflow tasks list my_dag_id
airflow tasks test my_dag_id my_task_id 2026-07-17   # run a task in isolation, no DB writes

airflow db init
airflow db upgrade
airflow users create --username admin --role Admin --email a@a.com --firstname A --lastname B --password admin

airflow webserver --port 8080
airflow scheduler
```

## Best Practices

- **Idempotency** — tasks should produce the same result if re-run for the same logical date; avoid `datetime.now()` inside tasks, use `{{ ds }}`/logical date instead.
- **Keep DAG files lightweight** — heavy imports or top-level code (like DB queries) at module scope slow down DAG parsing, which the scheduler does repeatedly.
- **Don't pass large data via XCom** — write intermediate data to S3/GCS/a table, pass only the reference (path/ID) through XCom.
- **Use `catchup=False`** unless you specifically want automatic backfilling of missed schedule intervals on deploy.
- **Set `execution_timeout`** on tasks to avoid a hung task blocking a worker slot indefinitely.
- **Use pools** to limit concurrency against a constrained resource (e.g., a database), independent of overall parallelism settings.
- **Prefer TaskFlow API + dynamic task mapping** for new Python-centric DAGs — cleaner than manual XCom push/pull and `PythonOperator` boilerplate.
- **Version-control and code-review DAGs** like any other production code — a bad DAG can silently stop scheduling other DAGs if it fails to parse.
