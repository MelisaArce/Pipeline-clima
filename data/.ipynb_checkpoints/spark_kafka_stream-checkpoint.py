from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, FloatType, LongType, IntegerType


# Crear sesión de Spark
spark = SparkSession.builder \
    .master("spark://spark-master:7077")\
    .appName("KafkaToSparkStreaming") \
    .getOrCreate()

# Esquema del mensaje JSON esperado
schema = StructType() \
        .add("lat", StringType()) \
        .add("lon", StringType()) \
        .add("alt_m", FloatType()) \
        .add("alt_f", FloatType()) \
        .add("wx_desc", StringType()) \
        .add("wx_code", IntegerType()) \
        .add("wx_icon", StringType()) \
        .add("temp_c", FloatType()) \
        .add("temp_f", FloatType()) \
        .add("feelslike_c", FloatType()) \
        .add("feelslike_f", FloatType()) \
        .add("windspd_mph", IntegerType()) \
        .add("windspd_kmh", IntegerType()) \
        .add("windspd_kts", IntegerType()) \
        .add("windspd_ms", FloatType()) \
        .add("winddir_deg", IntegerType()) \
        .add("winddir_compass", StringType()) \
        .add("cloudtotal_pct", IntegerType()) \
        .add("humid_pct", IntegerType()) \
        .add("dewpoint_c", FloatType()) \
        .add("dewpoint_f", FloatType()) \
        .add("vis_km", FloatType()) \
        .add("vis_mi", FloatType()) \
        .add("slp_mb", IntegerType()) \
        .add("slp_in", FloatType())
    

# Leer el stream de Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "weather_data") \
    .option("startingOffsets", "earliest") \
    .load()

# Convertir el valor (que viene en bytes) a string y luego parsearlo como JSON
weather_df = df.selectExpr("CAST(value AS STRING) as json_string") \
    .select(from_json(col("json_string"), schema).alias("data")) \
    .select("data.*")

# Mostrar los datos por consola (para debug)
query = weather_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
