# monitor_data.py
# This is part of Raspberry BBI project - Version 1.0.0
# Copyright (c) Pitis Daniel - Florin <pitis.dan [at] gmail [dot] com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

from ..mod_picontrol import get_time_date
import threading
import thread

class monitorData:

	__monitor_thread = None

	def __init__(self, display, config_city, weather):
		self.weather 	 = weather
		self.config_city = config_city
		self.display     = display

	def start_monitoring(self):
		date_time        = get_time_date.getTimeAndDate()
		date_time_string = date_time.get_date() + ' ' + date_time.get_time()
		self.display.print_first_line(date_time_string,self.display.style.center)

		weather_temp   = self.weather.get_temperature()
		weather_desc   = self.weather.get_description()
		weather_string = weather_temp + ' degrees C,' + weather_desc + ' in Sibiu'
		#self.display.print_second_line(weather_string,4)

		thread.start_new_thread(self.display.print_second_line, (weather_string,self.display.style.scroll,))

		self.__monitor_thread = threading.Timer(60, self.start_monitoring,)
		self.__monitor_thread.start()

	# Check if thread is started and cancels it
	def stop_monitoring(self):
		if self.__monitor_thread != None:
			self.__monitor_thread.cancel()