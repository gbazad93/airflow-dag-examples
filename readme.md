# Airflow Tutorial DAGs

This repository contains a set of example Apache Airflow DAGs designed to teach key concepts step by step:

- **basic_dag_tutorial.py**  
  A “Hello World” DAG with a single DummyOperator, demonstrating file structure and manual trigger.

  - **basic_dag_tutorial_decorators.py**  
  The same Hello World DAG using the `@dag`/`@task` decorator API for cleaner task definitions.

- **basic_dag04.py**  
  Demonstrates a select database query (`SELECT COUNT(*)`) and an insert task using AirFlow connections and the decorator style.
