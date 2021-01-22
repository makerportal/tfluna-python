######################################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
######################################################
#
# TF-Luna Mini LiDAR wired to a Raspberry Pi via UART
# --- testing the distance measurement from the TF-Luna
#
#
######################################################
#
import serial,time
import numpy as np
#
##########################
# TFLuna Lidar
##########################
#
ser = serial.Serial("/dev/serial0", 115200,timeout=0) # mini UART serial device
#
############################
# read ToF data from TF-Luna
############################
#
def read_tfluna_data():
    while True:
        counter = ser.in_waiting # count the number of bytes of the serial port
        if counter > 8:
            bytes_serial = ser.read(9) # read 9 bytes
            ser.reset_input_buffer() # reset buffer

            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # check first two bytes
                distance = bytes_serial[2] + bytes_serial[3]*256 # distance in next two bytes
                strength = bytes_serial[4] + bytes_serial[5]*256 # signal strength in next two bytes
                temperature = bytes_serial[6] + bytes_serial[7]*256 # temp in next two bytes
                temperature = (temperature/8.0) - 256.0 # temp scaling and offset
                return distance/100.0,strength,temperature

if ser.isOpen() == False:
    ser.open() # open serial port if not open

distance,strength,temperature = read_tfluna_data() # read values
print('Distance: {0:2.2f} m, Strength: {1:2.0f} / 65535 (16-bit), Chip Temperature: {2:2.1f} C'.\
              format(distance,strength,temperature)) # print sample data
ser.close() # close serial port
