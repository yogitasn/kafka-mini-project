import os
import json
from time import sleep
from kafka import KafkaProducer
from transactions import create_random_transaction

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")

# Extract the queueing.transactions topic from TRANSACTIONS_TOPIC environment variable
TRANSACTIONS_TOPIC = os.environ.get("TRANSACTIONS_TOPIC")

# Make the sleep time configurable through a TRANSACTIONS_PER_SECOND environment variable.
TRANSACTIONS_PER_SECOND = float(os.environ.get("TRANSACTIONS_PER_SECOND"))
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND


if __name__ == "__main__":

    producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER_URL,
            # Encode all values as JSON
            # Make use of KafkaProducer's value_serializer argument to automatically serialize messages from a dict to JSON bytes.
            value_serializer=lambda value: json.dumps(value).encode(),
    )
    while True:

        transaction: dict = create_random_transaction()
        producer.send(TRANSACTIONS_TOPIC, value=transaction)
        #print(transaction) # DEBUG
        sleep(SLEEP_TIME)
