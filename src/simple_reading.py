#
############################
# Testing the TF-Luna Output
############################
#

import tfluna 

with tfluna.TfLuna() as tfluna:
    try:
        tfluna.get_version()
        tfluna.set_samp_rate(10)
        
        for i in range(10):
            distance,strength,temperature = tfluna.read_tfluna_data() # read values
            print(f'Distance: {distance:2.2f} m, Strength: {strength:2.0f} / 65535 (16-bit), Chip Temperature: {temperature:2.1f} C') # print sample data
    except TimeoutError:
        print(f"Timeout while communicating with the Tf Luna sensor, exiting")