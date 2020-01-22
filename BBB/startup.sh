#!/bin/sh
python main.py &
python web_server.py &
python teensy_server.py &