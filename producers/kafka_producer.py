import json

from configurers.configuration_manager import ConfigurationManager
from producers.data_producer import DataProducer
from confluent_kafka import Producer
from serializers.kafka_serializer import KafkaSerializer


class KafkaProducer(DataProducer):
    def produce_data(self, time_series_df, config_manager: ConfigurationManager, filename=None):
        topic = str(config_manager.current_dataset_num)
        producer = Producer({'bootstrap.servers': 'kafka:9092/'})  # Replace with your Kafka broker(s) address

        for index, row in time_series_df.iterrows():
            data = KafkaSerializer.serialize(row, config_manager)
            # Produce the data to the specified Kafka topic
            producer.produce(topic, key=topic, value=data)
        producer.produce(topic, key='end')
        # Wait for any outstanding messages to be delivered and delivery reports to be received.
        producer.flush()
        return True

    def generate_metadata_file(self):
        pass