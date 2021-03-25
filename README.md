## Table of contents
* [General Info](#general-info)
* [Description](#description)
* [Technologies](#technologies)
* [Setup](#setup)
* [Execution](#execution)

## General Info
This project is Building A Streaming Fraud Detection System With Kafka And Python


## Description
In this project, we will use Kafka to generate a stream of transactions a Python script to process those streams of transactions to detect which ones are potential fraud.



## Technologies
The project is created as follows:
* Docker
* Python3.7+ (Library: Kafka-python)


## Setup

* Creating Custom Docker Image for generator and detector

To use the generator and detector services, we need to use the base image of python:3.6 and add the library Kafka-python


Following is our customized Dockerfile.

```
FROM python:3.6

WORKDIR /usr/app

ADD ./requirements.txt ./

RUN pip install -r requirements.txt

ADD ./ ./

CMD ["python", "app.py"]


```

In production, Kafka is always used as a service i.e. that the cluster runs independently of the applications that use it. The latter simply connects to the cluster to publish or read events from it. To do this locally, we're going to move our zookeeper and broker services to a separate Docker Compose configuration i.e. docker-compose.kafka.yml file. Later on, we'll use the regular docker-compose.yml for our application services only.

* Create an isolated Docker network

```

docker network create Kafka-network

```


``` 
# docker-compose.kafka.yml
version: "3"
services:
    zookeeper:
        image: confluentinc/cp-zookeeper:latest
        environment:
           ZOOKEEPER_CLIENT_PORT: 2181
           ZOOKEEPER_TICK_TIME: 2000
    
    broker:
        image: confluentinc/cp-kafka:latest
        depends_on:
            - zookeeper
        environment:
            KAFKA_BROKER_ID: 1
            KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
            KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://broker:9092
            KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

# NEW
networks:
     default:
       external:
          name: kafka-network

```

docker-compose.yml for the application services: generator and detector

```

version: '3'
services:
    generator:
        build: ./generator
        environment:
           KAFKA_BROKER_URL: broker:9092
           TRANSACTIONS_TOPIC: queueing.transactions
           TRANSACTIONS_PER_SECOND: 1000
    
    detector:
        build: ./detector
        environment:
          KAFKA_BROKER_URL: broker:9092
          TRANSACTIONS_TOPIC: queueing.transactions
          LEGIT_TOPIC: streaming.transactions.legit
          FRAUD_TOPIC: streaming.transactions.fraud

networks:
  default:
    external:
      name: kafka-network

```




## Execution

Navigate to the project folder and execute the following commands

* Spin up Kafka cluster

```
docker-compose -f docker-compose.kafka.yml up

```

![Alt text](/Screenshot/kafkacluster.PNG?raw=true "Kafka Cluster")


* Start Generator and Detector services

```
docker-compose -f docker-compose.yml up

```

![Alt text](/Screenshot/startgenerator_detector.PNG?raw=true "Start Services")


* Consume Legit Transactions

```
docker-compose -f docker-compose.kafka.yml exec broker kafka-console-consumer --bootstrap-server localhost:9092 --topic streaming.transactions.legit

```

![Alt text](/Screenshot/consumelegitTransactions.PNG?raw=true "Legit Transactions")


* Consume Fraud Transactions

```
docker-compose -f docker-compose.kafka.yml exec broker kafka-console-consumer --bootstrap-server localhost:9092 --topic streaming.transactions.fraud

```

![Alt text](/Screenshot/consumefraudtransactions.PNG?raw=true "Fraud Transactions")


