from kafka import KafkaProducer
import json

from config import KAFKA_HOST, KAFKA_PORT


producer = KafkaProducer(bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}')


def send_message(topic, msg):
    producer.send(topic, json.dumps(msg).encode('utf-8'))