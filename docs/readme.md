# Module Documentation


This document contains the documentation for all the modules in the **UCL-Tombola-app** version 2.0.2 application.

---

## Contents


[app_control](./app_control.md)  
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

[camera_timed](./camera_timed.md)  
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

[example](./example.md)  
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

[logmanager](./logmanager.md)  
Logging Configuration and Management

This module provides centralized logging configuration and management for the application.
Configures logging formats, handlers, and log file management to ensure consistent
logging across all application components.

Features:
    - Standardized log formatting
    - File-based logging with rotation
    - Log level management
    - Thread-safe logging operations

Exports:
    logger: Configured logger instance for use across the application

Usage:
    from logmanager import logger

    logger.info('Operation completed successfully')
    logger.warning('Resource threshold reached')
    logger.error('Failed to complete operation')

Log Format:
    Timestamps, log levels, and contextual information are automatically included
    in each log entry for effective debugging and monitoring.

Log Files:
    Logs are stored with automatic rotation to prevent excessive disk usage
    while maintaining historical records.


---

