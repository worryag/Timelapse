# Copyright (c) 2018 Svalov Ivan
# The PostProcessingPlugin is released under the terms of the AGPLv3 or higher.
# Pause at layers and park XY.

import re
from ..Script import Script

class Timelapse(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Time lapse",
            "key": "Timelapse",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "head_park_x":
                {
                    "label": "Park Print Head X",
                    "description": "What X location does the head move to when pausing.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 0
                },
                "head_park_y":
                {
                    "label": "Park Print Head Y",
                    "description": "What Y location does the head move to when pausing.",
                    "unit": "mm",
                    "type": "float",
                    "default_value": 215
                },
                "pause_timelapse":
                {
                    "label": "Pause at layers",
                    "description": "Pause at layers for number of seconds.",
                    "type": "float",
                    "default_value": 1
                }
            }
         }"""

    def execute(self, data):
        parkX = self.getSettingValueByKey("head_park_x")
        parkY = self.getSettingValueByKey("head_park_y")
        PauseTimeLapse = self.getSettingValueByKey("pause_timelapse")
        
        prepend_gcode=";Start script: Timelapse.py\n"
        prepend_gcode+="G0 Y%.1f F9000\n"%(parkY)
        prepend_gcode+="G0 X%.1f F9000\n"%(parkX)
        prepend_gcode+="G4 S%.1f \n"%(PauseTimeLapse)
        prepend_gcode+=";End script: Timelapse.py\n"
        
        pattern = re.compile(r';MESH:.*STL')
        for layer_number, layer in enumerate(data):
            data[layer_number]=re.sub(pattern,prepend_gcode,layer,flags=re.IGNORECASE)
            
        return data
