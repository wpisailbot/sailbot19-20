### PINS ###
HALL_STBD_PIN = "P9_23"
HALL_PORT_PIN = "P9_15"
RUDDER_PIN = "P9_14"
MOV_BAL_PIN = "P9_16"
MOV_BAL_POT_PIN = "P9_27" # Hardware not implemented, code using this pin not implemented


### BOAT VARIABLES ###
MAX_HEEL_ANGLE = 20
RUDDER_MAX_ANGL = 180
RUDDER_MIN_ANGL = 0
MOV_BAL_MAX_ANGL = 180 # This is where the port mangetic switch is
MOV_BAL_MIN_ANGL = 0 # This is where the stbd mangetic switch is
MOV_BAL_MAX_SPEED = 15 # Max speed with which the ballast can move
MOV_BAL_ANGL_TOL = 5

### WIFI VARIABLES ###
TRIM_IP = '192.168.0.25' # Use this with the actual Trim Tab - it has a static IP
# TRIM_IP = '127.168.0.1' # Use this with the simulator
TRIM_PORT = 50000
BUFFER_SIZE = 50
# OWN_IP = '192.168.0.21' # This is the actual boat address
OWN_IP = '192.168.0.14' # This is for local testing. This is whatever address you use to ssh into the board.
# OWN_IP = '192.168.0.3'

OWN_PORT = 50051