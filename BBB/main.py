import maretron as Maretron
import messenger as Messenger
import PWM_read as PWMReader
import logger as LOG

maretron = Maretron.Maretron()
Messenger.init()


def loop():
    ## Try implementing async
    # get data
    # process data
    # communicate
    maretron.read_usb()
    Messenger.serve()

def cleanup():
    Messenger.cleanup()

try:
    while True:
        loop()
except KeyboardInterrupt:
    LOG.LOG_I("Keyboard Interrupt")
    cleanup()