import serial
import logger as LOG

class Maretron:
    
    def __init__(self):
        try:
            # Port is only available when something is plugged into the USB A port
            self.usb_port = serial.Serial(port="/dev/ttyUSB0", baudrate = 9600, timeout = 10)
            LOG.LOG_I("Maretron is ready!")
        except:
            # LOG.LOG_E("USB Port not available")
            pass
    
    def read_usb(self):
        try:
            LOG.LOG_D(self.usb_port.read())
        except:
            # LOG.LOG_E("USB Port not available")
            pass
        