######################################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
######################################################
#
# TF-Luna Mini LiDAR wired to a Raspberry Pi via UART
# --- Real-time ranging with signal strength indicator
#
#
######################################################
#
import serial,time
import numpy as np
import matplotlib.pyplot as plt
#
############################
# Serial Functions
############################
#
def read_tfluna_data():
    while True:
        counter = ser.in_waiting # count the number of bytes waiting to be read
        bytes_to_read = 9
        if counter > bytes_to_read-1:
            bytes_serial = ser.read(bytes_to_read) # read 9 bytes
            ser.reset_input_buffer() # reset buffer

            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: # check first two bytes
                distance = bytes_serial[2] + bytes_serial[3]*256 # distance in next two bytes
                strength = bytes_serial[4] + bytes_serial[5]*256 # signal strength in next two bytes
                temperature = bytes_serial[6] + bytes_serial[7]*256 # temp in next two bytes
                temperature = (temperature/8) - 256 # temp scaling and offset
                return distance/100.0,strength,temperature

def set_samp_rate(samp_rate=100):
    ##########################
    # change the sample rate
    samp_rate_packet = [0x5a,0x06,0x03,samp_rate,00,00] # sample rate byte array
    ser.write(samp_rate_packet) # send sample rate instruction
    return
            
def get_version():
    ##########################
    # get version info
    info_packet = [0x5a,0x04,0x14,0x00]

    ser.write(info_packet) # write packet
    time.sleep(0.1) # wait to read
    bytes_to_read = 30 # prescribed in the product manual
    t0 = time.time()
    while (time.time()-t0)<5:
        counter = ser.in_waiting
        if counter > bytes_to_read:
            bytes_data = ser.read(bytes_to_read)
            ser.reset_input_buffer()
            if bytes_data[0] == 0x5a:
                version = bytes_data[3:-1].decode('utf-8')
                print('Version -'+version) # print version details
                return
            else:
                ser.write(info_packet) # if fails, re-write packet
                time.sleep(0.1) # wait

def set_baudrate(baud_indx=4):
    ##########################
    # get version info
    baud_hex = [[0x80,0x25,0x00], # 9600
                [0x00,0x4b,0x00], # 19200
                [0x00,0x96,0x00], # 38400
                [0x00,0xe1,0x00], # 57600
                [0x00,0xc2,0x01], # 115200
                [0x00,0x84,0x03], # 230400
                [0x00,0x08,0x07], # 460800
                [0x00,0x10,0x0e]]  # 921600
    info_packet = [0x5a,0x08,0x06,baud_hex[baud_indx][0],baud_hex[baud_indx][1],
                   baud_hex[baud_indx][2],0x00,0x00] # instruction packet 

    prev_ser.write(info_packet) # change the baud rate
    time.sleep(0.1) # wait to settle
    prev_ser.close() # close old serial port
    time.sleep(0.1) # wait to settle
    ser_new =serial.Serial("/dev/serial0", baudrates[baud_indx],timeout=0) # new serial device
    if ser_new.isOpen() == False:
        ser_new.open() # open serial port if not open
    bytes_to_read = 8
    t0 = time.time()
    while (time.time()-t0)<5:
        counter = ser_new.in_waiting
        if counter > bytes_to_read:
            bytes_data = ser_new.read(bytes_to_read)
            ser_new.reset_input_buffer()
            if bytes_data[0] == 0x5a:
                indx = [ii for ii in range(0,len(baud_hex)) if \
                        baud_hex[ii][0]==bytes_data[3] and
                        baud_hex[ii][1]==bytes_data[4] and
                        baud_hex[ii][2]==bytes_data[5]]
                print('Set Baud Rate = {0:1d}'.format(baudrates[indx[0]]))
                time.sleep(0.1) 
                return ser_new
            else:
                ser_new.write(info_packet) # try again if wrong data received
                time.sleep(0.1) # wait 100ms
                continue

