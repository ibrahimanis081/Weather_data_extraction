
def get_data():
	"""Get Weather data from Stormglass through its
 	global API that provides both historical and forcast data
 	for any given coordinate
	
 	Returns
	-------
	A nested dictionary
  	"""
	
	import requests
	import arrow

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
		'Authorization': 'API key here'
	}
	)

	response = response.json()
	return response


response_data = get_data()


def extract_timestamp():
	"""extract timestamp from the dictionary
	object returned by the API call

	Returns
	-------
	A list.
	"""
	timestamp = []
	for values in response_data['hours']:
		timestamp.append(values['time'])
	return timestamp


def extract_humidity_data():
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
	return humidity


def extract_precipitation_data():
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
	return precipitation


def extract_temperature_data():
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
	return temperature


timestamp = extract_timestamp()
humidity = extract_humidity_data()
temperature = extract_temperature_data()
precipitation = extract_precipitation_data()


def merge_datas():
	"""Merge the timestamp, humidity_data, precipitation_data
	and temperature_data into a pandas dataframe

	Returns
	-------
	A pandas Dataframe
	"""
	import pandas as pd

	dataframe = {'timestamp':timestamp, 'humidity':humidity, 
              'temperature':temperature, 'precipitation':precipitation}
	weather_dataframe = pd.DataFrame(dataframe)
	weather_dataframe.set_index('timestamp', drop = True, append = False, 
                                  inplace = True ) #<- set the timestamp as index
	return weather_dataframe


weather = merge_datas()


def connect_load_data_and_close_db_connection():
	"""load pandas Dataframe into table
 	 and terminate connection"""
   
	from pangres.core import aupsert, upsert #Pangres allows us to upsert data
	from sqlalchemy import create_engine

	engine = create_engine('postgresql+psycopg2://weather_user:weather_pass@localhost/weather_db')
	conn = engine.connect()
	upsert(conn, weather, 'weather_table', if_row_exists = 'update')
	conn.close()

connect_load_data_and_close_db_connection()


def main():
  get_data()
  extract_timestamp()
  extract_humidity_data()
  extract_temperature_data()
  extract_precipitation_data()
  merge_datas()
  connect_load_data_and_close_db_connection()

if __name__ == "__main__":
	main()