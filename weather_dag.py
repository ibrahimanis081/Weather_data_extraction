from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from python_scripts.weather_data import get_data, extract_timestamp, extract_humidity_data
from python_scripts.weather_data import extract_temperature_data, extract_precipitation_data
from python_scripts.weather_data import merge_datas, connect_load_data_and_close_db_connection

default_args = {
    "owner": "airflow",
    "retries": 5,
    "retry_delay": timedelta(minutes = 1)
}

with DAG(
    dag_id = "weather_pipeline",
    default_args = default_args,
    start_date = datetime(2022, 10, 23),
    schedule_interval = "@daily",
    catchup = False   
) as dag:

	data = PythonOperator(
		task_id = "get_data_from_API",
		python_callable = get_data
	)
	
	timestamp = PythonOperator(
		task_id = "extract_timestamp",
		python_callable = extract_timestamp
	)

	humidity = PythonOperator(
		task_id = "extract_humidity_data",
		python_callable = extract_humidity_data
	)
 
	precipitation = PythonOperator(
		task_id = "extract_precipitation_data",
		python_callable = extract_precipitation_data
	)

	temperature = PythonOperator(
		task_id = "get_temperature_data",
		python_callable = extract_temperature_data
	)

	merge_data = PythonOperator(
		task_id = "merge_data",
		python_callable = merge_datas
	)

	load_data_and_close_connection = PythonOperator(
		task_id = "load_data_and_close_connection",
		python_callable = connect_load_data_and_close_db_connection
	)

	data >> [timestamp, humidity, precipitation, temperature] >> merge_data  >> load_data_and_close_connection
