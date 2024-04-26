"""
Camera Control - controls a A chronos 2.1(HD) High speed camera via the api, triggered communicates with the
Hall Effect Sensors connected to an Adafriut USB GPIO board. Controls the drum RPM vis the API on the UCL Tombola
Controller

Author: Gary Twinn
"""

import os
import threading
from time import sleep
from datetime import datetime
import requests
import usb
from app_control import settings, writesettings
from logmanager import logger

dev = usb.core.find(idVendor=0x0403, idProduct=0x6014)  # scan the usb to see if the board is conencted
if dev is None:
    CONTROLLER = None
else:
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
        change_setting: Changes the settings stored in the settings.json file
        show_settings: Prints the settings stored in the settings.json file
    """
    def __init__(self):
        self.board_id = None
        self.start_sensor = None
        self.end_sensor = None
        self.runnning = False
        self.recording = False
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
        self.switchime = None
        self.camera = 0
        self.recording_counter = 0
        if CONTROLLER is not None:  # The USB device is plugges in and working
            self.board_id = CONTROLLER
            self.start_sensor = digitalio.DigitalInOut(board.C0)
            self.start_sensor.direction = digitalio.Direction.INPUT
            self.end_sensor = digitalio.DigitalInOut(board.C1)
            self.end_sensor.direction = digitalio.Direction.INPUT
            logger.info('CameraClass: Detected GPIO adapter: %s', CONTROLLER)
        else:
            logger.error('CameraClass: GPIO adapter missing')
            print('CameraClass: GPIO adapter missing')


    def setup_cameras(self):
        """Calculate number of frames to record and send details to camera"""
        rpm = self.get_drum_rpm()
        if rpm > 1:
            frames = int(round(settings['camera_frame_rate']*(((60/rpm)/360)*settings['camera_degrees']), 0))
        else:
            frames = settings['camera_frame_rate'] * 10
        frame_period = int(round((1/settings['camera_frame_rate']) * 1000000000, 0))
        data_message = {'recMode': settings['camera_recMode'], 'recMaxFrames': frames, 'framePeriod': frame_period }
        print(data_message)
        url = self.camera_url1 + '/control/p'
        try:
            response = requests.post(url, timeout=self.camera_timeout, data=data_message, headers=self.headers)
            if response.status_code == 200:
                self.recording = True
                logger.debug('CameraClass: Setup for camera 1 completed')
            else:
                logger.warning('CameraClass: Failed to Setup camera 1 - check camera status')
        except requests.Timeout:
            logger.error('CameraClass: Timeout when setting up camera 1')
        if settings['camera_qty'] == 2:
            try:
                url = self.camera_url2 + '/control/p'
                response = requests.post(url, timeout=self.camera_timeout, data=data_message, headers=self.headers)
                if response.status_code == 200:
                    self.recording = True
                    logger.debug('CameraClass: Setup for camera 2 completed')
                else:
                    logger.warning('CameraClass: Failed to Setup camera 2 - check camera status')
            except requests.Timeout:
                logger.error('CameraClass: Failed to Setup camera 2 - check camera status')

    def start_camera(self):
        """Starts the camera sensor/record process."""
        if self.board_id is not None:
            self.runnning = True
            self.setup_cameras()
            self.filename = datetime.now().strftime('UCL-Tombola-%Y-%m-%d-%H-%M-%S')
            thread = threading.Thread(target=self.__gpio_block1_sensor_monitor)
            thread.start()
            thread = threading.Thread(target=self.__gpio_block2_sensor_monitor)
            thread.start()
            logger.info('CameraClass: Starting auto recording, looking for sensor signals')
        else:
            logger.error('CameraClass: Start with no GPIO Board Installed')

    def stop_camera(self):
        """Stops the camera sensor/record process."""
        self.runnning = False
        logger.info('CameraClass: Stopping auto recording, ignoring sensor signals')

    def switch_camera(self):
        """save the current set of images and then switch to the other camera"""
        self.__file_save(self.camera, self.filename)
        if self.camera == 1:
            self.camera = 2
        else:
            self.camera = 1
        self.filename = datetime.now().strftime('UCL-Tombola-%Y-%m-%d-%H-%M-%S')
    def __gpio_block1_sensor_monitor(self):
        """GPIO Scanner thread scans the start sensor pin for a leading edge signal"""
        previous_sensor_state = False
        while self.runnning:
            current_sensor_state = self.start_sensor.value
            if previous_sensor_state != current_sensor_state and current_sensor_state is False:
                thread = threading.Thread(target=self.__block_1_detect)
                thread.start()
                sleep(settings['sensor_debounce_time'])
            previous_sensor_state = current_sensor_state


    def __gpio_block2_sensor_monitor(self):
        """GPIO Scanner thread scans the end sensor pin for a leading edge signal"""
        previous_sensor_state = False
        while self.runnning:
            current_sensor_state = self.end_sensor.value
            if previous_sensor_state != current_sensor_state and current_sensor_state is False:
                thread = threading.Thread(target=self.__block_2_detect)
                thread.start()
                sleep(settings['sensor_debounce_time'])
            previous_sensor_state = current_sensor_state

    def __block_1_detect(self):
        """Actions to do if the start sensor is triggered"""
        logger.debug('CameraClass: Block 1 Start Sensor Triggered')
        # print('CameraClass: Block 1 Sensor Triggered')
        if self.recording_counter < self.recording_cadence * 2:
            self.__start_recording()
        self.recording_counter += 1
        if self.recording_counter == self.recording_cadence * 2:
            self.switch_camera()

    def __block_2_detect(self):
        """Actions to do if the start sensor is triggered"""
        logger.debug('CameraClass: Block 2 Start Sensor Triggered')
        # print('CameraClass: Block 2 Sensor Triggered')
        if self.recording_counter < self.recording_cadence * 2:
            self.__start_recording()
        self.recording_counter += 1
        if self.recording_counter == self.recording_cadence * 2:
            self.switch_camera()

    def __start_recording(self):
        """Send a Start recording API call to the camera"""
        if self.recording:
            logger.warning('CameraClass: start_recording: Recording is already in progress')
            return
        if self.camera == 1:
            url = self.camera_url1 + '/startRecording'
        else:
            url = self.camera_url2 + '/startRecording'
        try:
            response = requests.get(url, timeout=self.camera_timeout, headers=self.headers)
            if response.status_code == 200:
                self.recording = True
                logger.debug('CameraClass: Recording started camera %s', self.camera)
            else:
                logger.warning('CameraClass: Failed to start recording - check camera %s status', self.camera)
        except requests.Timeout:
            logger.error('CameraClass: Timeout when starting the camera %s', self.camera)

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

    def __file_save(self, camera_id, filename):
        """Send a file save API call to the camera - format and file extentioon are in the settings.json file"""
        if self.recording:
            logger.warning('CameraClass: file_save: Recording is in progress so cannot save the file')
            return
        if camera_id == 1:
            url = self.camera_url1 + '/startRecording'
        else:
            url = self.camera_url2 + '/startRecording'
        payload = {'filename': filename,
                   'device': settings['camera_storage'],
                   'format': settings['camera_format']}
        try:
            response = requests.post(url, json=payload, timeout=self.camera_timeout, headers=self.headers)
            if response.status_code == 200:
                self.recording = True
                print('CameraClass: File saved')
                logger.debug('CameraClass: File saved')
            else:
                logger.warning('CameraClass: Failed to save file - check camera status %s', response.status_code)
        except requests.Timeout:
            logger.error('CameraClass: Timeout when saving a file to the camera, check it is on and connected')

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

    def show_settings(self):
        """Shows the current set of settings in the Json file"""
        print('\nUCL Tombola App Settings:')
        print('%s%s' % ("{:<40}".format('Setting'), 'Value'))
        print('%s%s' % ("{:<40}".format('-------'), '-----'))
        for item in settings:
            print('%s%s' % ("{:<40}".format(item), settings[item]))

    def change_setting(self, setting, value):
        """Update the setting in the settings json file"""
        settings[setting] = value
        writesettings()

if __name__ == "__main__":
    camera = CameraClass()
    camera.show_settings()