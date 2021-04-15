#
############################
# Testing the TF-Luna Output
############################
#

import timeout_decorator
import tfluna 

with tfluna.TfLuna(baud_speed=115200) as tfluna:
    try:
        tfluna.get_version()
        #tfluna.set_samp_rate(10)
        #tfluna.set_baudrate(57600)
        #tfluna.set_baudrate(115200)

        for i in range(10):
            distance,strength,temperature = tfluna.read_tfluna_data() # read values
            print(f'Distance: {distance:2.2f} m, Strength: {strength:2.0f} / 65535 (16-bit), Chip Temperature: {temperature:2.1f} C') # print sample data
    
    except timeout_decorator.TimeoutError:
        print(f"Timeout while communicating with the Tf Luna sensor, exiting")