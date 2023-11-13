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

from simulator_api.models import Simulator


def run_simulator(pk, **kwargs):

    path = f"http://web:8000/simulator/{pk}/run_simulator"
    response = requests.get(url=path)
    ti = kwargs['ti']
    ti.xcom_push(key='status_code', value=response.status_code)


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
