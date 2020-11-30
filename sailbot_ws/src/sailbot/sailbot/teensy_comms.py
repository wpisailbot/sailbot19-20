import rclpy
from rclpy.node import Node
import socket
import json
from enum import Enum

#for now, publish simple string
from std_msgs.msg import String

### PINS ###
HALL_STBD_PIN = "P9_23"
HALL_PORT_PIN = "P9_15"
RUDDER_PIN = "P9_14"
MOV_BAL_PIN = "P9_16"
MOV_BAL_POT_PIN = "P9_27" # Hardware not implemented, code using this pin not implemented


### BOAT VARIABLES ###
MAX_HEEL_ANGLE = 20 # Max heel angle the boat should ever allow (bigger angle risks capsizing)
RUDDER_MAX_ANGL = 180 # Max angle the rudder should ever move to
RUDDER_MIN_ANGL = 0 # Min angle the rudder should ever move to
MOV_BAL_MAX_ANGL = 180 # This is where the port mangetic switch is
MOV_BAL_MIN_ANGL = 0 # This is where the stbd mangetic switch is
MOV_BAL_MAX_SPEED = 15 # Max speed with which the ballast can move
MOV_BAL_ANGL_TOL = 5 # Tolarance of the movanble ballast angle

### WIFI VARIABLES ###
TRIM_IP = '192.168.0.25' # Use this with the actual Trim Tab - it has a static IP
# TRIM_IP = '127.168.0.1' # Use this with the simulator
TRIM_PORT = 50000
BUFFER_SIZE = 50
# OWN_IP = '192.168.0.21' # This is the actual boat address
OWN_IP = '10.0.2.15' # This is for local testing. This is whatever address you use to ssh into the board.
# OWN_IP = '192.168.0.3' # This is for local testing. This is whatever address you use to ssh into the board.

OWN_PORT = 50051

class TRIM_STATE(int, Enum):
    MAX_LIFT_PORT: int = 0
    MAX_LIFT_STBD: int = 1
    MAX_DRAG_PORT: int = 2
    MAX_DRAG_STBD: int = 3
    MIN_LIFT: int = 4
    MANUAL: int = 5

class TeensyComms(Node):
	
    def __init__(self):
        super().__init__('teensy_comms')
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.s.bind((OWN_IP,TRIM_PORT))
        print("bound")
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()

        #create publisher to teensy status topic
        self.teensy_status_publisher_ = self.create_publisher(String, 'teensy_status', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
	
        #create subscriber to teensy commands topic
        self.subscription = self.create_subscription(
            String,
            'teensy_commands',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def timer_callback(self):
        data = conn.recv(1024)
        if data:
            data = data.decode('utf-8')
            msg = String()
            msg.data = data
            self.teensy_status_publisher_.publish(msg)
            self.get_logger().info('Publishing: "%s"' % msg.data)

    def listener_callback(self, msg):
        self.conn.sendall(msg)

def main(args=None):
    rclpy.init(args=args)

    teensy_comms = TeensyComms()

    rclpy.spin(teensy_comms)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    teensy_comms.destroy_node()
  
    rclpy.shutdown()


if __name__ == '__main__':
    main()
