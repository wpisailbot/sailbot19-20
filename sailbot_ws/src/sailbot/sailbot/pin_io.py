import rclpy
from rclpy.node import Node

#for now, publish simple string
from std_msgs.msg import String


class PinIO(Node):

    def __init__(self):
        super().__init__('pin_io')
        #create publisher to serial_rc topic
        self.publisher_ = self.create_publisher(String, 'serial_rc', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Fake pin output: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    pin_io = PinIO()

    rclpy.spin(pin_io)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
