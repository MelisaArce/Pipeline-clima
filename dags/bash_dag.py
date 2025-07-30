from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='simple_test_dag',
    start_date=datetime(2023, 1, 1),      
    catchup=False,
    tags=['testing'],
) as dag:
    print_date_task = BashOperator(
        task_id='print_the_date',
        bash_command='echo "La fecha actual es: $(date)"',
    )