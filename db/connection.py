"""Database helpers used by the example DAGs.

The DAGs never hard-code credentials: they ask Airflow for a connection
(default id: my_mssql_conn) and build a SQLAlchemy engine/session from it, so
the same code works locally and in production.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from airflow.hooks.base import BaseHook
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

DEFAULT_CONN_ID = "my_mssql_conn"


def get_engine(conn_id: str = DEFAULT_CONN_ID) -> Engine:
    """Build a SQLAlchemy engine from an Airflow connection.

    Args:
        conn_id: Airflow connection id, configured in Admin -> Connections.

    Returns:
        A SQLAlchemy Engine with pre-ping enabled so stale pooled connections
        are recycled instead of raising on the next task run.
    """
    conn = BaseHook.get_connection(conn_id)
    return create_engine(conn.get_uri(), pool_pre_ping=True, future=True)


def get_session(conn_id: str = DEFAULT_CONN_ID) -> Session:
    """Return a new SQLAlchemy session for the given Airflow connection.

    The caller owns the session and is responsible for closing it. Prefer
    session_scope() unless you need manual control.
    """
    factory = sessionmaker(bind=get_engine(conn_id), future=True)
    return factory()


@contextmanager
def session_scope(conn_id: str = DEFAULT_CONN_ID) -> Iterator[Session]:
    """Session context manager that commits on success and rolls back on error."""
    session = get_session(conn_id)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
