"""
UCL Tombola Camera Control Script

This module controls a camera system for the UCL Tombola apparatus. It demonstrates
a typical experimental sequence for recording drum rotation at various speeds.

The script:
1. Initializes the camera with specific settings (recording cadence, frame rate)
2. Starts camera recording
3. Controls the drum at various RPM settings in a predefined sequence
4. Monitors drum speed
5. Stops the drum and camera recording when complete

Available Camera Functions:
    Camera.start_camera_recording()     Start the camera recording
    Camera.stop_camera_recording()      Stop the camera recording
    Camera.set_drum_rpm(rpm)            Set the drum rotating at specified RPM
    Camera.get_drum_rpm()               Get the current speed of the drum
    Camera.change_setting(key, value)   Configure camera settings
    Camera.print_settings_to_console()  Display all current settings

Dependencies:
    - time.sleep: Used for timing control between operations
    - camera_timed.CameraClass: Camera control interface
"""

from time import sleep
from camera_timed import CameraClass

if __name__ == "__main__":
    # code to execute when the script is run directly
    Camera = CameraClass()  # create a camera object
    Camera.change_setting('recording_cadence', 10)  # make the camera record 10 seconds before switching
    # to the 2nd camera
    Camera.change_setting('camera_frame_rate', 250)  # set the frame rate
    Camera.print_settings_to_console()  # display all the application settings in the pyton console

    print('Starting UCL-Tombola sequence')
    print('Starting the camera sensor')
    Camera.start_camera_recording()
    sleep(2)
    print('starting the drum at 95 rpm for 1 minute')
    Camera.set_drum_rpm(95)
    sleep(30)
    print('drum is at %s rpm' % Camera.get_drum_rpm())
    sleep(30)
    print('slowing the drum to 80 rpm')
    Camera.set_drum_rpm(80)
    sleep(20)
    print('slowing the drum to 78 rpm')
    Camera.set_drum_rpm(78)
    sleep(10)
    print('slowing the drum to 76 rpm')
    Camera.set_drum_rpm(76)
    sleep(10)
    print('slowing the drum to 74 rpm')
    Camera.set_drum_rpm(74)
    sleep(10)
    print('slowing the drum to 73 rpm')
    Camera.set_drum_rpm(73)
    sleep(10)
    print('slowing the drum to 72 rpm')
    Camera.set_drum_rpm(72)
    sleep(10)
    print('slowing the drum to 71.5 rpm')
    Camera.set_drum_rpm(71.5)
    sleep(10)
    print('drum is at %s rpm' % Camera.get_drum_rpm())
    sleep(120)
    print('stopping the drum')
    Camera.set_drum_rpm(0)
    sleep(10)
    print('Stopping the camera sensor')
    Camera.stop_camera_recording()
    sleep(2)
