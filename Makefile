# Makefile

# ================================
# Comandos disponibles
# ================================
help:
	@echo "Comandos disponibles:"
	@echo "  make stack-up         - Levanta Kafka, Spark y PostgreSQL"
	@echo "  make airflow-up       - Levanta los servicios de Airflow"
	@echo "  make stack-down       - Baja el stack de Kafka, Spark y PostgreSQL"
	@echo "  make airflow-down     - Baja los servicios de Airflow"
	@echo "  make airflow-logs     - Muestra logs de Airflow Webserver"
	@echo "  make build-airflow    - Construye la imagen custom de Airflow"
	@echo "  make up-all           - Levanta todos los servicios (Airflow y stack)"
	@echo "  make down-all         - Baja todos los servicios (Airflow y stack)"
	@echo "  make postgres-client  - Accede al cliente de PostgreSQL"

# ================================
# Variables
# ================================
STACK_COMPOSE := docker-compose.yml
AIRFLOW_COMPOSE := docker-compose-airflow.yml

STACK_PROJECT := clima_stack
AIRFLOW_PROJECT := clima_airflow

UP_FLAGS := -d
ifeq ($(REMOVE_ORPHANS),1)
	UP_FLAGS += --remove-orphans
endif

# ================================
# Comandos del Stack base
# ================================
stack-up:
	docker compose -f $(STACK_COMPOSE) --project-name $(STACK_PROJECT) up $(UP_FLAGS)

stack-down:
	docker compose -f $(STACK_COMPOSE) --project-name $(STACK_PROJECT) down

# ================================
# Comandos de Airflow
# ================================
airflow-up:
	docker compose -f $(AIRFLOW_COMPOSE) --project-name $(AIRFLOW_PROJECT) up $(UP_FLAGS)

airflow-down:
	docker compose -f $(AIRFLOW_COMPOSE) --project-name $(AIRFLOW_PROJECT) down

airflow-logs:
	docker compose -f $(AIRFLOW_COMPOSE) --project-name $(AIRFLOW_PROJECT) logs -f

# ================================
# Comandos combinados
# ================================
up-all:
	docker compose -f $(STACK_COMPOSE) --project-name $(STACK_PROJECT) up $(UP_FLAGS)
	docker compose -f $(AIRFLOW_COMPOSE) --project-name $(AIRFLOW_PROJECT) up $(UP_FLAGS)

down-all:
	docker compose -f $(AIRFLOW_COMPOSE) --project-name $(AIRFLOW_PROJECT) down
	docker compose -f $(STACK_COMPOSE) --project-name $(STACK_PROJECT) down

# ================================
# Cliente de PostgreSQL
# ================================
postgres-client:
	docker exec -it postgres-weather psql -U airflow-user -d weather

# ================================
# Build personalizado de Airflow
# ================================
build-airflow:
	docker build -t custom-airflow:latest .
