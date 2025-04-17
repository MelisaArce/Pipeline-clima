# Makefile
# Mostrar comandos disponibles
help:
	@echo "Comandos disponibles:"
	@echo "  make stack-up         - Levanta Kafka, Spark y PostgreSQL"
	@echo "  make airflow-up       - Levanta los servicios de Airflow"
	@echo "  make stack-down       - Baja el stack de Kafka, Spark y PostgreSQL"
	@echo "  make airflow-down     - Baja los servicios de Airflow"
	@echo "  make airflow-logs     - Muestra logs de Airflow Webserver"  
	@echo "  make up-all           - Levanta todos los servicios (Airflow y stack)"
	@echo "  make down-all         - Baja todos los servicios (Airflow y stack)"
	@echo "  make postgres-client  - Accede al cliente de PostgreSQL"  

# Variables
AIRFLOW_COMPOSE=docker-compose-airflow.yml
STACK_COMPOSE=docker-compose.yml

airflow-up:
	docker compose -f $(AIRFLOW_COMPOSE) up -d

airflow-logs:
	docker compose -f $(AIRFLOW_COMPOSE) logs -f

airflow-down:
	docker compose -f $(AIRFLOW_COMPOSE) down

stack-up:
	docker compose -f $(STACK_COMPOSE) up -d

stack-down:
	docker compose -f $(STACK_COMPOSE) down

up-all:
	docker compose -f $(STACK_COMPOSE) up -d
	docker compose -f $(AIRFLOW_COMPOSE) up -d

down-all:
	docker compose -f $(AIRFLOW_COMPOSE) down
	docker compose -f $(STACK_COMPOSE) down

postgres-client:
	docker exec -it postgres-weather psql -U airflow-user -d weather