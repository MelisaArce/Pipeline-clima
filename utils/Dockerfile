FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install kafka-python
CMD ["python", "consumer_to_spark.py"]
