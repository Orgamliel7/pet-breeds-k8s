import time
import requests
from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers='kafka:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))


def fetch_and_publish():
    while True:
        response = requests.get('https://portal.thatapicompany.com/api/breeds')
        if response.status_code == 200:
            breeds = response.json()[:10]  # Get 10 random breeds
            producer.send('breeds_topic', breeds)
            producer.flush()
        time.sleep(60)


if __name__ == "__main__":
    fetch_and_publish()
