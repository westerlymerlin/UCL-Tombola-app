# Contents for: camera_timed

* [camera\_timed](#camera_timed)
  * [threading](#camera_timed.threading)
  * [datetime](#camera_timed.datetime)
  * [requests](#camera_timed.requests)
  * [settings](#camera_timed.settings)
  * [writesettings](#camera_timed.writesettings)
  * [logger](#camera_timed.logger)
  * [CameraClass](#camera_timed.CameraClass)
    * [\_\_init\_\_](#camera_timed.CameraClass.__init__)
    * [setup\_cameras](#camera_timed.CameraClass.setup_cameras)
    * [start\_camera\_recording](#camera_timed.CameraClass.start_camera_recording)
    * [stop\_camera\_recording](#camera_timed.CameraClass.stop_camera_recording)
    * [global\_timer](#camera_timed.CameraClass.global_timer)
    * [switch\_camera](#camera_timed.CameraClass.switch_camera)
    * [\_\_flush\_recording](#camera_timed.CameraClass.__flush_recording)
    * [\_\_start\_recording](#camera_timed.CameraClass.__start_recording)
    * [\_\_stop\_recording](#camera_timed.CameraClass.__stop_recording)
    * [\_\_file\_save](#camera_timed.CameraClass.__file_save)
    * [set\_drum\_rpm](#camera_timed.CameraClass.set_drum_rpm)
    * [get\_drum\_rpm](#camera_timed.CameraClass.get_drum_rpm)
    * [print\_settings\_to\_console](#camera_timed.CameraClass.print_settings_to_console)
    * [change\_setting](#camera_timed.CameraClass.change_setting)

<a id="camera_timed"></a>

# camera\_timed

Camera Timed - controls a A chronos 2.1(HD) High speed camera via the api, switches between 2 cameras based on the
cadence setting for time. Controls the drum RPM vis the API on the UCL Tombola
Controller

Author: Gary Twinn

<a id="camera_timed.threading"></a>

## threading

<a id="camera_timed.datetime"></a>

## datetime

<a id="camera_timed.requests"></a>

## requests

<a id="camera_timed.settings"></a>

## settings

<a id="camera_timed.writesettings"></a>

## writesettings

<a id="camera_timed.logger"></a>

## logger

<a id="camera_timed.CameraClass"></a>

## CameraClass Objects

```python
class CameraClass()
```

CameraClass

A class representing a camera sensor/record process.
It initializes the CameraClass object by setting the properties such as board id, start and end sensors,
running and recording flags, headers, camera url, camera timeout, and drum url and timeout.
It also checks if the CONTROLLER is None and logs an error message if it is.

Methods:
    start_camera_recording: Starts the camera sensor/record process.
    stop_camera_recording: Stops the camera sensor/record process.
    set_drum_rpm: Sets the desired RPM of the drum.
    get_drum_rpm: Gets the RPM of the drum.
    change_setting: Changes the settings stored in the settings.json file
    print_settings_to_console: Prints the settings stored in the settings.json file

<a id="camera_timed.CameraClass.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="camera_timed.CameraClass.setup_cameras"></a>

#### setup\_cameras

```python
def setup_cameras()
```

Calculate number of frames to record and send details to camera

<a id="camera_timed.CameraClass.start_camera_recording"></a>

#### start\_camera\_recording

```python
def start_camera_recording()
```

Starts the camera sensor/record process.

<a id="camera_timed.CameraClass.stop_camera_recording"></a>

#### stop\_camera\_recording

```python
def stop_camera_recording()
```

Stops the camera sensor/record process.

<a id="camera_timed.CameraClass.global_timer"></a>

#### global\_timer

```python
def global_timer()
```

used when running to run times events

<a id="camera_timed.CameraClass.switch_camera"></a>

#### switch\_camera

```python
def switch_camera()
```

save the current set of images and then switch to the other camera

<a id="camera_timed.CameraClass.__flush_recording"></a>

#### \_\_flush\_recording

```python
def __flush_recording(camera_id)
```

Send a Start recording API call to the camera

<a id="camera_timed.CameraClass.__start_recording"></a>

#### \_\_start\_recording

```python
def __start_recording(camera_id)
```

Send a Start recording API call to the camera

<a id="camera_timed.CameraClass.__stop_recording"></a>

#### \_\_stop\_recording

```python
def __stop_recording(camera_id)
```

Send a Stop recording API call to the camera

<a id="camera_timed.CameraClass.__file_save"></a>

#### \_\_file\_save

```python
def __file_save(camera_id, filename)
```

Send a file save API call to the camera - format and file extension are in the settings.json file

<a id="camera_timed.CameraClass.set_drum_rpm"></a>

#### set\_drum\_rpm

```python
def set_drum_rpm(speed: float)
```

Set the desired rpm of the drum
**speed** = float (0.0 - 74.9)

<a id="camera_timed.CameraClass.get_drum_rpm"></a>

#### get\_drum\_rpm

```python
def get_drum_rpm()
```

Get the rpm of the drum

<a id="camera_timed.CameraClass.print_settings_to_console"></a>

#### print\_settings\_to\_console

```python
def print_settings_to_console()
```

Shows the current set of settings in the Json file

<a id="camera_timed.CameraClass.change_setting"></a>

#### change\_setting

```python
def change_setting(setting, value)
```

Update the setting in the settings json file

