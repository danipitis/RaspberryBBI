# handle_upload_data.py
# This is part of Raspberry BBI project - Version 1.0.0
# Copyright (c) Pitis Daniel - Florin <pitis.dan [at] gmail [dot] com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

import shutil
import os

def move_file(uploaded_filename, config_settings):

	img_ext = ['.jpg', '.jpeg', '.JPEG', '.JPG']

	upload_path 		   = os.path.join(config_settings.UPLOADS_PATH, uploaded_filename)
	mp3_destination_path   = config_settings.MUSIC_PATH 
	image_destination_path = config_settings.IMAGES_PATH 

	if uploaded_filename.endswith('.mp3'):
		shutil.copy(upload_path,mp3_destination_path)
	if uploaded_filename.endswith(tuple(img_ext)):
		shutil.copy(upload_path,image_destination_path)

	if os.path.isfile(upload_path):
		os.remove(upload_path)
	else:
		print('Error: %s could not delete file: ' % upload_path)