# TF-Luna LiDAR with Raspberry Pi
Python codes for configuring and reading the TF-Luna Light Detection And Ranging (LiDAR) module interfaced with a Raspberry Pi computer.

Tutorial: https://makersportal.com/blog/distance-detection-with-the-tf-luna-lidar-and-raspberry-pi

Buy a TF-Luna from our Store: https://makersportal.com/shop/tf-luna-lidar-module

#

### - TF-Luna + Raspberry Pi Wiring - 

The TF-Luna can be wired to the Raspberry Pi via the mini UART port:

![TF-Luna RPi Wiring](https://static1.squarespace.com/static/59b037304c0dbfb092fbe894/t/6009f277b8566661c36dfa67/1611264637375/TF_luna_RPi_wiring.png?format=1500w)

---
### - TF-Luna Ranging Test - 

The script entitled 'tfluna_test_plot.py' outputs a plot similar to the following:

![TF-Luna Ranging Test](./images/tfluna_test_plot_white.png)

---
### - Real-Time Ranging Visualization - 

The script entitled 'tfluna_test_realtime.py' outputs a real-time output of distance and signal strength, similar to the following:

![TF-Luna Real-Time Ranging](./images/tfluna_realtime_plot_white.png)
