import rclpy
from rclpy.node import Node
import socket
import json
import requests

from std_msgs.msg import String

# Website URL #
url = '192.168.17.18:3000'

class DebugInterface(Node):

    def __init__(self):
        super().__init__('debug_interface')
        #create subcription to serial_rc topic
        self.serial_rc_subscription = self.create_subscription(
            String,
            'serial_rc',
            self.serial_rc_listener_callback,
            10)
        self.serial_rc_subscription
        
        #create subscription to airmar_data
        self.airmar_data_subscription = self.create_subscription(
            String,
            'airmar_data',
            self.airmar_data_listener_callback,
            10)
        self.airmar_data_subscription
        
        #create subscription to teensy_status
        self.teensy_status_subscription = self.create_subscription(
            String,
            'teensy_status',
            self.teensy_status_listener_callback,
            10)
        self.teensy_status_subscription
        

        #create instance vars for subscribed topics to update
        self.serial_rc = ""
        self.airmar_data = ""
        self.teensy_status = ""
        

    def serial_rc_listener_callback(self, msg):
        self.get_logger().info('Serial msg: "%s"' % msg.data)
        self.serial_rc = msg
        
    def airmar_data_listener_callback(self, msg):
        self.get_logger().info('Airmar data: "%s"' % msg.data)
        self.airmar_data = msg
        requests.post(url, json = msg.data)
        
    def teensy_status_listener_callback(self, msg):
        self.get_logger().info('Teensy msg: "%s"' % msg.data)
        self.teensy_status = msg
        

def main(args=None):
    rclpy.init(args=args)

    debug_interface = DebugInterface()

    while( rclpy.ok() ):
        rclpy.spin_once(debug_interface)
        # now we have new vals from subscribers in:
        # control_system.serial_rc
        # control_system.airmar_data
        # control_system.teensy_status

        # need to publish new values to both control topics based on new values
        # control_system.pwm_control_publisher_.publish()
        # control_system.teensy_control_publisher_.publish()

        #TODO ^^implement
        
        
    

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    debug_interface.destroy_node()
    rclpy.shutdown()




if __name__ == '__main__':
    main()
