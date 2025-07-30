FROM apache/airflow:3.0.1

ARG DOCKER_GID=984
USER root

RUN groupadd -g ${DOCKER_GID} docker_host_group || true
RUN usermod -aG docker_host_group airflow

USER airflow
COPY requirements.txt /
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt