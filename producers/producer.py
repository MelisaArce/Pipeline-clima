import json
import time
import requests
from kafka import KafkaProducer
from dotenv import load_dotenv
import os

load_dotenv()

KAFKA_BROKER= os.getenv("KAFKA_BROKER")
TOPIC= os.getenv("KAFKA_TOPIC")
LAT = os.getenv("LAT")
LON = os.getenv("LON")
# Validar variables requeridas
required_vars = {
    "LAT": LAT,
    "LON": LON,
    "KAFKA_BROKER": KAFKA_BROKER,
    "TOPIC": TOPIC
}

missing = [var for var, value in required_vars.items() if not value]

if missing:
    print(f"Faltan las siguientes variables de entorno en el archivo .env: {', '.join(missing)}")
    exit(1)



API_URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": LAT,
    "longitude": LON,
    "current_weather": True,
    "timezone": "America/Argentina/Buenos_Aires"
}

# Configurar el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    api_version=(3,4,0)
    
)

def fetch_weather():
    try:
        print(f"Realizando solicitud a Open-Meteo con params: {PARAMS}")
        response = requests.get(API_URL, params=PARAMS)
        print(f"Respuesta código {response.status_code}: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            current = data.get("current_weather")
            
            if not current:
                print("La API devolvió una respuesta sin 'current_weather'.")
                return None
            
            # Enriquecemos el mensaje
            enriched = {
                "timestamp": time.time(),
                "temperature": current["temperature"],
                "weathercode": current["weathercode"],
                "is_day": current["is_day"],
                "raw_time": current["time"]
            }
            return enriched

        else:
            print("Error al obtener datos.")
    except requests.exceptions.RequestException as e:
        print(f"Error de red: {e}")
    return None

weather_data = fetch_weather()

if weather_data:
    print(f"Enviando mensaje a Kafka: {weather_data}")
    try:
        producer.send(TOPIC, weather_data).get(timeout=10)
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")
else:
    print("No se enviaron datos debido a error en la API.")

producer.close()