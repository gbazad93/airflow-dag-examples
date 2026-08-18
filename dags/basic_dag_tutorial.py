"""Hello World DAG.

The simplest possible DAG: a single task that does nothing. Use it to verify
that Airflow can parse files in your dags/ folder and to see the anatomy of a
DAG file before adding real work.

Note: older tutorials use DummyOperator, which was deprecated in Airflow 2.4
and removed in Airflow 3. EmptyOperator is the drop-in replacement.
"""

from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="basic_dag_tutorial",
    description="Hello World DAG with a single EmptyOperator task.",
    start_date=datetime(2024, 1, 1),
    schedule=None,  # trigger manually from the UI
    catchup=False,
    tags=["tutorial", "basics"],
) as dag:
    start = EmptyOperator(task_id="start")
