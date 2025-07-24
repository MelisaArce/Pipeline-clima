from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'melisa',
    'depends_on_past': False,
    'start_date': datetime(2025, 7, 23),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='producer_weather_dag',
    default_args=default_args,
    description='Ejecuta el producer de clima 2 veces al día',
    schedule_interval='0 8,20 * * *',  # 08:00 y 20:00
    catchup=False,
) as dag:

    run_producer = DockerOperator(
    task_id='run_weather_producer',
    image='melisaarce/weather-producer:latest',
    container_name='producer_intento99',
    api_version='auto',
    auto_remove=True,
    docker_url='unix://var/run/docker.sock',
    network_mode='airflow_pipeline_net',
    mount_tmp_dir=False,
    command="python /app/producer.py",
    environment={
        "LAT": "-34.6037",
        "LON": "-58.3816",
        "KAFKA_BROKER": "kafka:9092",
        "TOPIC": "weather_data"
    }
)