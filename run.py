# run.py
# This is part of Raspberry BBI project - Version 1.0.0
# Copyright (c) Pitis Daniel - Florin <pitis.dan [at] gmail [dot] com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

from flask import Flask, render_template, redirect, request, send_from_directory
from werkzeug import secure_filename
from app.mod_picontrol import get_system_temperature
from app.mod_picontrol import get_system_info
from app.mod_picontrol import get_weather
from app.mod_picontrol import control_lcd
from app.mod_picontrol import control_music
from app.mod_picontrol import handle_pictures
from app.mod_picontrol import get_time_date
from app.mod_picontrol import handle_upload_data
from app.mod_monitor import monitor_data
import thread
import config
import os
import re
import urllib2

app = Flask(__name__,static_folder = config.APP_STATIC_FOLDER,template_folder=config.APP_TEMPLATE_FOLDER)

app.config['UPLOAD_FOLDER'] = config.UPLOADS_PATH

# Set the allowed extensions from the config file
app.config['ALLOWED_EXTENSIONS'] = set(config.ALLOWED_EXTENSIONS)

lcd     		 = control_lcd.lcdDisplay()
music            = control_music.raspberryMusic(config.MUSIC_PATH)
pictures_data    = handle_pictures.RaspberryHandleImages(config.IMAGES_PATH)

weather 		 = get_weather.getWeatherData(config.CURRENT_CITY)
monitor_lcd_data = monitor_data.monitorData(lcd,config.CURRENT_CITY, weather)

# Check if the file extension is in the allowed list
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Convert the extension to lowercase
def convert_file_extension_to_lowercase(name):
	base, ext = os.path.splitext(name)
	return base + ext.lower()

# Upload the file using POST
@app.route('/upload', methods=['POST'])
def upload():
	global music
	global pictures_data

	# Get the uploaded file name
	file = request.files['file']

	filename = convert_file_extension_to_lowercase(file.filename)

	if file and allowed_file(filename):
				
		# Make the filename safe, remove unsupported chars
		filename = secure_filename(filename)

		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		handle_upload_data.move_file(filename,config)

		if filename.endswith('.mp3'):
			music.update_music(filename)
			return redirect("/", code=302)
		if filename.endswith(tuple(config.IMAGES_EXTENSIONS)):
			pictures_data.update_picture(filename)
			return redirect("/", code=302)
		else: # If upload button is clicked but no file is selected
			return redirect("/", code=302)
	else: 
		return redirect("/", code=302)

@app.route("/")
def index():
	global weather
	now         = get_time_date.getTimeAndDate()
	time_string = now.get_date() + ' ' + now.get_time()

	temperature          = get_system_temperature.raspberryTemp()
	show_cpu_temperature = temperature.cpu_temp()
	show_gpu_temperature = temperature.gpu_temp()

	sys_info           = get_system_info.sysInfo()
	uptime             = sys_info.get_uptime()
	percent_ram_memory = sys_info.get_ram_in_percent()
	
	percent_disk_space    = sys_info.get_disk_space()
	percent_disk_space[3] = percent_disk_space[3].replace('%','')
	percent_cpu_use       = sys_info.get_cpu_use()

	weather_data = weather.get_temperature()
	weather_desc = weather.get_description()

	templateData = {
		'time': time_string,
		'cpu_temperature': show_cpu_temperature,
		'gpu_temperature': show_gpu_temperature,
		'system_uptime': uptime,
		'ram_percent': percent_ram_memory,
		'disk_percent': percent_disk_space[3],
		'weather_temperature': weather_data,
		'weather_description': weather_desc,
		'total_used_cpu': percent_cpu_use
		}
	return render_template('index.html', **templateData)

@app.route("/pictures/")
def raspberry_pictures():
	global pictures_data

	images_list = {
	'images_data': pictures_data.image_list
	 }

	return render_template('picontrol/pictures.html', **images_list)

# Handle the remove picture link
@app.route("/<picture_name>/<action>")
def remove_picture(picture_name, action):
	global pictures_data
	if action == 'remove':
		pictures_data.delete_picture(picture_name)
		return redirect("/pictures/", code=302)
	else:
		return redirect("/", code=302)

