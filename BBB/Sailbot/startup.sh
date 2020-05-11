#!/bin/sh

# This has not been tested sinse the switch to Python3, so this might take some adjustments, but ultimately this is whatever you end up putting into the command window to start the modules.

python3 -m PWMSystems.PWM_IO &
python3 -m PWMSystems.SensorReader &
python3 -m TrimTab.trimComms &
python3 -m webserver.webserver &