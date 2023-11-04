import json


class KafkaDeserializer:

    @staticmethod
    def deserialize(msg) -> dict:
        data_dict = json.loads(msg.value().decode('utf-8'))
        return data_dict