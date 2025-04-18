# Module Documentation


This document contains the documentation for all the modules in the **UCL-Tombola-app** version 2.0.2 application.

---

## Contents


[app_control](./app_control.md)  
Settings module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will create from the defaults in the initialise function.
Author: Gary Twinn

[camera_timed](./camera_timed.md)  
Camera Timed - controls a A chronos 2.1(HD) High speed camera via the api, switches between 2 cameras based on the
cadence setting for time. Controls the drum RPM vis the API on the UCL Tombola
Controller

Author: Gary Twinn

[example](./example.md)  
This is an example sequence and shows how to use the tombola-app

    Camera.set_drum_rpm(rpm)        Set the drum rotating at a speed of rpm
    Camera.get_drum_rpm()           Get the actual speed of the drum
    Camera.start_camera()           Start the camera recording
    Camera.stop_camera()            Stop the camera recording
    sleep(seconds)                  Wait for (seconds) before executing the next command

[logmanager](./logmanager.md)  
logmanager, setus up application logging. Ese the **logger** property to
write to the log.
Author: Gary Twinn


---

