# detector/app.py
import os
import json
from kafka import KafkaConsumer, KafkaProducer

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")

# Extract the queueing.transactions topic from TRANSACTIONS_TOPIC environment variable
TRANSACTIONS_TOPIC = os.environ.get("TRANSACTIONS_TOPIC")

# Extract the streaming.transactions.legit topic from LEGIT_TOPIC environment variable
LEGIT_TOPIC = os.environ.get("LEGIT_TOPIC")

# Extract the streaming.transactions.fraud topic from FRAUD_TOPIC environment variable
FRAUD_TOPIC = os.environ.get("FRAUD_TOPIC")


def is_suspicious(transaction: dict):
    """Determine whether a transaction is suspicious."""
    return transaction["amount"] >= 900



if __name__ == "__main__":
   
    consumer = KafkaConsumer(
              TRANSACTIONS_TOPIC,
              bootstrap_servers=KAFKA_BROKER_URL,
              value_deserializer=lambda value: json.loads(value),
    )
    
    producer = KafkaProducer(
               bootstrap_servers=KAFKA_BROKER_URL,
               value_serializer=lambda value: json.dumps(value).encode(),
    )
    
    for message in consumer:
        transaction: dict = message.value
        # output transaction in the correct topic (legit or fraud)
        topic = FRAUD_TOPIC if is_suspicious(transaction) else LEGIT_TOPIC
        producer.send(topic, value=transaction)
        print(topic, transaction) # DEBUG
