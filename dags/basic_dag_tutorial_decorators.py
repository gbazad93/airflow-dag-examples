"""Hello World DAG - TaskFlow (decorator) flavour.

Same idea as basic_dag_tutorial.py, but written with the @dag / @task decorator
API. Values returned from a @task function are pushed to XCom automatically, so
wiring tasks together is just a normal Python call.
"""

from __future__ import annotations

from datetime import datetime

from airflow.decorators import dag, task


@dag(
    dag_id="basic_dag_tutorial_decorators",
    description="Hello World DAG written with the TaskFlow API.",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["tutorial", "basics", "taskflow"],
)
def basic_dag_tutorial_decorators() -> None:
    @task
    def say_hello() -> str:
        message = "Hello from the TaskFlow API!"
        print(message)
        return message

    @task
    def shout(message: str) -> None:
        print(message.upper())

    shout(say_hello())


basic_dag_tutorial_decorators()
