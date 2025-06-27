from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='192.168.10.21:29092',
    group_id='visual-consumer',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for msg in consumer:
    txn = msg.value
    print(f"\n Transaction Received")
    print(f"User: {txn['user']} | Amount: ${txn['amount']} | Time: {txn['timestamp']}")
