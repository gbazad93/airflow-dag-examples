"""Talking to a database from a DAG.

Two tasks, decorator style:

1. count_rows  - runs SELECT COUNT(*) against a table
2. insert_row  - writes an audit row using the count from the first task

Credentials come from the Airflow connection my_mssql_conn via
db.connection.session_scope(), so nothing sensitive lives in this file.
"""

from __future__ import annotations

from datetime import datetime, timezone

from airflow.decorators import dag, task
from sqlalchemy import text

from db.connection import session_scope

SOURCE_TABLE = "dbo.demo_events"
AUDIT_TABLE = "dbo.demo_audit"


@dag(
    dag_id="basic_dag04",
    description="SELECT COUNT(*) then INSERT an audit row using an Airflow connection.",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["tutorial", "sql"],
)
def basic_dag04() -> None:
    @task
    def count_rows() -> int:
        """Return the number of rows currently in the source table."""
        with session_scope() as session:
            result = session.execute(text(f"SELECT COUNT(*) FROM {SOURCE_TABLE}"))
            row_count = int(result.scalar_one())
        print(f"{SOURCE_TABLE} currently holds {row_count} rows")
        return row_count

    @task
    def insert_row(row_count: int) -> None:
        """Write one audit row recording what the count task saw."""
        statement = text(
            f"INSERT INTO {AUDIT_TABLE} (source_table, row_count, checked_at) "
            "VALUES (:source_table, :row_count, :checked_at)"
        )
        with session_scope() as session:
            session.execute(
                statement,
                {
                    "source_table": SOURCE_TABLE,
                    "row_count": row_count,
                    "checked_at": datetime.now(timezone.utc),
                },
            )

    insert_row(count_rows())


basic_dag04()
