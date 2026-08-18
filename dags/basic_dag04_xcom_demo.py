"""Passing real query results between tasks with XCom.

SQLAlchemy Row objects are not JSON serialisable, so they cannot go into XCom as
they are. This DAG fetches rows, converts them to plain dicts (with dates turned
into ISO strings), hands them to the next task via XCom, and summarises them.

Keep XCom payloads small: it is metadata plumbing, not a data pipe. For large
result sets, write to storage and pass a path instead.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from airflow.decorators import dag, task
from sqlalchemy import text

from db.connection import session_scope

SOURCE_TABLE = "dbo.demo_events"
MAX_ROWS = 100


def _json_safe(value: Any) -> Any:
    """Convert values SQL drivers return into something XCom can serialise."""
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


@dag(
    dag_id="basic_dag04_xcom_demo",
    description="Fetch rows, serialise them to dicts, pass them through XCom.",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["tutorial", "sql", "xcom"],
)
def basic_dag04_xcom_demo() -> None:
    @task
    def fetch_rows() -> list[dict[str, Any]]:
        """Read a bounded number of rows and return them as JSON-safe dicts."""
        statement = text(
            f"SELECT TOP (:max_rows) event_id, event_name, event_date FROM {SOURCE_TABLE} "
            "ORDER BY event_date DESC"
        )
        with session_scope() as session:
            result = session.execute(statement, {"max_rows": MAX_ROWS})
            rows = [
                {key: _json_safe(value) for key, value in row.items()}
                for row in result.mappings()
            ]
        print(f"fetched {len(rows)} rows from {SOURCE_TABLE}")
        return rows

    @task
    def summarise(rows: list[dict[str, Any]]) -> None:
        """Consume the XCom payload produced by fetch_rows."""
        if not rows:
            print("no rows to summarise")
            return
        newest = rows[0].get("event_date")
        oldest = rows[-1].get("event_date")
        print(f"{len(rows)} rows, newest {newest}, oldest {oldest}")

    summarise(fetch_rows())


basic_dag04_xcom_demo()
