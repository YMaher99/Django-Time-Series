from datetime import datetime

from confluent_kafka import Consumer, KafkaError
import csv
import json
import os

from deserializers.kafka_deserializer import KafkaDeserializer


class KafkaConsumer:
    def __init__(self):
        self.topic = None
        consumer_config = {
            'bootstrap.servers': 'kafka:9092',  # Kafka broker address
            'group.id': 'my-group',
            'auto.offset.reset': 'earliest'  # Start consuming from the beginning of the topic
        }
        self.consumer = Consumer(consumer_config)

    def subscribe(self, topic):
        self.topic = topic
        self.consumer.subscribe([topic])

    def generate_csv(self):
        csv_filename = f"./sample_datasets/{self.topic}.csv"
        if os.path.exists(csv_filename):
            os.remove(csv_filename)
        csv_file = open(csv_filename, 'a', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['value', 'timestamp', 'anomaly', 'attribute_id','generator_id'])
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.key() == b'end':
                print("EOF")
                break
            if msg.error():
                print(f"Error: {msg.error()}")
            else:
                # Process the received message and append it to the CSV file
                message_dict = KafkaDeserializer.deserialize(msg)  # Decode the message
                data_list = []
                for key in message_dict.keys():
                    if key == "timestamp":
                        data_list.append(datetime.utcfromtimestamp(message_dict[key]/1000))
                    else:
                        data_list.append(message_dict[key])

                csv_writer.writerow(data_list)  # Append the data to the CSV file
                csv_file.flush()  # Ensure data is written immediately
        self.consumer.close()
        csv_file.close()
