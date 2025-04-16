"""
Script para crear el tópico 'weather_data' en Kafka.

Uso futuro:
- Puede ser llamado desde un DAG en Airflow con un PythonOperator.
- Requiere que Kafka esté corriendo y accesible en KAFKA_BROKER.
- Asegúrate de que el tópico no exista antes de ejecutar este script.
"""

from kafka.admin import KafkaAdminClient, NewTopic
import os
# Configuración del broker y tópico
KAFKA_BROKER = os.getenv("KAFKA_BROKER")
TOPIC = os.getenv("KAFKA_TOPIC")

# Crear un administrador de Kafka
admin_client = KafkaAdminClient(
    bootstrap_servers=KAFKA_BROKER,
    client_id="topic_creator"
)

# Intentar crear el tópico
try:
    topic_list = [NewTopic(name=TOPIC, num_partitions=1, replication_factor=1)]
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
    print(f"Tópico '{TOPIC}' creado exitosamente.")
except Exception as e:
    print(f"El tópico '{TOPIC}' ya existe o hubo un error: {e}")

admin_client.close()
