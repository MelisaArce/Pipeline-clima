# Makefile



up-all:
	docker compose -f docker-compose-airflow.yml -f docker-compose.yml up -d --build

down-all:
	docker compose -f docker-compose-airflow.yml -f docker-compose.yml down

