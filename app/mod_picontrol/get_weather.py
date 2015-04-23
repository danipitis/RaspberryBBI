# get_weather.py
# This is part of Raspberry BBI project - Version 1.0.0
# Copyright (c) Pitis Daniel - Florin <pitis.dan [at] gmail [dot] com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

from json import load
from urllib2 import Request, urlopen, URLError

class getWeatherData:

	weather_json = None

	def __init__(self, config_city_name):
		self.config_city_name   = config_city_name 
		self._get_json(self.config_city_name)

	def _kelvin_to_celsius(self, temperature):
		return temperature - 273.15

	def _kelvin_to_fahrenheit(self, temperature): # if you want the temp in Fahrenheit
		return (kelvin_to_celsius(temperature) * 1.800) + 32.00

	def _get_json(self, city):
		req = Request('http://api.openweathermap.org/data/2.5/weather?q={}'.format(self.config_city_name))
		try:
			response = urlopen(req)
		except URLError as e:
			if hasattr(e, 'reason'):
				print 'We failed to reach a server.'
				print 'Reason: ', e.reason
			elif hasattr(e, 'code'):
				print 'The server couldn\'t fulfill the request.'
				print 'Error code: ', e.code
		else: # All good here
			self.weather_json = load(response)

	def get_temperature(self):

		if self.weather_json != None: # If i fetched the json
			json_data = self.weather_json
			if json_data['cod'] == 200: # if everything is ok 
				json_main = json_data['main'] 
				temp = json_main['temp']
				real_temp = self._kelvin_to_celsius(temp)
				return str(round(int(real_temp)))
			else:
				return '9000' # There was an error with the city name
		else:
			return '9001' # Error while getting data

	def get_description(self):
		if self.weather_json != None:
			json_data = self.weather_json
			if json_data['cod'] == 200: # if everything is ok 
				json_main = json_data['main'] 
				weather_description = json_data['weather'][0]['description']
				return str(weather_description)
			else:
				return '9000' # There was an error with the city name
		else:
			return '9001' # Error while getting data


	def get_pressure(self):
		if self.weather_json != None:
			json_data = self.weather_json
			if json_data['cod'] == 200: # if everything is ok 
				json_main = json_data['main'] 
				pressure = json_main['pressure']
				return str(pressure)
			else:
				return '9000' # There was an error with the city name
		else:
			return '9001' # Error while getting data