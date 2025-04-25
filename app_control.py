"""
Settings Management Module

This module handles application configuration settings with JSON persistence.
It provides functionality to read, write, and initialize application settings
from a settings.json file with fallback to defaults when settings are missing.

Features:
- Automatic creation of settings.json if not present
- Default values for all settings
- Persistence of settings to JSON format
- Automatic detection and addition of new settings
- Timestamp tracking of settings modifications

Usage:
    import from app_control import settings, writesettings

"""

import json
from datetime import datetime


VERSION = '2.0.2'


def writesettings():
    """Write settings to json file"""
    settings['LastSave'] = datetime.now().strftime('%d/%m/%y %H:%M:%S')
    with open('settings.json', 'w', encoding='UTF-8') as outfile:
        json.dump(settings, outfile, indent=4, sort_keys=True)


def initialise():
    """Setup the settings structure with default values"""
    isettings = {'LastSave': '01/01/2000 00:00:01',
                 'app-name': 'UCL-Tombola-app',
                 'logappname': 'Tombola-Py',
                 'logfilepath': './logs/tombola-app.log',
                 'loglevel': 'INFO',
                 'drum_apikey': '<type-it-here>',
                 'drum_controller': 'http://192.168.0.10/api',
                 'drum_controller_timeout': 0.5,
                 'recording_cadence': 10,
                 'camera_controller1': 'http://192.168.0.20/control',
                 'camera_controller2': 'http://192.168.0.21/control',
                 'camera_controller_timeout': 0.5,
                 'camera_qty': 1,
                 'camera_storage': 'sda1',
                 'camera_format': 'x264',
                 'sensor_debounce_time': 0.1}
    return isettings


def readsettings():
    """Read the json file"""
    try:
        with open('settings.json', encoding='UTF-8') as json_file:
            jsettings = json.load(json_file)
            return jsettings
    except FileNotFoundError:
        print('File not found')
        return {}


def loadsettings():
    """Replace the default settings with thsoe from the json files"""
    global settings
    settingschanged = 0
    fsettings = readsettings()
    for item in settings.keys():
        try:
            settings[item] = fsettings[item]
        except KeyError:
            print(f'settings[{item}] Not found in json file using default')
            settingschanged = 1
    if settingschanged == 1:
        writesettings()


settings = initialise()
loadsettings()
