FROM apache/airflow:2.9.1-python3.10

ARG DOCKER_GID=984

USER root

RUN groupadd -g ${DOCKER_GID} docker_host_group || true

RUN usermod -aG docker_host_group airflow

USER airflow

RUN pip install --no-cache-dir \
    apache-airflow-providers-docker \
    docker \
    kafka-python