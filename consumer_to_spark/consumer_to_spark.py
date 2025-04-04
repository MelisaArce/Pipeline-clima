# Esperamos que el broker esté disponible
import time
from kafka import KafkaConsumer, errors
import json
import os

DATA_DIR = "/data/raw"

MAX_RETRIES = 10
for i in range(MAX_RETRIES):
    try:
        consumer = KafkaConsumer(
            "weather_data",
            bootstrap_servers="kafka:9092",
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='spark_etl_group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            api_version=(3,4,0)
        )
        break
    except errors.NoBrokersAvailable:
        print(f"Kafka aún no disponible. Reintentando {i+1}/{MAX_RETRIES}")
        time.sleep(5)
else:
    raise Exception("No se pudo conectar con Kafka después de varios intentos")

with open(f"{DATA_DIR}/weather_data.json", "a") as f:
    for message in consumer:
        json.dump(message.value, f)
        f.write("\n")

