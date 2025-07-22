FROM apache/airflow:2.9.1-python3.10

USER airflow

# Instalar paquetes adicionales como el usuario airflow
RUN pip install --no-cache-dir \
    apache-airflow-providers-docker \
    docker \
    kafka-python

