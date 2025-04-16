# Makefile

# Variables
AIRFLOW_COMPOSE=docker-compose-airflow.yml
STACK_COMPOSE=docker-compose.yml

# Levantar Airflow
airflow-up:
	docker compose -f $(AIRFLOW_COMPOSE) up -d

# Ver logs de Airflow
airflow-logs:
	docker compose -f $(AIRFLOW_COMPOSE) logs -f

# Apagar Airflow
airflow-down:
	docker compose -f $(AIRFLOW_COMPOSE) down

# Levantar el stack principal (Kafka, Spark, Postgres, etc.)
stack-up:
	docker compose -f $(STACK_COMPOSE) up -d

# Apagar el stack principal
stack-down:
	docker compose -f $(STACK_COMPOSE) down

# Ver logs del stack principal
stack-logs:
	docker compose -f $(STACK_COMPOSE) logs -f

# Levantar ambos (Airflow y stack)
up-all:
	docker compose -f $(STACK_COMPOSE) up -d
	docker compose -f $(AIRFLOW_COMPOSE) up -d

# Bajar ambos
down-all:
	docker compose -f $(AIRFLOW_COMPOSE) down
	docker compose -f $(STACK_COMPOSE) down

postgres-db:
	docker exec -it postgres-weather psql -U airflow-user -d weather