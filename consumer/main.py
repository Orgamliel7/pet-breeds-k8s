# Reads data from the "pets" Kafka topic and prints it to stdout
import json
import os
from kafka import KafkaConsumer  # type: ignore

KAFKA_TOPIC = 'pets'
# Get Kafka brokers from 'KAFKA_SERVER' env var, with defaults  
KAFKA_SERVER = os.getenv(
    'KAFKA_SERVER',
    'kafka-0.kafka:9092,kafka-1.kafka:9092,kafka-2.kafka:9092'
).split(',')

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')) # Deserialize message from bytes to Python obj
)

if __name__ == "__main__":
    for message in consumer:
        print(f"Received: {message.value}") # Print the received message value to stdout
