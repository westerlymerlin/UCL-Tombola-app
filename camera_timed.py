"""
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

"""

import threading
from datetime import datetime
import requests
from app_control import settings, writesettings
from logmanager import logger


class CameraClass:
    """
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
    """
    def __init__(self):
        self.running = False
        self.headers = {"Accept": "application/json",
                        "Content-Type": "application/json",
                        "api-key": settings['drum_apikey']}
        self.camera_url1 = settings['camera_controller1']
        self.camera_url2 = settings['camera_controller2']
        self.camera_timeout = settings['camera_controller_timeout']
        self.drum_url = settings['drum_controller']
        self.drum_timeout = settings['drum_controller_timeout']
        self.recording_cadence = settings['recording_cadence']
        self.filename = None
        self.recording_time = None
        self.camera_no = None

    def setup_cameras(self):
        """Calculate number of frames to record and send details to camera"""
        frame_period = int(round((1/settings['camera_frame_rate']) * 1000000000, 0))
        data_message = {'recMode': settings['camera_recMode'], 'framePeriod': frame_period,
                        'recMaxFrames': settings['camera_maxframes']}
        url = self.camera_url1 + '/p'
        try:
            response = requests.post(url, timeout=self.camera_timeout, json=data_message, headers=self.headers)
            # print(response)
            if response.status_code == 200:
                logger.debug('CameraClass: Setup for camera 1 completed')
            else:
                logger.warning('CameraClass: Failed to Setup camera 1 - check camera status')
        except requests.Timeout:
            logger.error('CameraClass: Timeout when setting up camera 1')
        if settings['camera_qty'] == 2:
            try:
                url = self.camera_url2 + '/p'
                response = requests.post(url, timeout=self.camera_timeout, json=data_message, headers=self.headers)
                if response.status_code == 200:
                    logger.debug('CameraClass: Setup for camera 2 completed')
                else:
                    logger.warning('CameraClass: Failed to Setup camera 2 - check camera status')
            except requests.Timeout:
                logger.error('CameraClass: Failed to Setup camera 2 - check camera status')

    def start_camera_recording(self):
        """Starts the camera sensor/record process."""
        print('Starting camera recording')
        logger.info('CameraClass: starting camera recording')
        # self.setup_cameras()
        self.running = True
        self.camera_no = 1
        self.recording_time = 0
        self.__start_recording(self.camera_no)
        threading.Timer(0.1, self.global_timer).start()

    def stop_camera_recording(self):
        """Stops the camera sensor/record process."""
        self.running = False
        self.__stop_recording(1)
        self.__file_save(1, self.filename)
        self.__stop_recording(2)
        print('Stopped all camera recording')
        logger.info('CameraClass: Stopping auto recording')

    def global_timer(self):
        """used when running to run times events"""
        if self.running:
            timerthread = threading.Timer(1, self.global_timer)
            timerthread.start()
            if self.recording_time == settings['recording_cadence']:
                self.switch_camera()
            else:
                self.recording_time += 1

    def switch_camera(self):
        """save the current set of images and then switch to the other camera"""
        print('Recording time is up - switching cameras now')
        self.recording_time = 0
        if self.camera_no == 1:
            self.camera_no = 2
            self.__flush_recording(2)
            self.__start_recording(2)
            self.__stop_recording(1)
            self.__file_save(1, self.filename)
        else:
            self.camera_no = 1
            self.__flush_recording(1)
            self.__start_recording(1)
            self.__stop_recording(2)
            self.__file_save(2, self.filename)
        print('CameraClass: Switched completed to camera %s' % self.camera_no)

    def __flush_recording(self, camera_id):
        """Send a Start recording API call to the camera"""
        if camera_id > settings['camera_qty']:
            print('Only 1 camera installed skipping flush recording camera 2')
            return
        if camera_id == 1:
            url = self.camera_url1 + '/flushRecording'
        else:
            url = self.camera_url2 + '/flushRecording'
        try:
            response = requests.get(url, timeout=self.camera_timeout, headers=self.headers)
            if response.status_code == 200:
                print('CameraClass: Camera %s flush recording' % camera_id)
                logger.debug('CameraClass: flush recording %s', camera_id)
            else:
                print('CameraClass: Failed to flush recording check camera. status = %s' % camera_id)
                logger.warning('CameraClass: Failed to flush recording check camera. status = %s', camera_id)
        except requests.Timeout:
            print('CameraClass: Timeout when flushing recording camera %s' % camera_id)
            logger.error('CameraClass: Timeout when flushing recordingcamera %s', camera_id)

    def __start_recording(self, camera_id):
        """Send a Start recording API call to the camera"""
        if camera_id > settings['camera_qty']:
            print('Only 1 camera installed skipping starting camera 2')
            return
        if camera_id == 1:
            url = self.camera_url1 + '/startRecording'
        else:
            url = self.camera_url2 + '/startRecording'
        try:
            response = requests.get(url, timeout=self.camera_timeout, headers=self.headers)
            if response.status_code == 200:
                print('CameraClass: Camera %s starting recording' % camera_id)
                logger.debug('CameraClass: Recording started camera %s', camera_id)
            else:
                print('CameraClass: Failed to start recording check camera. status = %s' % camera_id)
                logger.warning('CameraClass: Failed to start recording check camera. status = %s', camera_id)
        except requests.Timeout:
            print('CameraClass: Timeout when starting the camera %s' % camera_id)
            logger.error('CameraClass: Timeout when starting the camera %s', camera_id)

    def __stop_recording(self, camera_id):
        """Send a Stop recording API call to the camera"""
        self.filename = datetime.now().strftime('UCL-Tombola_%Y-%m-%d_%H-%M-%S')
        if camera_id > settings['camera_qty']:
            print('Only 1 camera installed skipping stopping camera 2')
            return
        if camera_id == 1:
            url = self.camera_url1 + '/stopRecording'
        else:
            url = self.camera_url2 + '/stopRecording'
        try:
            response = requests.get(url, timeout=self.camera_timeout, headers=self.headers)
            if response.status_code == 200:
                print('CameraClass: Camera %s stopping recording' % camera_id)
                logger.debug('CameraClass: Recording stopped camera %s', camera_id)
            else:
                print('CameraClass: Failed to stop recording - check camera %s status' % camera_id)
                logger.warning('CameraClass: Failed to stop recording - check camera %s status', camera_id)
        except requests.Timeout:
            print('CameraClass: Timeout when stopping the camera %s' % camera_id)
            logger.error('CameraClass: Timeout when stopping the camera %s', camera_id)

    def __file_save(self, camera_id, filename):
        """Send a file save API call to the camera - format and file extension are in the settings.json file"""
        if camera_id > settings['camera_qty']:
            print('Only 1 camera installed skipping file saving to camera 2')
        if camera_id == 1:
            url = self.camera_url1 + '/startFilesave'
        else:
            url = self.camera_url2 + '/startFilesave'
        payload = {'filename': filename,
                   'device': settings['camera_storage'],
                   'format': settings['camera_format']}
        try:
            response = requests.post(url, json=payload, timeout=self.camera_timeout, headers=self.headers)
            if response.status_code == 200:
                print('CameraClass: File saved camera = %s filename = %s' % (camera_id, filename))
                logger.debug('CameraClass: File saved')
            else:
                print('CameraClass: Failed to save file please check camera. status code = %s' % response.status_code)
                logger.warning('CameraClass: Failed to save file please check camera. status code = %s',
                               response.status_code)
        except requests.Timeout:
            logger.error('CameraClass: Timeout when saving a file to the camera, check it is on and connected')

    def set_drum_rpm(self, speed: float):
        """Sets the drum RPM (revolutions per minute) by sending a POST request to
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
        """
        payload = {"setrpm": speed}
        try:
            requests.post(self.drum_url, json=payload, timeout=self.drum_timeout, headers=self.headers)
            print('CameraClass: Drum speed set to %s' % str(speed))
            return speed
        except requests.Timeout:
            print('CameraClass: set_drum_speed request timed out, check the raspberry pi')
            logger.error("CameraClass: set_drum_speed request timed out, check the raspberry pi")
            return 0.0

    def get_drum_rpm(self):
        """
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
        """
        payload = {"rpm": True}
        try:
            response = requests.post(self.drum_url, json=payload, timeout=self.drum_timeout, headers=self.headers)
            rpm = response.json()['rpm']
            return rpm
        except requests.Timeout:
            logger.error("CameraClass: set_drum_speed request timed out")
            return 0.0

    def print_settings_to_console(self):
        """Shows the current set of settings in the Json file"""
        format_string = "{:<40}"
        print('\nUCL Tombola App Settings:')
        print('%s%s' % (format_string.format('Setting'), 'Value'))
        print('%s%s' % (format_string.format('-------'), '-----'))
        for item in settings:
            print('%s%s' % (format_string.format(item), settings[item]))

    def change_setting(self, setting, value):
        """Update the setting in the settings json file"""
        settings[setting] = value
        writesettings()
