#!/bin/sh

python -m PWMRead.PWMRead &
# python -m Rudders.rudderControl &
python -m TrimTab.trimComms &
python -m main.py &