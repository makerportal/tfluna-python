# TF-Luna LiDAR Python Driver

The [TF-Luna sensor](https://www.dfrobot.com/product-1995.html) is a LiDAR sensor, which can be read either with I2C or Serial.

This repository contains the code permitting to use the TF-Luna sensor with the serial interface.

This repository is a fork of [tfluna-python](https://github.com/makerportal/tfluna-python), and is a rewrite of the driver to a class-based structure.
The new code is also more careful when it comes to handling the serial interface: this driver is indeed intended to be used (only) as a Python resource, i.e. as follows (more details in the `example` folder):

```
import tfluna
import timeout_decorator

with tfluna.TfLuna(baud_speed=115200, serial_name="/dev/serial0") as tfluna:
    tfluna.get_version()
    tfluna.set_samp_rate(10)
    #tfluna.set_baudrate(57600) # can be used to change the baud_speed
    distance,strength,temperature = tfluna.read_tfluna_data() 
```

### - TF-Luna + Raspberry Pi Wiring - 

The TF-Luna can be wired to the Raspberry Pi via the mini UART port:

![TF-Luna RPi Wiring](https://static1.squarespace.com/static/59b037304c0dbfb092fbe894/t/6009f277b8566661c36dfa67/1611264637375/TF_luna_RPi_wiring.png?format=1500w)

