from kafka import KafkaConsumer
import json
import psycopg2

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='192.168.10.21:29092',
    group_id='db-consumer',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

conn = psycopg2.connect(
    dbname="postgres", user="airflow", password="airflow", host="192.168.10.21", port="2990"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id TEXT PRIMARY KEY,
        username TEXT,
        amount FLOAT,
        timestamp TEXT
    );
""")
conn.commit()

for msg in consumer:
    data = msg.value
    print(f"Storing: {data}")
    try:
        cur.execute("INSERT INTO transactions VALUES (%s, %s, %s, %s)", (
            data["id"], data["user"], data["amount"], data["timestamp"]
        ))
        conn.commit()
    except Exception as e:
        print(f"DB Error: {e}")
