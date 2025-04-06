# [DEPRECATED] Consumer para guardar mensajes Kafka en JSON plano.
# Reemplazado por Spark Structured Streaming.

import time
from kafka import KafkaConsumer, errors
import json
import os

DATA_DIR = "/data/raw"
os.makedirs(DATA_DIR, exist_ok=True)

MAX_RETRIES = 20
for i in range(MAX_RETRIES):
    try:
        print("Intentando conectarse a Kafka...")
        consumer = KafkaConsumer(
            "weather_data",
            bootstrap_servers="kafka:9092",
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id="weather_consumer",
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            api_version=(3,4,0)
        )
        print("✅ Conexión a Kafka exitosa")
        break
    except errors.NoBrokersAvailable:
        print(f"Kafka aún no disponible. Reintentando {i+1}/{MAX_RETRIES}")
        time.sleep(5)
else:
    raise Exception("No se pudo conectar con Kafka después de varios intentos")

output_path = os.path.join(DATA_DIR, "weather_data.json")

print(f"✍️ Escribiendo mensajes en: {output_path}")
with open(output_path, "a") as f:
    for message in consumer:
        print(f"Mensaje recibido: {message.value}")
        json.dump(message.value, f)
        f.write("\n")
