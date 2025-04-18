"""
This is an example sequence and shows how to use the tombola-app

    Camera.set_drum_rpm(rpm)        Set the drum rotating at a speed of rpm
    Camera.get_drum_rpm()           Get the actual speed of the drum
    Camera.start_camera()           Start the camera recording
    Camera.stop_camera()            Stop the camera recording
    sleep(seconds)                  Wait for (seconds) before executing the next command
"""

from time import sleep
from camera_timed import CameraClass

if __name__ == "__main__":
    # code to execute when the script is run directly
    Camera = CameraClass()  # create a camera object
    # make the camera record 10 seconds before switching to the 2nd camera
    Camera.change_setting('recording_cadence', 10)
    # set the frame rate
    Camera.change_setting('camera_frame_rate', 250)
    # display all the application settings in the pyton console
    Camera.print_settings_to_console()

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
