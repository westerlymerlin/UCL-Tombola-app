# UCL-tombola-app

## Overview
A data collection application for the Riverbed simulator. This tool facilitates capturing and processing data from a large-scale (1m diameter) drum simulator that models riverbed dynamics using water and cement blocks.
## Hardware Components
### Riverbed Simulator
- 1m diameter drum containing water and cement blocks (simulating riverbed rocks)
- Variable speed control for experimental conditions

### Data Acquisition Equipment
- **High-Speed Camera**: [Chronos 2.1 HD](https://www.krontech.ca/product/chronos-2-1-hd-high-speed-camera/)
    - Captures high-resolution footage of riverbed simulations
    - [Camera API Documentation](https://www.krontech.ca/wp-content/uploads/2020/05/WebAPI_Printout.pdf)

- **Position Tracking**: [Adafruit FT232H Breakout](https://www.adafruit.com/product/2264)
    - USB to GPIO/SPI/I2C interface for precise drum position monitoring
    - Setup Instructions:
        - [Linux](https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/linux)
        - [Windows](https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/windows)

    - [Python Libraries](https://github.com/adafruit/Adafruit_Blinka)

## Documentation
- [Application User Guide](./README.pdf) - Detailed usage instructions
- [Module Documentation](./docs/readme.md) - Technical documentation for Python modules
- [Change Log](./changelog.txt) - History of project updates

## Usage
### Sample Code
See `example.py` for a demonstration of controlling drum speed and recording image sequences.
### Camera Interface
The Camera class provides the following key methods:

| Method | Description |
| --- | --- |
| `start_camera_recording()` | Initiates the camera sensor/recording process |
| `stop_camera_recording()` | Stops the camera sensor/recording process |
| `set_drum_rpm(rpm)` | Sets the desired RPM of the drum |
| `get_drum_rpm()` | Returns the current RPM of the drum |
| `change_setting(setting, value)` | Modifies a saved configuration setting |
| `print_settings_to_console()` | Displays current configuration settings |
## Installation
``` bash
# Clone the repository
git clone https://github.com/your-org/UCL-tombola.git
cd UCL-tombola

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
## License
[GNU GENERAL PUBLIC LICENSE](./LICENCE)
## Contributors
Dr Gary Twinn   
Dr Byron Adams  
Dr Jesse Zondervan  
## Acknowledgments
This project supports research at University College London (UCL).

&nbsp;   
&nbsp;    
&nbsp;  
&nbsp;   
&nbsp;   
&nbsp;   
--------------

#### Copyright (C) 2025 Gary Twinn

This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, either version 3 of the License, or  
(at your option) any later version.  

This program is distributed in the hope that it will be useful,  
but WITHOUT ANY WARRANTY; without even the implied warranty of  
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the  
GNU General Public License for more details.  

You should have received a copy of the GNU General Public License  
along with this program. If not, see <https://www.gnu.org/licenses/>.


Author:  Gary Twinn  
Repository:  [github.com/westerlymerlin](https://github)





