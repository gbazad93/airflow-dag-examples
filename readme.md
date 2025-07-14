# Airflow Tutorial DAGs

This repository contains a set of example Apache Airflow DAGs designed to teach key concepts step by step:

- **basic_dag_tutorial.py**  
  A “Hello World” DAG with a single DummyOperator, demonstrating file structure and manual trigger.

  - **basic_dag_tutorial_decorators.py**  
  The same Hello World DAG using the `@dag`/`@task` decorator API for cleaner task definitions.

- **basic_dag04.py**  
  Demonstrates a select database query (`SELECT COUNT(*)`) and an insert task using AirFlow connections and the decorator style.

- **basic_dag04_xcom_demo.py**  
  Shows how to fetch rows from Azure SQL, serialize them to JSON-friendly dicts, and pass them between tasks via XCom.


## Prerequisites

- Apache Airflow ≥ 2.0  
- Python 3.8+  
- `sqlalchemy`, and an ODBC driver (`pyodbc` or similar)  
- Airflow Connection ID: `my_mssql_conn` pointing to your SQL instance  
- A helper module `db/connection.py` exporting:

    def get_session(conn_id: str = "my_mssql_conn") -> Session
