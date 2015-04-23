# get_system_info.py
# This is part of Raspberry BBI project - Version 1.0.0
# Copyright (c) Pitis Daniel - Florin <pitis.dan [at] gmail [dot] com>
# This script is published under the terms of the MIT license
# http://opensource.org/licenses/MIT

import commands
import os

class sysInfo:
    # This method gets the uptime of the Raspberry Pi
    def get_uptime(self):
        dataFile       = open("/proc/uptime")
        # In contents[0] we store the Raspberry Pi
        # Uptime in unix time format
        contents       = dataFile.read().split()
        dataFile.close()
        unixTime       = float(contents[0])
        minute         = 60
        hour           = minute * 60
        day            = hour * 24
        days           = int(unixTime / day)
        hours          = int((unixTime % day) / hour)
        minutes        = int((unixTime % hour) / minute)
        seconds        = int(unixTime % minute)

        raspberryUptime = ''
        if days > 0:
            raspberryUptime += str(days) + ' ' + (days == 1 and 'Day' or'Days') + ' '
        if len (raspberryUptime) > 0 or hours > 0:
            raspberryUptime     += str(hours) + ' ' + (hours == 1 and 'Hour' or 'Hours') + ' '
        if len (raspberryUptime) > 0 or minutes > 0:
            raspberryUptime     += str(minutes) + ' ' + (minutes == 1 and 'Min' or 'Min') + ' '
        raspberryUptime += str( seconds ) + ' ' + ( seconds == 1 and 'Sec' or 'Sec') + ' '
        return raspberryUptime

    # Return the RAM informations (unit=kb) in a list
    # Index 0: total RAM
    # Index 1: used RAM
    # Index 2: free RAM
    def ram_info(self):
        p = os.popen('free')
        i = 0
        while 1:
            i = i + 1
            line = p.readline()
            if i==2:
                return(line.split()[1:4])
    
    # Returns total RAM avaible on the Raspberry Pi
    def total_ram(self):
        infoRAM = self.ram_info()
        total_ram = round(int(infoRAM[0]) / 1000,1)
        return total_ram
    # Returns used RAM from the Raspberry Pi
    def used_ram(self):
        infoRAM = self.ram_info()
        used_ram = round(int(infoRAM[1]) / 1000,1)
        return used_ram

    # Returns the percent of RAM used on the device
    def percent_ram(self, total, used):
        return((used * 100) / total)

    def get_ram_in_percent(self):
        total_ram_memory   = self.total_ram()
        used_ram_memory    = self.used_ram()
        percent_ram_memory = self.percent_ram(total_ram_memory, used_ram_memory)
        percent_ram_memory = str(int(percent_ram_memory)) # Remove decimals
        return percent_ram_memory

    # Return information about disk space as a list (unit included)                     
    # Index 0: total disk space                                                         
    # Index 1: used disk space                                                         
    # Index 2: remaining disk space                                                     
    # Index 3: percentage of disk used                                                 
    def get_disk_space(self):
        p = os.popen("df -h /")
        i = 0
        while 1:
            i = i + 1
            line = p.readline()
            if i==2:
                return(line.split()[1:5])

    # Return % of CPU used by user as a character string                                
    def get_cpu_use(self):
        cpu_use = os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip('\\')
        cpu_use = cpu_use.rstrip('\n')
        cpu_use = float(cpu_use)
        cpu_use = int(cpu_use)
        return cpu_use
