# get_system_temperature.py
# This is part of Raspberry BBI project - Version 1.0.0
# Copyright (c) Pitis Daniel - Florin <pitis.dan [at] gmail [dot] com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

import commands
import os

class raspberryTemp:

    def remove_decimals(self, number):
        return int(round(number,))

    def cpu_temp(self):
        tempFile = open("/sys/class/thermal/thermal_zone0/temp")
        cpu_temp = tempFile.read()
        tempFile.close()
        return self.remove_decimals(float(cpu_temp)/1000)
        # return int(round(float(cpu_temp)/1000,))
        # Uncomment the next line if you want the temp in Fahrenheit
        # return (1.8*cpu_temp)+32

    def gpu_temp(self):
        gpu_temp = commands.getoutput('/opt/vc/bin/vcgencmd measure_temp').replace('temp=', '').replace('\'C', '')
        return  self.remove_decimals(float(gpu_temp))
        # Uncomment the next line if you want the temp in Fahrenheit
        # return (1.8*gpu_temp)+32