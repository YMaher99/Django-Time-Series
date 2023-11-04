import pandas as pd
import json
from configurers.configuration_manager import ConfigurationManager
from producers.data_producer import DataProducer
import requests
import psycopg2


class NIFIProducer(DataProducer):

    def produce_data(self, time_series_df: pd.DataFrame):
        # df_json = time_series_df.to_json(orient='records')

        dbname = "postgres"
        user = "postgres"
        password = "postgres"
        host = "db"
        port = "5432"

        # Establish a connection to the database
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

        cur = conn.cursor()
        query = "SELECT MAX(id) FROM public.time_series_json;"
        cur.execute(query)
        max_value = cur.fetchone()[0]

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
        json_str = '{"id":' + str(max_value + 1) + ',"json":' + json_result + '}'

        url = 'http://nifi:5000/'
        response = requests.post(url, data=json_str)
        if response.status_code == 200:
            print("DataFrame sent successfully!")
        else:
            print("Failed to send DataFrame. Status code:", response.status_code)

    def add_metadata(self):
        pass

    def generate_metadata_file(self):
        pass
