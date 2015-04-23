# control_lcd.py
# This is part of Raspberry BBI project - Version 1.0.0
# Copyright (c) Pitis Daniel - Florin <pitis.dan [at] gmail [dot] com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

import RPi.GPIO as GPIO
import time

class LCDstyle:
	left, center, right, scroll = range(4)

class lcdDisplay:

	# Define GPIO to LCD mapping
	LCD_RS = 25
	LCD_E  = 24
	LCD_D4 = 23
	LCD_D5 = 17
	LCD_D6 = 18
	LCD_D7 = 22

	# Define some device constants
	LCD_WIDTH = 16    # Maximum characters per line
	LCD_CHR = True
	LCD_CMD = False

	LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
	LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

	# Timing constants
	E_PULSE = 0.00005
	E_DELAY = 0.00005

	style = LCDstyle

	def __init__(self):

		# Main program block
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)            # Use BCM GPIO numbers
		GPIO.setup(self.LCD_E, GPIO.OUT)  # E
		GPIO.setup(self.LCD_RS, GPIO.OUT) # RS
		GPIO.setup(self.LCD_D4, GPIO.OUT) # DB4
		GPIO.setup(self.LCD_D5, GPIO.OUT) # DB5
		GPIO.setup(self.LCD_D6, GPIO.OUT) # DB6
		GPIO.setup(self.LCD_D7, GPIO.OUT) # DB7

		# Initialise display
		self.lcd_byte(0x33,self.LCD_CMD)
		self.lcd_byte(0x32,self.LCD_CMD)
		self.lcd_byte(0x28,self.LCD_CMD)
		self.lcd_byte(0x0C,self.LCD_CMD)
		self.lcd_byte(0x06,self.LCD_CMD)
		self.lcd_byte(0x01,self.LCD_CMD)


	def _scroll_effect(self, message, lcd_line):
		str_pad = " " * 16
		my_long_string = str(message)
		my_long_string = str_pad + my_long_string
		for i in range (0, len(my_long_string)):
			self.lcd_byte(lcd_line, self.LCD_CMD)
			lcd_text = my_long_string[i:(i+15)]
			self.lcd_string(lcd_text,0)
			time.sleep(0.4)
		self.lcd_byte(lcd_line, self.LCD_CMD)
		self.lcd_string(str_pad,0)

	def _left_right_center_effect(self, message, lcd_line, style):
		self.lcd_byte(lcd_line, self.LCD_CMD)
		self.lcd_string(message,style)

	def print_first_line(self, message, style):
		# print style
		if style == 0 or style == 1 or style == 2:
			self._left_right_center_effect(message, self.LCD_LINE_1, style)
		elif style == 3:
			self._scroll_effect(message, self.LCD_LINE_1)
		else:
			print("No such format style")


	def print_second_line(self, message, style):

		if style == 0 or style == 1 or style == 2:
			self._left_right_center_effect(message, self.LCD_LINE_2, style)
		elif style == 3:
			self._scroll_effect(message, self.LCD_LINE_2)
		else:
			print("No such format style")

	def lcd_string(self, message,style):
		# Send string to display
		# style = 0 Left justified
		# style = 1 Centred
		# style = 3 Right justified

		if style == 0:
			message = message.ljust(self.LCD_WIDTH," ")
		elif style == 1:
			message = message.center(self.LCD_WIDTH," ")
		elif style == 2:
			message = message.rjust(self.LCD_WIDTH," ")

		for i in range(self.LCD_WIDTH):
			self.lcd_byte(ord(message[i]),self.LCD_CHR)

	def lcd_byte(self, bits, mode):
		# Send byte to data pins
		# bits = data
		# mode = True  for character
		#        False for command

		GPIO.output(self.LCD_RS, mode) # RS

		# High bits
		GPIO.output(self.LCD_D4, False)
		GPIO.output(self.LCD_D5, False)
		GPIO.output(self.LCD_D6, False)
		GPIO.output(self.LCD_D7, False)
		if bits&0x10==0x10:
			GPIO.output(self.LCD_D4, True)
		if bits&0x20==0x20:
			GPIO.output(self.LCD_D5, True)
		if bits&0x40==0x40:
			GPIO.output(self.LCD_D6, True)
		if bits&0x80==0x80:
			GPIO.output(self.LCD_D7, True)

		# Toggle 'Enable' pin
		time.sleep(self.E_DELAY)
		GPIO.output(self.LCD_E, True)
		time.sleep(self.E_PULSE)
		GPIO.output(self.LCD_E, False)
		time.sleep(self.E_DELAY)

		# Low bits
		GPIO.output(self.LCD_D4, False)
		GPIO.output(self.LCD_D5, False)
		GPIO.output(self.LCD_D6, False)
		GPIO.output(self.LCD_D7, False)
		if bits&0x01==0x01:
			GPIO.output(self.LCD_D4, True)
		if bits&0x02==0x02:
			GPIO.output(self.LCD_D5, True)
		if bits&0x04==0x04:
			GPIO.output(self.LCD_D6, True)
		if bits&0x08==0x08:
			GPIO.output(self.LCD_D7, True)

		# Toggle 'Enable' pin
		time.sleep(self.E_DELAY)
		GPIO.output(self.LCD_E, True)
		time.sleep(self.E_PULSE)
		GPIO.output(self.LCD_E, False)
		time.sleep(self.E_DELAY)