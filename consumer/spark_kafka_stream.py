import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, DoubleType, IntegerType, StringType
from pyspark.sql.functions import from_json, col

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
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "weather_data") \
    .option("startingOffsets", "earliest") \
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
    .option("path", "/data") \
    .option("checkpointLocation", "/data/checkpoint") \
    .outputMode("append") \
    .trigger(processingTime='10 seconds') \
    .start()

query_console.awaitTermination()
query_csv.awaitTermination()
