######################################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
######################################################
#
# TF-Luna Mini LiDAR wired to a Raspberry Pi via UART
# --- test ranging plotter for TF-Luna
#
#
######################################################
#
import time
import numpy as np

import tfluna
#
############################
# Testing the TF-Luna Output
############################
#
with tfluna.TfLuna(baud_speed=115200) as tfluna:

    tot_pts = 100 # points for sample rate test
    time_array,dist_array = [],[] # for storing values
    print('Starting Ranging...')
    while len(dist_array)<tot_pts:
        try:
            distance,strength,temperature = tfluna.read_tfluna_data() # read values
            dist_array.append(distance) # append to array
            time_array.append(time.time())
        except:
            continue
    print('Sample Rate: {0:2.0f} Hz'.format(len(dist_array)/(time_array[-1]-time_array[0]))) # print sample rate
#
##############################
# Plotting the TF-Luna Output
##############################
#
import matplotlib.pyplot as plt

plt.style.use('ggplot') # figure formatting
fig,ax = plt.subplots(figsize=(12,9)) # figure and axis
ax.plot(np.subtract(time_array,time_array[0]),dist_array,linewidth=3.5) # plot ranging data
ax.set_ylabel('Distance [m]',fontsize=16) 
ax.set_xlabel('Time [s]',fontsize=16)
ax.set_title('TF-Luna Ranging Test',fontsize=18)
plt.show() # show figure
