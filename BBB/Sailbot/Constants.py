### PINS ###
PWM_CH1 = "P8_08"
PWM_CH2 = "P8_10"
PWM_CH3 = "P8_12"
PWM_CH4 = "P8_14"
PWM_CH5 = "P8_16"
PWM_CH6 = "P8_18"

RUDDER_OUT_PIN = "P9_21"
RUDDER_OUT_PIN_STR = "P9_21"

### BOAT VARIABLES ###
MAX_HEEL_ANGLE = 20

### LOGGER COLORS ###
#https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
INFO = '\x1b[7;30;47m'
ERNO = '\x1b[7;30;41m'
WARN = '\x1b[7;33;40m'
FAIL = '\x1b[7;31;47m'
DEBG = '\x1b[7;34;47m'
MESS = '\x1b[7;35;47m'
ENDC = '\x1b[0m'

### WIFI VARIABLES ###
TRIM_IP = '192.168.0.25'
TRIM_PORT = 50000
BUFFER_SIZE = 50
#OWN_IP = '192.168.0.21' # This is the actual boat address
OWN_IP = '192.168.0.14' # This is for local testing. This is whatever address you use to ssh into the board.
OWN_PORT = 50051