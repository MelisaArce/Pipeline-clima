import json
import time
import requests
from kafka import KafkaProducer
from dotenv import load_dotenv
import os

load_dotenv()

KAFKA_BROKER="kafka:9092"
TOPIC="weather_data"

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")
LAT = os.getenv("LAT")
LON = os.getenv("LON")
# Validar variables requeridas
required_vars = {
    "APP_ID": APP_ID,
    "APP_KEY": APP_KEY,
    "LAT": LAT,
    "LON": LON,
    "KAFKA_BROKER": KAFKA_BROKER,
    "TOPIC": TOPIC
}

missing = [var for var, value in required_vars.items() if not value]

if missing:
    print(f"Faltan las siguientes variables de entorno en el archivo .env: {', '.join(missing)}")
    print("Por favor, asegurate de que el archivo .env esté completo y correctamente cargado.")
    exit(1)



API_URL = f"http://api.weatherunlocked.com/api/current/{LAT},{LON}?app_id={APP_ID}&app_key={APP_KEY}"
# Configurar el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    api_version=(3,4,0)
    
)

def fetch_weather():
    try:
        print(f"Realizando solicitud a: {API_URL}")
        response = requests.get(API_URL)
     
        
        print(f"Respuesta de la API (Código {response.status_code}): {response.text}") 
        
        if response.status_code == 200:
            data = response.json()
            print(f"Datos completos recibidos: {data}")  
            
            if not data:
                print("La API devolvió un JSON vacío.")
                return None
            
            # Agregar timestamp y devolver toda la data
            data["timestamp"] = time.time()
            return data
        
        else:
            print(f"Error al obtener datos: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
    
    return None

# Obtener datos del clima
weather_datos = fetch_weather()

# Enviar mensaje solo si es válido
if weather_datos:
    print(f"Enviando mensaje a Kafka: {weather_datos}")
    try:
        producer.send(TOPIC, weather_datos).get(timeout=10)
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")
else:
    print("No se enviaron datos porque la respuesta fue inválida.")

producer.close()