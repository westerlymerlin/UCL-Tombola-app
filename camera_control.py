"""
Camera Control - controls a A chronos 2.1(HD) High speed camera via the api, triggered communicates with the
Hall Effect Sensors connected to an Adafriut USB GPIO board. Controls the drum RPM vis the API on the UCL Tombola
Controller

Author: Gary Twinn
"""

import os
import threading
from datetime import datetime
import requests
import usb
from settings import settings
from logmanager import logger

dev = usb.core.find(idVendor=0x0403, idProduct=0x6014)  # scan the usb to see if the board is conencted
if dev is None:
    CONTROLLER = None
else:
    # print('USB device data:\n', dev)
    os.environ["BLINKA_FT232H"] = "1"  # set an environment variable for the board we are using
    import board
    import digitalio
    CONTROLLER = board.board_id


class CameraClass:
    """
    CameraClass

    A class representing a camera sensor/record process.
    It initializes the CameraClass object by setting the properties such as board id, start and end sensors,
    running and recording flags, headers, camera url, camera timeout, and drum url and timeout.
    It also checks if the CONTROLLER is None and logs an error message if it is.

    Methods:
        start_camera: Starts the camera sensor/record process.
        stop_camera: Stops the camera sensor/record process.
        set_drum_rpm: Sets the desired RPM of the drum.
        get_drum_rpm: Gets the RPM of the drum.

    """
    def __init__(self):
        self.board_id = None
        self.start_sensor = None
        self.end_sensor = None
        self.runnning = False
        self.recording = False
        self.headers = {"Accept": "application/json", "api-key": settings['drum_apikey']}
        self.camera_url = settings['camera_controller']
        self.camera_timeout = settings['camera_controller_timeout']
        self.drum_url = settings['drum_controller']
        self.drum_timeout = settings['drum_controller_timeout']
        if CONTROLLER is not None:
            self.board_id = CONTROLLER
            self.start_sensor = digitalio.DigitalInOut(board.C0)
            self.start_sensor.direction = digitalio.Direction.INPUT
            self.end_sensor = digitalio.DigitalInOut(board.C1)
            self.end_sensor.direction = digitalio.Direction.INPUT
            logger.info('CameraClass: Detected GPIO adapter: %s', CONTROLLER)
        else:
            logger.error('CameraClass: GPIO adapter missing')

    def start_camera(self):
        """Starts the camera sensor/record process."""
        if self.board_id is not None:
            self.runnning = True
            thread = threading.Thread(target=self.__gpio_monitor)
            thread.start()
        else:
            logger.error('CameraClass: Start with no GPIO Board Installed')

    def stop_camera(self):
        """Stops the camera sensor/record process."""
        self.runnning = False
        logger.debug('CameraClass: Exiting')

    def set_drum_rpm(self, speed: float):
        """Set the desired rpm of the drum
        **speed** = float (0.0 - 74.9)"""
        payload = {"setrpm": speed}
        try:
            requests.post(self.drum_url, json=payload, timeout=self.drum_timeout, headers=self.headers)
            return speed
        except requests.Timeout:
            logger.error("CameraClass: set_drum_speed request timed out")
            return 0.0

    def get_drum_rpm(self):
        """Get the rpm of the drum"""
        payload = {"rpm": True}
        try:
            response = requests.post(self.drum_url, json=payload, timeout=self.drum_timeout, headers=self.headers)
            rpm = response.json()['rpm']
            return rpm
        except requests.Timeout:
            logger.error("CameraClass: set_drum_speed request timed out")
            return 0.0

    def __gpio_monitor(self):
        """GPIO Scanner thread scans the start and end sensor pins"""
        startsensorvalue = False
        endsensorvalue = False
        while self.runnning:
            if startsensorvalue != self.start_sensor.value:
                if self.start_sensor.value is False:
                    self.__start_detect()
            if endsensorvalue != self.end_sensor.value:
                if self.end_sensor.value is False:
                    self.__end_detect()
            startsensorvalue = self.start_sensor.value
            endsensorvalue = self.end_sensor.value

    def __start_detect(self):
        """Actions to do if the start sensor is triggered"""
        logger.debug('CameraClass: Start Sensor Triggered')
        self.__start_recording()

    def __end_detect(self):
        """Actions to do if the end sensor is triggered"""
        logger.debug('CameraClass: End Sensor Triggered')
        self.__stop_recording()
        self.__file_save()

    def __start_recording(self):
        """Send a Start recoording API call to the camera"""
        if self.recording:
            logger.warning('CameraClass: start_recording: Recording is already in progress')
            return
        url = self.camera_url + '/startRecording'
        try:
            response = requests.get(url, timeout=self.camera_timeout, headers=self.headers)
            if response.status_code == 200:
                self.recording = True
                logger.debug('CameraClass: Recording started')
            else:
                logger.warning('CameraClass: Failed to start recording - check camera status')
        except requests.Timeout:
            logger.error('CameraClass: Timeout when starting the camera')

    def __stop_recording(self):
        """ Send a stop recording API call to the Camera"""
        if not self.recording:
            logger.warning('CameraClass: stop_recording: Recording is already stopped')
            return
        url = self.camera_url + '/stopRecording'
        try:
            response = requests.get(url, timeout=self.camera_timeout, headers=self.headers)
            if response.status_code == 200:
                self.recording = False
                logger.debug('CameraClass: Recording stopped')
            else:
                logger.warning('CameraClass: Failed to stop recording - check camera status')
        except requests.Timeout:
            logger.error('CameraClass: Timeout when stopping the camera')

    def __file_save(self):
        """Send a file save API call to the camera - format and file extentioon are in the settings.json file"""
        if self.recording:
            logger.warning('CameraClass: file_save: Recording is in progress so cannot save the file')
            return
        url = self.camera_url + 'startFilesave'
        payload = {'filename': datetime.now().strftime('UCL-Tombola_%Y-%m-%d_%H-%M-%S.%f.'
                                                       + settings['camera_file_extention']),
                   'device': settings['camera_storage'],
                   'format': settings['camera_format']}
        try:
            response = requests.get(url, json=payload, timeout=self.camera_timeout, headers=self.headers)
            if response.status_code == 200:
                self.recording = True
                logger.debug('CameraClass: File saved')
            else:
                logger.warning('CameraClass: Failed to save file - check camera status')
        except requests.Timeout:
            logger.error('CameraClass: Timeout when saving a file to the camera')
