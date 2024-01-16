"""
This is an example sequence and shows how to use the tombola-app

    Camera.set_drum_rpm(rpm)        Set the drum rotating at a speed of rpm
    Camera.get_drum_rpm()           Get the actual speed of the drum
    Camera.start_camera()           Start the camera recording
    Camera.stop_camera()            Stop the camera recording
    sleep(seconds)                  Wait for (seconds) before executing the next command
"""

from time import sleep
from camera_control import CameraClass

if __name__ == "__main__":
    # code to execute when the script is run directly
    Camera = CameraClass()  # create a camera object
    print('Starting UCL-Tombola sequence')
    sleep(2)
    print('starting the drum at 60 rpm')
    Camera.set_drum_rpm(60)
    sleep(5)
    print('drum is at %s rpm' % Camera.get_drum_rpm())
    sleep(5)
    print('slowing the drum to 58 rpm')
    Camera.set_drum_rpm(58)
    sleep(5)
    print('slowing the drum to 56 rpm')
    Camera.set_drum_rpm(56)
    sleep(5)
    print('slowing the drum to 54 rpm')
    Camera.set_drum_rpm(54)
    sleep(5)
    print('slowing the drum to 52 rpm')
    Camera.set_drum_rpm(52)
    sleep(5)
    print('slowing the drum to 50 rpm')
    Camera.set_drum_rpm(50)
    print('Starting the camera sensor')
    Camera.start_camera()
    sleep(60)
    print('Stopping the camera sensor')
    Camera.stop_camera()
    print('stopping the drum')
    Camera.set_drum_rpm(0)
