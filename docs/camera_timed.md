

<a id="camera_timed"></a>

# camera\_timed

Camera Timed Module

A module for controlling Chronos 2.1(HD) high-speed cameras through their API. Features include:
- Switching between two cameras based on configurable time cadence
- Controlling drum RPM via the UCL Tombola Controller API
- Recording management (start/stop/save recordings)
- Camera setup and configuration
- Settings management through a JSON configuration file

The module implements a CameraClass to handle all camera operations including recording,
file saving, and drum speed control. It's designed to work with either one or two cameras
based on configuration settings.

Dependencies:
    - requests: For API communication
    - threading: For timer-based camera switching
    - datetime: For timestamped filenames
    - app_control: For settings management
    - logmanager: For logging operations

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

Sets the drum RPM (revolutions per minute) by sending a POST request to
a specified drum URL with the desired speed value.

Attempts to send the specified speed information as a JSON payload to the
tombola controller api endpoint. If the request succeeds, the speed value is
returned. If the request times out, an error message is logged, and a
default value is returned.

Args:
    speed (float): Desired drum speed in revolutions per minute (0.1 to 79.9).

Returns:
    float: The RPM value that was set if the request succeeds, or 0.0
    if the request times out.

<a id="camera_timed.CameraClass.get_drum_rpm"></a>

#### get\_drum\_rpm

```python
def get_drum_rpm()
```

Fetches the drum's rotations per minute (RPM) from a remote service.

This function sends a POST request to the tombola controller api endpoint with a payload requesting
the RPM of the drum. If the request is successful, the RPM value is extracted and
returned. In case of a timeout, it logs an error and returns a default value of 0.0.

Raises:
    KeyError: If the expected 'rpm' key is not present in the JSON response.

Args:
    None

Returns:
    float: The RPM of the drum, or 0.0 if the request times out.

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

