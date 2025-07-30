import os
import argparse 
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, DoubleType, IntegerType, StringType
from pyspark.sql.functions import from_json, col

parser = argparse.ArgumentParser(description='Spark Kafka Stream Consumer for Weather Data.')
parser.add_argument('--kafka-broker', type=str, default='kafka:9092',
                    help='Kafka bootstrap servers (e.g., kafka:9092)')
parser.add_argument('--topic', type=str, default='weather_data',
                    help='Kafka topic to subscribe to')
parser.add_argument('--processing-time-interval', type=str, default='10 seconds',
                    help='Interval for micro-batch processing (e.g., "10 seconds", "1 minute")')
parser.add_argument('--output-path', type=str, default='/data/weather_csv',
                    help='Base path for CSV output')
parser.add_argument('--checkpoint-path', type=str, default='/data/checkpoint_weather',
                    help='Checkpoint location for CSV output')

args = parser.parse_args()

# Usar los argumentos
KAFKA_BROKER = args.kafka_broker
KAFKA_TOPIC = args.topic
PROCESSING_INTERVAL = args.processing_time_interval
CSV_OUTPUT_PATH = args.output_path
CSV_CHECKPOINT_PATH = args.checkpoint_path

spark = SparkSession.builder.appName("KafkaWeatherConsumer").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

schema = StructType() \
    .add("timestamp", DoubleType()) \
    .add("temperature", DoubleType()) \
    .add("weathercode", IntegerType()) \
    .add("is_day", IntegerType()) \
    .add("raw_time", StringType())

df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) 
    .option("subscribe", KAFKA_TOPIC)              
    .option("startingOffsets", "earliest")
    .load()

df_parsed = df_raw.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json(col("json_str"), schema).alias("data")) \
    .select("data.*")

query_console = df_parsed.writeStream \
    .format("console") \
    .outputMode("append") \
    .start()

query_csv = df_parsed.writeStream \
    .format("csv") \
    .option("path", CSV_OUTPUT_PATH) 
    .option("checkpointLocation", CSV_CHECKPOINT_PATH) 
    .outputMode("append")
    .trigger(processingTime=PROCESSING_INTERVAL)
    .start()

query_console.awaitTermination(timeout=60) 
query_csv.awaitTermination(timeout=60) 
