### PINS ###
STATE1_PIN  = "P8_8"
STATE2_PIN  = "P8_10"
BALLAS_PIN = "P8_12"
RUDDER_PIN  = "P8_14"
MANCTR_PIN = "P8_16"
UNUSED_PIN  = "P8_18"

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
TRIM_PORT = 6677
BUFFER_SIZE = 50
OWN_IP = '192.168.7.3'