#
############################
# Configurations
############################
#
baudrates = [9600,19200,38400,57600,115200,230400,460800,921600] # baud rates
prev_indx = 4 # previous baud rate index (current TF-Luna baudrate)
prev_ser = serial.Serial("/dev/serial0", baudrates[prev_indx],timeout=0) # mini UART serial device
if prev_ser.isOpen() == False:
    prev_ser.open() # open serial port if not open
baud_indx = 4 # baud rate to be changed to (new baudrate for TF-Luna)
ser = set_baudrate(baud_indx) # set baudrate, get new serial at new baudrate
set_samp_rate(100) # set sample rate 1-250
get_version() # print version info for TF-Luna
#
##############################################
# Plotting functions
##############################################
#
def plotter():
    ################################################
    # ---- start real-time ranging and strength bar
    ################################################
    #
    plt.style.use('ggplot') # plot formatting
    fig,axs = plt.subplots(1,2,figsize=(12,8),
                        gridspec_kw={'width_ratios': [5,1]}) # create figure
    fig.canvas.manager.set_window_title('TF-Luna Real-Time Ranging')
    fig.subplots_adjust(wspace=0.05)
    # ranging axis formatting
    axs[0].set_xlabel('Sample',fontsize=16)
    axs[0].set_ylabel('Amplitude',fontsize=16) # amplitude label
    axs[0].set_xlim([0.0,plot_pts])
    axs[0].set_ylim([0.0,8.0]) # set ranging limits
    # signal strength axis formatting
    axs[1].set_xlim([-1.0,1.0]) # strength bar width
    axs[1].set_xticks([]) # remove x-ticks
    axs[1].set_ylim([1.0,2**16]) # set signal strength limits
    axs[1].yaxis.tick_right() # move strength ticks to right
    axs[1].yaxis.set_label_position('right') # label to right
    axs[1].set_ylabel('Signal Strength',fontsize=16,labelpad=6.0)
    axs[1].set_yscale('log') # log scale for better visual
    # draw and background specification
    fig.canvas.draw() # draw initial plot
    ax1_bgnd = fig.canvas.copy_from_bbox(axs[0].bbox) # get background
    ax2_bgnd = fig.canvas.copy_from_bbox(axs[1].bbox) # get background
    line1, = axs[0].plot(np.zeros((plot_pts,)),linewidth=3.0,
                color=plt.cm.Set1(1)) # dummy initial ranging data (zeros)
    bar1,  = axs[1].bar(0.0,1.0,width=1.0,color=plt.cm.Set1(2))
    fig.show() # show plot
    return fig,axs,ax1_bgnd,ax2_bgnd,line1,bar1

def plot_updater():
    ##########################################
    # ---- time series 
    fig.canvas.restore_region(ax1_bgnd) # restore background 1 (for speed)
    fig.canvas.restore_region(ax2_bgnd) # restore background 2
    line1.set_ydata(dist_array) # update channel data
    bar1.set_height(strength) # update signal strength
    if strength<100.0 or strength>30000.0:
        bar1.set_color(plt.cm.Set1(0)) # if invalid strength, make bar red
    else:
        bar1.set_color(plt.cm.Set1(2)) # green bar
    axs[0].draw_artist(line1) # draw line
    axs[1].draw_artist(bar1) # draw signal strength bar
    fig.canvas.blit(axs[0].bbox) # blitting (for speed)
    fig.canvas.blit(axs[1].bbox) # blitting
    fig.canvas.flush_events() # required for blitting
    return line1,bar1
#
############################
# Real-Time Plotter Loop
############################
#
plot_pts = 100 # points for sample rate test
fig,axs,ax1_bgnd,ax2_bgnd,line1,bar1 = plotter() # instantiate figure and plot
dist_array = [] # for updating values
print('Starting Ranging...')
while True:
    distance,strength,temperature = read_tfluna_data() # read values
    dist_array.append(distance) # append to array
    if len(dist_array)>plot_pts:
        dist_array = dist_array[1:] # drop first point (maintain array size)
        line1,bar1 = plot_updater() # update plot
ser.close() # close serial port

