import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class ControlSystem(Node):

    def __init__(self):
        super().__init__('control_system')
        self.subscription = self.create_subscription(
            String,
            'serial_rc',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('Received msg: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    control_system = ControlSystem()

    rclpy.spin(control_system)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
