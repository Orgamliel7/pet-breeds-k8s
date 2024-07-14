import time
import requests
from confluent_kafka import Producer
import json

producer_conf = {
    'bootstrap.servers': 'kafka:9092',
    'client.id': 'python-producer'
}
producer = Producer(producer_conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def fetch_and_publish():
    while True:
        response = requests.get('https://portal.thatapicompany.com/api/breeds')
        if response.status_code == 200:
            breeds = response.json()[:10]  # Get 10 random breeds
            producer.produce('breeds_topic', key=None, value=json.dumps(breeds), callback=delivery_report)
            producer.flush()
        time.sleep(60)

if __name__ == "__main__":
    fetch_and_publish()
