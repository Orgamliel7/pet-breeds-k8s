# Fetches random cat/dog breeds from an API and sends the data to "pets" Kafka topic
import requests # type: ignore
import json
import time
import random
from kafka import KafkaProducer # type: ignore
import os
API_URLS = [
    "https://api.thedogapi.com/v1/breeds",
    "https://api.thecatapi.com/v1/breeds"
]
KAFKA_TOPIC = 'pets'
# Get Kafka brokers from 'KAFKA_SERVER' env var, with defaults  
KAFKA_SERVER = os.getenv(
    'KAFKA_SERVER',
    'kafka-0.kafka:9092,kafka-1.kafka:9092,kafka-2.kafka:9092'
).split(',')
# Function to fetch cat and dog breeds from the APIs
def fetch_breeds():
    all_breeds = []
    for url in API_URLS:
        try:
            response = requests.get(url)
            if response.status_code == 200:   
                breeds = response.json() # Parse JSON to Python obj
                all_breeds.extend(breeds)
            else:
                print(f"Unexpected status code from {url}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {url}: {e}")
    return all_breeds
# Function to get a random subset of breeds
def get_random_breeds(breeds, n=10):
    return random.sample(breeds, min(n, len(breeds)))
# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)
if __name__ == "__main__":
    print("Producer starting...")
    while True:
        try:
            all_breeds = fetch_breeds()
            if all_breeds:
                random_breeds = get_random_breeds(all_breeds, 10)
                for breed in random_breeds:
                    producer.send(KAFKA_TOPIC, breed)
                print(f"Sent {len(random_breeds)} breeds to Kafka")
            else:
                print("No breeds fetched")
            time.sleep(60)  # Wait for 60 seconds before next fetch
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(10)  # Wait a bit before retrying in case of error