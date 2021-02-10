import json
import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class PWMController(Node):

    def __init__(self):
        super().__init__('pwm_controller')
        self.subscription = self.create_subscription(
            String,
            'pwm_control',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('PWM command received: "%s"' % msg.data)
        self.execute_pwm(msg)

    def execute_pwm(self, msg):
        json.loads(msg)
        #TODO


def main(args=None):
    rclpy.init(args=args)

    pwm_controller = PWMController()

    rclpy.spin(pwm_controller)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    pwm_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
