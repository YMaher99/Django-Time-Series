from configurers.configuration_manager import ConfigurationManager
from producers.data_producer import DataProducer
from confluent_kafka import Producer
from producers.kafka_consumer import KafkaConsumer


class KafkaProducer(DataProducer):
    def produce_data(self, time_series_df, config_manager: ConfigurationManager, filename=None):
        topic = str(config_manager.current_dataset_num)
        print(f"Producer Topic {topic}")
        producer = Producer({'bootstrap.servers': 'kafka:9092/'})  # Replace with your Kafka broker(s) address

        for index, row in time_series_df.iterrows():
            data = row.to_json()
            print(data)

            # Produce the data to the specified Kafka topic
            producer.produce(topic, key=filename, value=data)
        producer.produce(topic, key='end')
        # Wait for any outstanding messages to be delivered and delivery reports to be received.
        producer.flush()
        return True

    def generate_metadata_file(self):
        pass