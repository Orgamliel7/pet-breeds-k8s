# Fetches random cat/dog breeds from an API and sends the data to "pets" Kafka topic
import requests  # type: ignore
import json
import time
import random
from kafka import KafkaProducer  # type: ignore
import os

API_URLS = [
    "https://api.thedogapi.com/v1/breeds",
    "https://api.thecatapi.com/v1/breeds"
]
# Get Kafka brokers from 'KAFKA_SERVER' env var, with defaults  
KAFKA_SERVER = os.getenv(
    'KAFKA_SERVER',
    'kafka-0.kafka:9092,kafka-1.kafka:9092,kafka-2.kafka:9092'
).split(',')
KAFKA_TOPIC = 'pets'

# Function to fetch cat and dog breeds from the APIs
def fetch_breeds():
    all_breeds = []
    for url in API_URLS:
        try:
            response = requests.get(url)
            if response.status_code == 200: # Parsing from JSON to Python obj  
                breeds = response.json() 
                all_breeds.extend(breeds)
            else:
                print(
                    f"Unexpected status code from {url}: "
                    f"{response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {url}: {e}")
    return all_breeds

# Function to get a random subset of breeds
def get_random_breeds(breeds, n=10):
    return random.sample(breeds, min(n, len(breeds)))


def main():
    # Init of Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda x: json.dumps(x).encode('utf-8') # Convert the message from Python obj to a JSON string + encode it as bytes for Kafka 
    )

    while True:
        all_breeds = fetch_breeds()
        if all_breeds:
            random_breeds = get_random_breeds(all_breeds, 10)
            for breed in random_breeds:
                producer.send(KAFKA_TOPIC, breed) # Each breed is sent to the Lambda function
            print(f"Sent {len(random_breeds)} breeds to Kafka")
        else:
            print("No breeds fetched")
        time.sleep(60) # Wait for 60 seconds before next fetch


if __name__ == "__main__":
    main()
