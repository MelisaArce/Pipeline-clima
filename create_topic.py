from kafka.admin import KafkaAdminClient, NewTopic

# Configuración del broker y tópico
KAFKA_BROKER = "kafka:9092"
TOPIC = "weather_data"

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
