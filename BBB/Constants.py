import comms_pb2 as comms

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

def stringify_proto_flask(proto):
    string = ""
    string = string + "device_id: "
    if(proto.device_id == comms.RIGID_SAIL):
        string = string + "RIGID_SAIL"
    elif(proto.device_id == comms.HERO):
        string = string + "HERO"
    elif(proto.device_id == comms.ARDUINO):
        string = string + "ARDUINO"
    elif(proto.device_id == comms.BBB):
        string = string + "BBB"
    else:
        string = string + "UNKNOWN"

    string = string + "<br/> state: "
    if(proto.state == comms.MIN_LIFT):
        string = string + "MIN_LIFT"
    elif(proto.state == comms.STBD_TACK):
        string = string + "STBD_TACK"
    elif(proto.state == comms.PORT_TACK):
        string = string + "PORT_TACK"
    elif(proto.state == comms.MAX_DRAG_STBD):
        string = string + "MAX_DRAG_STBD"
    elif(proto.state == comms.MAX_DRAG_PORT):
        string = string + "MAX_DRAG_PORT"
    elif(proto.state == comms.MAN_CTRL):
        string = string + "MAN_CTRL"
    else:
        string = string + "UNKNOWN"
    
    string = string + "<br/> curHeelAngle: " + str(proto.curHeelAngle)
    string = string + "<br/> maxHeelAngle: " + str(proto.maxHeelAngle)
    string = string + "<br/> controlAngle: " + str(proto.controlAngle)
    string = string + "<br/> windAngle: " + str(proto.windAngle)
    string = string + "<br/> vIn: " + str(proto.vIn)
    string = string + "<br/> hallPortTrip: " + str(proto.hallPortTrip)
    string = string + "<br/> hallStbdTrip: " + str(proto.hallStbdTrip)

    return string