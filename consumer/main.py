import json
import os
from kafka import KafkaConsumer  # type: ignore

KAFKA_TOPIC = 'pets'
KAFKA_SERVER = os.getenv(
    'KAFKA_SERVER',
    'kafka-0.kafka:9092,kafka-1.kafka:9092,kafka-2.kafka:9092'
).split(',')

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

if __name__ == "__main__":
    for message in consumer:
        print(f"Received: {message.value}")
