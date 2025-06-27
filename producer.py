from kafka import KafkaProducer
import json
import random
import time
from faker import Faker

fake = Faker()
producer = KafkaProducer(
    bootstrap_servers='192.168.10.21:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'transactions'

def generate_transaction():
    return {
        "id": fake.uuid4(),
        "user": fake.name(),
        "amount": round(random.uniform(5.0, 1000.0), 2),
        "timestamp": fake.iso8601()
    }

while True:
    txn = generate_transaction()
    print(f"Produced: {txn}")
    producer.send(topic, txn)
    time.sleep(1)
