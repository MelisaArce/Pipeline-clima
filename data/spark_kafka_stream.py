from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, FloatType

# Crear la sesión de Spark
spark = SparkSession.builder \
    .master(spark_master) \
    .appName("KafkaToSparkStreaming") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Definir el esquema esperado del JSON (ajustalo según tu producer)
schema = StructType() \
    .add("location", StringType()) \
    .add("temperature", FloatType()) \
    .add("description", StringType()) \
    .add("timestamp", StringType())

# Leer desde Kafka
df_kafka = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:29092") \
    .option("subscribe", "weather_topic") \
    .load()

# Parsear el valor como JSON
df_valores = df_kafka.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json("json_str", schema).alias("data")) \
    .select("data.*")

# Mostrar en consola
query = df_valores.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
