######################################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
# Code refactoring (to classes): Clément Nussbaumer, April 2021
# Reference manual for the sensor: https://github.com/May-DFRobot/DFRobot/blob/master/TF-Luna%20LiDAR%EF%BC%888m%EF%BC%89Product%20Manual.pdf
######################################################
#
# TF-Luna Mini LiDAR wired to a Raspberry Pi via UART
# --- Configuring the TF-Luna's baudrate, sample rate,
# --- and printing out the device version info 
#
######################################################
#
import serial,time
import timeout_decorator
from .util import raise_if_outside_context


class TfLuna():

    baud_config = {
        9600: [0x80,0x25,0x00], # 9600
        19200: [0x00,0x4b,0x00], # 19200
        38400: [0x00,0x96,0x00], # 38400
        57600: [0x00,0xe1,0x00], # 57600
        115200: [0x00,0xc2,0x01], # 115200
        230400: [0x00,0x84,0x03], # 230400
        460800: [0x00,0x08,0x07], # 460800
        921600: [0x00,0x10,0x0e]  # 921600
    }

    def __init__(self, serial_name = "/dev/serial0", baud_speed = 115200):
        if baud_speed not in self.baud_config:
            raise Exception(f"Invalid baud_speed setting used: {baud_speed}\n"
            "available baud speeds: 9600,19200,38400,57600,115200,230400,460800,921600")
        self.serial_name = serial_name
        self.baud_speed = baud_speed
        self.inside_context = False # set to False so long as we haven't used the with statement.

    def __enter__(self):
        self.ser = serial.Serial(self.serial_name, self.baud_speed, timeout = 1) # mini UART serial device
        self.inside_context = True # now that we are in a context, we set this to true and open the serial device 
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.inside_context = False
        self.ser.close()
        print(f"Correctly closed the TfLuna Object and the serial port")


    @raise_if_outside_context
    @timeout_decorator.timeout(5, use_signals=False)
    def read_tfluna_data(self):
        while True:
            counter = self.ser.in_waiting # count the number of bytes of the serial port
            bytes_to_read = 9
            if counter > bytes_to_read-1:
                bytes_serial = self.ser.read(bytes_to_read) # read 9 bytes
                self.ser.reset_input_buffer() # reset buffer

                if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # check first two bytes
                    distance = bytes_serial[2] + bytes_serial[3]*256 # distance in next two bytes
                    strength = bytes_serial[4] + bytes_serial[5]*256 # signal strength in next two bytes
                    temperature = bytes_serial[6] + bytes_serial[7]*256 # temp in next two bytes
                    temperature = (temperature/8) - 256 # temp scaling and offset
                    return distance/100.0,strength,temperature

    @raise_if_outside_context
    def set_samp_rate(self, samp_rate=100):
        ##########################
        # change the sample rate
        samp_rate_packet = [0x5a,0x06,0x03,samp_rate,00,00] # sample rate byte array
        self.ser.write(samp_rate_packet) # send sample rate instruction
        time.sleep(0.1) # wait for change to take effect
        return
            
    @raise_if_outside_context
    @timeout_decorator.timeout(5, use_signals=False)
    def get_version(self):
        ##########################
        # get version info
        info_packet = [0x5a,0x04,0x14,0x00]

        self.ser.write(info_packet)
        time.sleep(0.1)
        bytes_to_read = 30
        while True: # timeout handled by the timeout decorator
            counter = self.ser.in_waiting
            if counter > bytes_to_read:
                bytes_data = self.ser.read(bytes_to_read)
                self.ser.reset_input_buffer()
                if bytes_data[0] == 0x5a:
                    try:
                        version = bytes_data[3:-1].decode('utf-8')
                        print('Version -'+version)
                    except:
                        continue
                    return
                else:
                    self.ser.write(info_packet)
                    time.sleep(0.1)

    @timeout_decorator.timeout(5, use_signals=False)
    @raise_if_outside_context
    def set_baudrate(self, baud_rate=115200):
        if baud_rate not in self.baud_config:
            raise Exception(f"Invalid baud_speed setting used: {baud_rate}\n"
            "available baud speeds: 9600,19200,38400,57600,115200,230400,460800,921600")

        info_packet = [0x5a,0x08,0x06,
            self.baud_config[baud_rate][0],
            self.baud_config[baud_rate][1],
            self.baud_config[baud_rate][2],
            0x00,0x00] # instruction packet 

        self.ser.write(info_packet) # change the baud rate
        time.sleep(0.1) # wait to settle
        self.ser.close()
        self.ser.baudrate = baud_rate
        self.ser.open()
        time.sleep(0.1) # wait to settle
        bytes_to_read = 8
        while True:
            counter = self.ser.in_waiting
            if counter > bytes_to_read:
                bytes_data = self.ser.read(bytes_to_read)
                self.ser.reset_input_buffer()
                if bytes_data[0] == 0x5a:
                    for spd in self.baud_config:
                        match = True
                        match &= self.baud_config[spd][0] == bytes_data[3]
                        match &= self.baud_config[spd][1] == bytes_data[4]
                        match &= self.baud_config[spd][2] == bytes_data[5]
                        if match:
                            print(f"Baud Rate = {spd}")
                            return
                    time.sleep(0.1) 
                else:
                    self.ser.write(info_packet) # try again if wrong data received
                    time.sleep(0.1) # wait 100ms
                    continue
