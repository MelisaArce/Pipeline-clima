from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# default_args = {
#     'owner': 'mel',
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }

with DAG(
    dag_id='clima_pipeline',
    default_args=default_args,
    description='Orquesta el flujo API > Kafka > Spark > PostgreSQL',
    start_date=datetime(2025, 4, 17),
    schedule_interval='0 8,13,20 * * *',  # 08:00, 13:00, 20:00
    catchup=False,
    tags=['clima', 'kafka', 'spark'],
) as dag:

    run_api_producer = DockerOperator(
        task_id='run_api_producer',
        image='producer',  # Usa el nombre del servicio del docker-compose
        api_version='auto',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        network_mode='airflow_pipeline_net',  # nombre de tu red
        command="",  # si tu contenedor corre automáticamente, dejalo vacío
        mounts=[],
    )

    run_spark_processing = SparkSubmitOperator(
    task_id='run_spark_processing',
    application='/data/spark_kafka_stream.py',  # tu ruta actual
    conn_id='spark_default',
    verbose=True,
    application_args=['--topic', 'weather_data'],  # opcional, si lo usás en el script
)


    run_api_producer >> run_spark_processing
