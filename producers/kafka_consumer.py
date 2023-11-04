from confluent_kafka import Consumer, KafkaError
import csv


class KafkaConsumer:
    def __init__(self):
        consumer_config = {
            'bootstrap.servers': 'kafka:9092',  # Kafka broker address
            'group.id': 'my-group',
            'auto.offset.reset': 'earliest'  # Start consuming from the beginning of the topic
        }
        self.consumer = Consumer(consumer_config)
        # Open a CSV file in append mode

    def subscribe(self, topic):
        print(f'Consumer topic {topic}')
        self.consumer.subscribe([topic])

    def generate_csv(self):
        # csv_filename = 'output.csv'
        # csv_file = open(csv_filename, 'a', newline='')
        # csv_writer = csv.writer(csv_file)
        print('Started Generating')
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
                print(f'consumed {msg.value()}')
                # print(msg.value())
                # message_value = msg.value().decode('utf-8')  # Decode the message
                # data = message_value.split(',')  # Assuming the message is comma-separated

                # csv_writer.writerow(data)  # Append the data to the CSV file
                # csv_file.flush()  # Ensure data is written immediately
        self.consumer.close()
        # csv_file.close()
