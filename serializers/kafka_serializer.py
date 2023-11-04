import pandas as pd
import json

from configurers.configuration_manager import ConfigurationManager


class KafkaSerializer:

    @staticmethod
    def serialize(series: pd.Series, config_manager: ConfigurationManager) -> str:
        data = series.to_json()
        data = json.loads(data)
        data['attributeId'] = config_manager.datasets[config_manager.current_dataset_num].attribute_id
        data['assetId'] = config_manager.datasets[config_manager.current_dataset_num].generator_id

        data = json.dumps(data)
        return data
