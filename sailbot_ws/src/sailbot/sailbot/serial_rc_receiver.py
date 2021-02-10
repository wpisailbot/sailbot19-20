import serial
import json

import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class SerialRCReceiver(Node):

    def __init__(self):
        super().__init__('serial_rc_receiver')
        self.serial = serial.Serial() #TODO
        self.publisher_ = self.create_publisher(String, 'serial_rc', 10)
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)


    def timer_callback(self):
        msg = String()
        msg.data = json.dumps(readLineToJson())
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)

    def readLineToJson(self):

        line = self.serial.readline()
        #TODO
        return {}
    

def main(args=None):
    rclpy.init(args=args)

    serial_rc_receiver = SerialRCReceiver()

    rclpy.spin(serial_rc_receiver)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    serial_rc_receiver.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
