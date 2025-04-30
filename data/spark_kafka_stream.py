from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, FloatType, IntegerType
from transformaciones import renombrar_columnas
import os


pg_host = os.getenv("PG_HOST")
pg_port = os.getenv("PG_PORT")
pg_db = os.getenv("PG_DB")
pg_user = os.getenv("PG_USER")
pg_password = os.getenv("PG_PASSWORD")
pg_table = os.getenv("PG_TABLE_WEATHER")
spark_master = os.getenv("SPARK_MASTER_URL")
kafka_broker = os.getenv("KAFKA_BROKER")
topic = os.getenv("KAFKA_TOPIC")

pg_url = f"jdbc:postgresql://{pg_host}:{pg_port}/{pg_db}"


spark = SparkSession.builder \
    .master(spark_master) \
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
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topic) \
    .option("startingOffsets", "earliest") \
    .load()

# Parsear JSON del valor
weather_df = df.selectExpr("CAST(value AS STRING) as json_string") \
    .select(from_json(col("json_string"), schema).alias("data")) \
    .select("data.*")


def proceso_batch(batch_df, batch_id):
    # Aplicar transformación dentro del batch
    df_transformado = renombrar_columnas(batch_df)
    
    # Guardar en PostgreSQL
    df_transformado.write \
        .format("jdbc") \
        .option("url", pg_url) \
        .option("dbtable", pg_table) \
        .option("user", pg_user) \
        .option("password", pg_password) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

        
query = weather_df.writeStream \
    .foreachBatch(proceso_batch) \
    .outputMode("append") \
    .start()

query.awaitTermination()