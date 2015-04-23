# handle_pictures.py
# This is part of Raspberry BBI project - Version 1.0.0
# Copyright (c) Pitis Daniel - Florin <pitis.dan [at] gmail [dot] com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

import os

class RaspberryHandleImages:

	image_list = []

	def __init__(self, config_settings):
		self.config_settings = config_settings
		self.get_pictures_list()

	def get_pictures_list(self):
		img_ext = [".jpg", ".jpeg", ".JPEG", "JPG"]
		for file in os.listdir(self.config_settings):
			if file.endswith(tuple(img_ext)):
				self.image_list.append(file)

	def delete_picture(self, file_name):
		picture_to_delete = os.path.join(self.config_settings, file_name)
		if os.path.isfile(picture_to_delete):
			os.remove(picture_to_delete)
			self.image_list[:] = []
			self.get_pictures_list()
		else:
			print("Error: %s file not found" % file_name)

	def update_picture(self, file_name):
		self.image_list.append(file_name)