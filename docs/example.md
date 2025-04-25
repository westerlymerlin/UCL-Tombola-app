# Contents for: example

* [example](#example)
  * [sleep](#example.sleep)
  * [CameraClass](#example.CameraClass)

<a id="example"></a>

# example

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

<a id="example.sleep"></a>

## sleep

<a id="example.CameraClass"></a>

## CameraClass

