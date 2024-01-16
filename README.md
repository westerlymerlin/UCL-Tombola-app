# UCL-tombola

**An application to gather data from the UCL Riverbed simulator.**
<br>
The River simulator consistes of a large (1m diameter) drum that can contain water, cement blocks simulate rocks on the riverbed.

A high speed camera is used to capture images from the simulator

An [Adafruit FT232H Breakout - General Purpose USB to GPIO, SPI, I2C - USB C](https://www.adafruit.com/product/2264) is 
used to read positional info from the drum.

Python instructions [are here](https://github.com/adafruit/Adafruit_Blinka)

A chronos 2.1(HD) Hisgh speed camera [description here](https://www.krontech.ca/product/chronos-2-1-hd-high-speed-camera/)

Camera API [description is here](https://www.krontech.ca/wp-content/uploads/2020/05/WebAPI_Printout.pdf)

---
**Sample Code**<br>
`example.py` example of a python script that controls the drum speed and records a series of images.

---
**CameraClass**

The camera class has 4 public methods:
`start_camera`: Starts the camera sensor/record process.<br>
`stop_camera`: Stops the camera sensor/record process.<br>
`set_drum_rpm`: Sets the desired RPM of the drum.<br>
`get_drum_rpm`: Gets the RPM of the drum.



