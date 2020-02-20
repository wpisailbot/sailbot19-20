#!/bin/sh

python -m PWMRead.PWMRead &
python -m TrimTab.trimComms &
python -m main.py &