
import requests
import arrow
import pandas as pd
from pangres.core import aupsert, upsert
from sqlalchemy import create_engine


def get_data():
	"""Get Weather data from Stormglass through its
 	global API that provides both historical and forcast data
 	for any given coordinate
	
 	Returns
	-------
	A nested dictionary
  	"""
	# Get first hour of today
	start = arrow.now().floor('day')

	# Get the last hour of 7 days from now
	end = arrow.now().ceil('day').shift(days = 7)

	response = requests.get(
	'https://api.stormglass.io/v2/weather/point',
	params={
		'lat': 9.0765,
		'lng': 7.3986,
		'params': ','.join(['precipitation', 'humidity', 'airTemperature']),
		'start': start.to('UTC+1').timestamp(),  # Convert to UTC+1 timestamp
		'end': end.to('UTC+1').timestamp(),  # Convert to UTC+1 timestamp
		'source': 'noaa'
	},
	headers={
		'Authorization': 'ee9dd582-4956-11ed-bc36-0242ac130002-ee9dd5e6-4956-11ed-bc36-0242ac130002'
	}
	)

	response = response.json()
	return response


def extract_timestamp(response_data):
	"""extract timestamp from the dictionary
	object returned by the API call

	Returns
	-------
	A list.
	"""
	timestamp = []
	for values in response_data['hours']:
		timestamp.append(values['time'])
	print("time done")
	return timestamp


def extract_humidity_data(response_data):
	"""extract humidity data from the dictionary
	object returned by the API call.

	Returns
	-------
	A list.
	"""
	humidity_data = []
	extracted_humidity = []
	for values in response_data['hours']:
		humidity_data.append(values['humidity']) #<- A list a with Nested dictionary
	for nested_dictionary in humidity_data:
		for dictionary in nested_dictionary.items():
			extracted_humidity.append(list(dictionary)) #<- A list of list, convert to regular list
	flat_list = [item for sublist in extracted_humidity 
              for item in sublist]
	humidity = flat_list[1::2]
	print("hum done")
	return humidity


def extract_precipitation_data(response_data):
	"""extract precipitation data from the dictionary
	object returned by the api call.

	Returns
	-------
	A list.
	"""
	precipitation_data = []
	extracted_precipitation = []
	for values in response_data['hours']:
		precipitation_data.append(values['precipitation']) #<- A list with a Nested dictionary
	for nested_dictionary in precipitation_data:
		for dictionary in nested_dictionary.items():
			extracted_precipitation.append(list(dictionary)) #<- A list of list, convert to regular list
	flat_list = [item for sublist in extracted_precipitation 
              for item in sublist]
	precipitation = flat_list[1::2]
	print("prep done")
	return precipitation


def extract_temperature_data(response_data):
	"""extract temperature data from the dictionary
	object returned by the api call.

	Returns
	-------
	A list.
	"""
	temperature_data = []
	extracted_temperature = []
	for values in response_data['hours']:
		temperature_data.append(values['airTemperature']) #<- A list with a Nested dictionary
	for nested_dictionary in temperature_data:
		for dictionary in nested_dictionary.items():
			extracted_temperature.append(list(dictionary)) #<- A list of list, convert to regular list
	flat_list = [item for sublist in extracted_temperature 
              for item in sublist]
	temperature = flat_list[1::2]
	print("temp done")
	return temperature
	

def merge_datas(timestamp, humidity, temperature, precipitation):
	"""Merge the timestamp, humidity_data, precipitation_data
	and temperature_data into a pandas dataframe

	Returns
	-------
	A pandas Dataframe
	"""
	dataframe = {'timestamp':timestamp, 'humidity':humidity, 
              'temperature':temperature, 'precipitation':precipitation}
	weather_dataframe = pd.DataFrame(dataframe)
	weather_dataframe.set_index('timestamp', drop = True, append = False, 
                                  inplace = True ) #<- set the timestamp as index
	print("merge done")
	return weather_dataframe


def connect_load_data_and_close_db_connection(weather_dataframe):
	"""load pandas Dataframe into table
 	 and terminate connection"""
   
	engine = create_engine('postgresql+psycopg2://weather_user:weather_pass@localhost/weather_db')
	conn = engine.connect()
	upsert(conn, weather_dataframe, 'weather_table', if_row_exists = 'update')
	conn.close()
	print("Data inserted sucessfully")


def main():
    response_data = get_data()
    timestamp = extract_timestamp(response_data)
    humidity = extract_humidity_data(response_data)
    temperature = extract_temperature_data(response_data)
    precipitation = extract_precipitation_data(response_data)
    weather_dataframe = merge_datas(timestamp, humidity, temperature, precipitation)
    connect_load_data_and_close_db_connection(weather_dataframe)


if __name__ == "__main__":
	main()