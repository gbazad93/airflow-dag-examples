# Airflow Tutorial DAGs

A small, self-contained set of Apache Airflow DAGs that build up from "hello
world" to querying a database and passing results between tasks. Each file is
meant to be read top to bottom.

## Repository layout

```
dags/
  basic_dag_tutorial.py             # one EmptyOperator task, manual trigger
  basic_dag_tutorial_decorators.py  # same DAG with the @dag / @task API
  basic_dag04.py                    # SELECT COUNT(*) then an audit INSERT
  basic_dag04_xcom_demo.py          # rows -> JSON-safe dicts -> XCom
db/
  connection.py                     # engine/session built from an Airflow connection
requirements.txt
```

## The examples

**1. dags/basic_dag_tutorial.py** - the anatomy of a DAG file: a `with DAG(...)` block,
an explicit `start_date`, `catchup=False`, and a single `EmptyOperator` task you
trigger by hand from the UI.

**2. dags/basic_dag_tutorial_decorators.py** - the same DAG written with the
TaskFlow API. A value returned from a `@task` function is pushed to XCom
automatically, so wiring tasks together looks like a normal Python call.

**3. dags/basic_dag04.py** - talking to a database. One task runs
`SELECT COUNT(*)`, the next writes an audit row using that count. Credentials
come from an Airflow connection, never from the DAG file.

**4. dags/basic_dag04_xcom_demo.py** - SQLAlchemy `Row` objects are not JSON
serialisable, so this DAG converts them to plain dicts (dates become ISO
strings) before handing them to the next task through XCom. The result set is
capped on purpose: XCom is metadata plumbing, not a data channel.

## A note on DummyOperator

Older versions of this tutorial used `DummyOperator`. It was deprecated in
Airflow 2.4 and removed in Airflow 3; `EmptyOperator`
(`airflow.operators.empty.EmptyOperator`) is the drop-in replacement and is what
these DAGs use.

## Prerequisites

- Apache Airflow 2.7 or newer (developed against 2.9)
- Python 3.9+
- For the SQL examples: `pyodbc`, a system ODBC driver, and
  `apache-airflow-providers-microsoft-mssql`
- An Airflow connection whose id is `my_mssql_conn`

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

### Connection format

`db/connection.py` builds a SQLAlchemy engine from `Connection.get_uri()`, so the
connection has to carry both the dialect and the ODBC driver name, for example:

```
mssql+pyodbc://user:password@my-server.database.windows.net:1433/my_db?driver=ODBC+Driver+18+for+SQL+Server
```

Store it once with the CLI:

```bash
airflow connections add my_mssql_conn --conn-uri "mssql+pyodbc://..."
```

## Running the examples

```bash
export AIRFLOW_HOME="$(pwd)"
airflow standalone
```

Airflow picks up the `dags/` folder, and the `db` package sits next to it on the
Python path. Trigger a DAG from the UI and read the task logs - every example
prints what it did.

## Helper API

```python
from db.connection import get_engine, get_session, session_scope

with session_scope() as session:  # commits on success, rolls back on error
    rows = session.execute(...)
```

## License

MIT - see [LICENSE](LICENSE).
