import Adafruit_BBIO.GPIO as GPIO

hallPortPin = "P9_23"
hallStbdPin = "P9_15"

GPIO.setup(hallPortPin, GPIO.IN)
GPIO.setup(hallStbdPin, GPIO.IN)

hallPort = GPIO.input(hallPortPin)
hallStbd = GPIO.input(hallStbdPin)