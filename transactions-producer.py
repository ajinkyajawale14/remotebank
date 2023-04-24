from kafka import KafkaProducer
from faker import Faker
import time
import json

# create Kafka producer
producer = KafkaProducer(bootstrap_servers=['redpanda-0:9092','localhost:19092'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                         api_version=(0, 10, 1)
                        )

# create Faker instance
fake = Faker()

# function to generate a transaction record
def generate_transaction():
    transaction = {
        "user_id": fake.random_int(min=1, max=100),
        "transaction_timestamp_millis": int(time.time() * 1000),
        "amount": round(fake.pyfloat(min_value=-1000, max_value=1000, right_digits=2), 2),
        "currency": fake.currency_code(),
        "counterpart_id": fake.random_int(min=1, max=100)
    }
    return transaction

# send generated records to Kafka topic
for i in range(100):
    transaction = generate_transaction()
    producer.send('transactions', value=transaction)
    print(f'Sent transaction: {transaction}')
    time.sleep(1)

# close producer connection
producer.close()
