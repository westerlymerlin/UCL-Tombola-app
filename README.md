# UCL-tombola

**An application to gather data from the UCL Riverbed simulator.**
<br>
The River simulator consistes of a large (1m diameter) drum that can contain water, cement blocks simulate rocks on the riverbed.

A high speed camera is used to capture images from the simulator

An [Adafruit FT232H Breakout - General Purpose USB to GPIO, SPI, I2C - USB C](https://www.adafruit.com/product/2264) is 
used to read positional info from the drum.

Python instructions are [here](https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h)

**API Messages sent to the Tombola Motor Controller API**
<br>
`{"setrpm": n.n}`  Start the tombola running and hold it at n.n rpm (0.1 - 74.9 rpm)<br>
`{"setrpm": 0}`  Stop the tombola<br>

---