@app.route("/weather/")
def raspberry_weather():
	return render_template('picontrol/weather.html')

def is_matching_title(title):
	for expression in config.FILELIST_EXPRESSIONS:
		if re.match(expression, title):
			return title

def get_matching_titles(titles):
	for title in titles:
		if is_matching_title(title):
			yield title

def get_file_path(title):
	return os.path.join(config.UPLOADS_PATH, title + ".torrent")

def download_file(url, title):
	filedownload = urllib2.urlopen(url)
	file_path = get_file_path(title);
	if not os.path.isfile(file_path):
		output = open(file_path,'wb')
		output.write(filedownload.read())
		output.close()

def get_torrents():
	for file in os.listdir(config.UPLOADS_PATH):
		if file.endswith(".torrent"):
			yield file

@app.route("/movies/")
def raspberry_movies():
	import feedparser
	import glob

	filelist_url = "http://filelist.ro/rss.php?feed=dl&cat=21,23&passkey=secretpasskey"

	feed = feedparser.parse(filelist_url)

	titles = map(lambda item: item["title"], feed["items"])
	matching_titles = get_matching_titles(titles)

	items = feed["items"]
	for item in items:
		title = item["title"]
		link = item["link"]

		if is_matching_title(title):
			download_file(link, title)

	movies_data = {
		'all_movies': titles,
		'matching_movies': matching_titles,
		'downloaded_torrents': get_torrents()
	}
	return render_template('picontrol/movies.html', **movies_data)

@app.route("/music/")
def play_the_music():
	
	music_data = {
		'music_list': music.dict_music
	}
	return render_template('picontrol/music.html', **music_data)

# Handle the line change from the LCD
@app.route("/change_first_line", methods=['POST'])  
def change():  
	global lcd
	# Get the value from the submitted form 
	print_text = request.form['lcd']

	if request.form['btnPrintFirstLine'] == 'printCenter':
		lcd.print_first_line(print_text,lcd.style.center)  
	elif request.form['btnPrintFirstLine'] == 'printLeft':
		lcd.print_first_line(print_text,lcd.style.left)  
	elif request.form['btnPrintFirstLine'] == 'printRight':
		lcd.print_first_line(print_text,lcd.style.right)  
	elif request.form['btnPrintFirstLine'] == 'printScroll': 
		thread.start_new_thread(lcd.print_first_line, (print_text,lcd.style.scroll,))

	return redirect("/", code=302)  

# Handle the second line change from the LCD
@app.route("/change_second_line", methods=['POST'])
def change_sec_line():
	global lcd
	print_text = request.form['second_lcd']
	
	if request.form['btnPrintSecondLine'] == 'printCenter':
		lcd.print_second_line(print_text,lcd.style.center)  
	elif request.form['btnPrintSecondLine'] == 'printLeft':
		lcd.print_second_line(print_text,lcd.style.left)  
	elif request.form['btnPrintSecondLine'] == 'printRight':
		lcd.print_second_line(print_text,lcd.style.right)  
	elif request.form['btnPrintSecondLine'] == 'printScroll':
		thread.start_new_thread(lcd.print_second_line, (print_text,lcd.style.scroll,)) 

	return redirect("/", code=302)

@app.route("/start_lcd_monitoring", methods=['POST'])
def start_monitorng():
	global monitor_lcd_data
	monitor_lcd_data.start_monitoring()

	return redirect("/", code=302)

@app.route("/stop_lcd_monitoring", methods=['POST'])
def stop_monitorng(): 
	global monitor_lcd_data
	monitor_lcd_data.stop_monitoring()

	return redirect("/", code=302)

@app.route("/play_song/<song_name>/<song_action>")
def play_stop_song(song_name, song_action):
	global music

	if song_action == 'play' or song_action == 'stop':
		music.update_music_state(song_name,song_action)
		return redirect("/music/", code=302)
	else:
		return redirect("/", code=302)

if __name__ == "__main__":
	app.run(host=config.HOST_ADRESS, port=config.PORT, debug=config.DEBUG)
