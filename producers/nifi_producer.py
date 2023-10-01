import pandas as pd
import json
from configurers.configuration_manager import ConfigurationManager
from producers.data_producer import DataProducer
import requests


class NIFIProducer(DataProducer):

    def __init__(self):
        super().__init__()
        self.current_id = 0

    def produce_data(self, time_series_df: pd.DataFrame, config_manager: ConfigurationManager, filename=None):
        # df_json = time_series_df.to_json(orient='records')
        json_output = {}

        time_series_df.dropna(inplace=True)

        # Iterate through the DataFrame and create JSON records
        for idx, row in time_series_df.iterrows():
            record = {
                'value': row['value'],
                'timestamp': str(row['timestamp']),
                'anomaly_mask': row['anomaly']
            }
            json_output[str(idx)] = record
        json_result = json.dumps(json_output)
        json_str = '{"id":' + str(self.current_id) + ',"json":' + json_result + '}'
        self.current_id += 1

        url = 'http://nifi:5000/'
        response = requests.post(url, data=json_str)
        if response.status_code == 200:
            print("DataFrame sent successfully!")
        else:
            print("Failed to send DataFrame. Status code:", response.status_code)

    def generate_metadata_file(self):
        pass
