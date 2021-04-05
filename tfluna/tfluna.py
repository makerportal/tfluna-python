######################################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
# Code refactoring (to classes): Clément Nussbaumer, April 2021
######################################################
#
# TF-Luna Mini LiDAR wired to a Raspberry Pi via UART
# --- Configuring the TF-Luna's baudrate, sample rate,
# --- and printing out the device version info 
#
######################################################
#
import serial,time


class TfLuna():

    baud_config = {
        9600: [0x80,0x25,0x00], # 9600
        19200: [0x00,0x4b,0x00], # 19200
        115200: [0x00,0x00,0x00]
    }

    def __init__(self, serial_name = "/dev/serial0", baud_speed = 115200):
        self.ser = serial.Serial(serial_name, baud_speed, timeout = 5) # mini UART serial device
        self.set_samp_rate(100) # set sample rate 1-250
        time.sleep(300e-3) # wait 300ms to settle
        self.get_version() # print version info for TF-Luna


    
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

    def set_samp_rate(self, samp_rate=100):
        ##########################
        # change the sample rate
        samp_rate_packet = [0x5a,0x06,0x03,samp_rate,00,00] # sample rate byte array
        self.ser.write(samp_rate_packet) # send sample rate instruction
        time.sleep(0.1) # wait for change to take effect
        return
            
    def get_version(self):
        ##########################
        # get version info
        info_packet = [0x5a,0x04,0x14,0x00]

        self.ser.write(info_packet)
        time.sleep(0.1)
        bytes_to_read = 30
        t0 = time.time()
        while (time.time()-t0)<5:
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

    def set_baudrate(self, baud_rate=115200):
        ##########################
        # get version info
        baud_hex = {
            9600: [0x80,0x25,0x00], # 9600
            19200: [0x00,0x4b,0x00], # 19200
        }
        # baud_hex = [[0x80,0x25,0x00], # 9600
        #             [0x00,0x4b,0x00], # 19200
        #             [0x00,0x96,0x00], # 38400
        #             [0x00,0xe1,0x00], # 57600
        #             [0x00,0xc2,0x01], # 115200
        #             [0x00,0x84,0x03], # 230400
        #             [0x00,0x08,0x07], # 460800
        #             [0x00,0x10,0x0e]]  # 921600
        # info_packet = [0x5a,0x08,0x06,baud_hex[baud_indx][0],baud_hex[baud_indx][1],
        #             baud_hex[baud_indx][2],0x00,0x00] # instruction packet 

        # prev_ser.write(info_packet) # change the baud rate
        # time.sleep(0.1) # wait to settle
        # prev_ser.close() # close old serial port
        # time.sleep(0.1) # wait to settle
        # ser_new =serial.Serial("/dev/serial0", baudrates[baud_indx],timeout=0) # new serial device
        # if ser_new.isOpen() == False:
        #     ser_new.open() # open serial port if not open
        # bytes_to_read = 8
        # t0 = time.time()
        # while (time.time()-t0)<5:
        #     counter = ser_new.in_waiting
        #     if counter > bytes_to_read:
        #         bytes_data = ser_new.read(bytes_to_read)
        #         ser_new.reset_input_buffer()
        #         if bytes_data[0] == 0x5a:
        #             indx = [ii for ii in range(0,len(baud_hex)) if \
        #                     baud_hex[ii][0]==bytes_data[3] and
        #                     baud_hex[ii][1]==bytes_data[4] and
        #                     baud_hex[ii][2]==bytes_data[5]]
        #             print('Baud Rate = {0:1d}'.format(baudrates[indx[0]]))
        #             time.sleep(0.1) 
        #             return ser_new
        #         else:
        #             ser_new.write(info_packet) # try again if wrong data received
        #             time.sleep(0.1) # wait 100ms
        #             continue


#
############################
# Testing the TF-Luna Output
############################
#

tfluna = TfLuna()

distance,strength,temperature = tfluna.read_tfluna_data() # read values

print(f'Distance: {distance:2.2f} m, Strength: {strength:2.0f} / 65535 (16-bit), Chip Temperature: {temperature:2.1f} C') # print sample data

