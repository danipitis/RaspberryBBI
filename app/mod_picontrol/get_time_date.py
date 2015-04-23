# get_time_date.py
# This is part of Raspberry BBI project - Version 1.0.0
# Copyright (c) Pitis Daniel - Florin <pitis.dan [at] gmail [dot] com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

from time import strftime
from datetime import datetime

class getTimeAndDate():

	# In date_string i store the date in format Day-Month-Year (ex 08-Sep-14)
	def get_date(self):
		date_string = datetime.now().strftime('%d-%b-%y')
		return date_string

	# In time_string string i store the time in format Hours:Minutes
	def get_time(self):
		time_string = datetime.now().strftime('%H:%M')
		return time_string