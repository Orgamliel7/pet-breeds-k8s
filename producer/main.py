import requests
import json
import time
import random
from kafka import KafkaProducer
import os

API_URLS = [
    "https://api.thedogapi.com/v1/breeds",
    "https://api.thecatapi.com/v1/breeds"
]

KAFKA_BROKER = os.getenv('KAFKA_SERVER', 'kafka-0.kafka:9092,kafka-1.kafka:9092,kafka-2.kafka:9092')
KAFKA_TOPIC = 'pets'

def fetch_breeds():
    all_breeds = []
    for url in API_URLS:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                breeds = response.json()
                all_breeds.extend(breeds)
            else:
                print(f"Unexpected status code from {url}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {url}: {e}")
    return all_breeds

def get_random_breeds(breeds, n=10):
    return random.sample(breeds, min(n, len(breeds)))

def main():
    producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER],
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    while True:
        all_breeds = fetch_breeds()
        if all_breeds:
            random_breeds = get_random_breeds(all_breeds, 10)
            for breed in random_breeds:
                producer.send(KAFKA_TOPIC, breed)
            print(f"Sent {len(random_breeds)} breeds to Kafka")
        else:
            print("No breeds fetched")
        
        time.sleep(60)

if __name__ == "__main__":
    main()