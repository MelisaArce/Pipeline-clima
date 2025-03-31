import json
import time
import requests
from kafka import KafkaProducer

# Configuración de la API del clima
APP_ID = "a45e9457"
APP_KEY = "c043bf1310a6a0f16857fb6bb48d931a"
KAFKA_BROKER = "kafka:9092"  # Dirección del broker en la red de Docker
TOPIC = "weather_data"

API_URL = "http://api.weatherunlocked.com/api/current/40.71,-74.00?app_id=a45e9457&app_key=c043bf1310a6a0f16857fb6bb48d931a"
# Configurar el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    api_version=(3,4,0)
    
)

def fetch_weather():
    try:
        print(f"🔍 Realizando solicitud a: {API_URL}")
        response = requests.get(API_URL)
        
        print(f"📩 Respuesta de la API (Código {response.status_code}): {response.text}") 
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Datos completos recibidos: {data}")  
            
            if not data:
                print("⚠️ La API devolvió un JSON vacío.")
                return None
            
            # ✅ Agregar timestamp y devolver toda la data
            data["timestamp"] = time.time()
            return data
        
        else:
            print(f"⚠️ Error al obtener datos: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error en la solicitud: {e}")
    
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
    print("⚠️ No se enviaron datos porque la respuesta fue inválida.")

producer.close()
