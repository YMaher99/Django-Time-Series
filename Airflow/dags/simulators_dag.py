from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import sys
import os
import django

sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simulator.settings")
django.setup()

from configurers.django_configuration_manager import DjangoConfigurationManager
from generators.coefficients_generator import CoefficientsGenerator
from producers.csv_data_producer import CSVDataProducer
from producers.nifi_producer import NIFIProducer
from producers.kafka_producer import KafkaProducer
from simulator_operations.parallel_run_simulator import ParallelRunSimulator
from simulator_api.models import Simulator


def run_simulator(pk, **kwargs):

    instance = Simulator.objects.get(pk=pk)
    config_manager = DjangoConfigurationManager(instance)
    generator = CoefficientsGenerator(config_manager)
    if instance.producer_type == instance.CSV:
        producer = CSVDataProducer(config_manager)
    elif instance.producer_type == instance.KAFKA:
        producer = KafkaProducer(config_manager)
    elif instance.producer_type == instance.NIFI:
        producer = NIFIProducer(config_manager)
    else:
        producer = KafkaProducer(config_manager)

    if instance.simulator_runner is None:
        instance.simulator_runner = ParallelRunSimulator(config_manager, generator, producer)
    instance.simulator_runner.run_simulator()

    # path = f"http://web:8000/simulator/{pk}/run_simulator"
    # response = requests.get(url=path)
    ti = kwargs['ti']
    ti.xcom_push(key='status_code', value=200)


def check_simulator_status(**kwargs):
    ti = kwargs['ti']
    status_code = ti.xcom_pull(task_ids='op_1', key='status_code')
    if status_code == 200:
        print("Ran Successfully")


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 11, 12)
}

for simulator in Simulator.objects.all():
    with DAG(dag_id=str(simulator.pk),
             default_args=default_args,
             schedule_interval=f"0 0 */{str(simulator.scheduled_interval_days)} * *") as dag:
        operator_1 = PythonOperator(
            task_id='op_1',
            provide_context=True,
            python_callable=run_simulator,
            op_args=[simulator.pk],
            dag=dag
        )

        operator_2 = PythonOperator(
            task_id='op_2',
            provide_context=True,
            python_callable=check_simulator_status,
            dag=dag
        )

        operator_1 >> operator_2
