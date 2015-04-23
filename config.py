# config.py
# This is part of Raspberry BBI project - Version 1.0.0
# Copyright (c) Pitis Daniel - Florin <pitis.dan [at] gmail [dot] com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

import os
import sys

HOST_ADRESS = '192.168.0.102'
PORT		=  88
DEBUG 		= 'True' 

APP_STATIC_FOLDER   = 'app/static'
APP_TEMPLATE_FOLDER = 'app/templates'

CURRENT_CITY = 'Sibiu'
GET_WEATHER  = 'False'

pathname     = os.path.dirname(sys.argv[0])
MUSIC_PATH   = os.path.abspath(pathname) + '/app/static/Entertainment/Music/'
IMAGES_PATH  = os.path.abspath(pathname) + '/app/static/Entertainment/Images/'

UPLOADS_PATH = os.path.abspath(pathname) + '/app/uploads/'

# Extensions of the files that are allowed to be uploaded on the server
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'mp3']
IMAGES_EXTENSIONS  = ['.jpg', '.jpeg', '.png']
FILELIST_EXPRESSIONS = ['.*Simpsons.*S(?P<season>\d\d+)E(?P<episode>\d\d+).*720p.*', '.*Revenge\.S04.*']