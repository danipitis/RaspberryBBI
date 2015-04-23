# control_music.py
# This is part of Raspberry BBI project - Version 1.0.0
# Copyright (c) Pitis Daniel - Florin <pitis.dan [at] gmail [dot] com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

from mutagen.mp3 import MP3
from werkzeug import secure_filename
import thread
import pygame
import os

class raspberryMusic:

	dict_music = {}

	def __init__(self, config_settings):
		self.config_settings = config_settings
		self.get_music()

	# Returns the combined path of the music directory from settings + the filename
	def return_path(self, file_name):
		return os.path.join(self.config_settings, file_name)

	# We reset every song state to stop execept the song who started
	def reset_to_stop(self, file_name):
		for music_file in self.dict_music:
			if music_file != file_name:
				self.dict_music[music_file][1] = "stop"

	# This is called when another music file is uploaded to the server
	def update_music(self,filename):

		mp3_full_path = self.return_path(filename)
		
		secure_name = secure_filename(filename)
		secure_name = secure_name.replace('_', ' ')
		secure_name_full_path = self.return_path(secure_name)

		os.rename(mp3_full_path, secure_name_full_path)
		audio = MP3(secure_name_full_path)
		seconds = audio.info.length
		secure_name = secure_name.decode('utf-8')
		self.dict_music[secure_name] = [self.seconds_to_min_sec(seconds), 'stop']

	# Toggles play/stop on current melody
	def update_music_state(self, selected_song_name, state):
		if state == "play":
			self.dict_music[selected_song_name][1] = "play"
			thread.start_new_thread(self.play_song, (selected_song_name,))
		else: # stop
			self.dict_music[selected_song_name][1] = "stop"
			self.stop_song()

	# Create the music dictionary containing:
	# dict_music[songname]    - The song name
	# dict_music[songname][0] - Song duration
	# dict_music[songname][1] - Song state play/stop
	def get_music(self):

		for music_file in os.listdir(self.config_settings):
			if music_file.endswith(".mp3"):
				self.update_music(music_file)

	def play_song(self, filename):
		pygame.mixer.init()

		# If play is hit when another song is playing
		if pygame.mixer.music.get_busy():
			pygame.mixer.music.stop()
			self.reset_to_stop(filename)

		pygame.mixer.music.load(self.return_path(filename))
		pygame.mixer.music.play()

		while pygame.mixer.music.get_busy() == True:
			continue

		# Set state to stop when the song finishes
		self.dict_music[filename][1] = "stop"

	def stop_song(self):
		pygame.mixer.music.stop()

	# Return a minutes:seconds string representation of the given number of seconds.
	def seconds_to_min_sec(self,secs):
		mins = int(secs) / 60
		secs = int(secs - (mins * 60))
		return "%d:%02d" % (mins, secs)