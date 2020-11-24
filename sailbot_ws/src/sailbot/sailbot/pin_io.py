import rclpy
from rclpy.node import Node
import json

#for now, publish simple string
from std_msgs.msg import String




class PinIO(Node):

    def __init__(self):
        super().__init__('pin_io')
        timer_period = 0.5  # seconds
        #create publisher to serial_rc topic
        self.serial_rc_publisher_ = self.create_publisher(String, 'serial_rc', 10)
        self.timer = self.create_timer(timer_period, self.serial_rc_timer_callback)
        #create subcriber to pwm_control topic
        self.subscription = self.create_subscription(
            String,
            'pwm_control',
            self.pwm_control_listener_callback,
            10)
        self.subscription
        #create publisher to airmar_data topic
        self.airmar_data_publisher_ = self.create_publisher(String, 'airmar_data', 10)
        self.timer = self.create_timer(timer_period, self.airmar_data_timer_callback)

    def serial_rc_timer_callback(self):
        msg = String()
        msg.data = check_serial_rc_pins()
        self.serial_rc_publisher_.publish(msg)
        self.get_logger().info('Serial RC publishing: "%s"' % msg.data)

    def pwm_control_listener_callback(self, msg):
        self.get_logger().info('PWM is outputting: "%s"' % msg.data)
        #TODO: format msg?
        output_pwm_pins(msg)

    def airmar_data_timer_callback(self):
        msg = String()
        msg.data = check_airmar_data()
        self.airmar_data_publisher_.publish(msg)
        self.get_logger().info('Airmar data publishing: "%s"' % msg.data)
        
        

def main(args=None):
    rclpy.init(args=args)

    pin_io = PinIO()

    rclpy.spin(pin_io)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    pin_io.destroy_node()
    rclpy.shutdown()

def check_serial_rc_pins(): #collects and returns json of serial rc pin values
    return "not yet implemented"

def output_pwm_pins(valArray): #takes json of pwm values and sets pins appropriately
    print("not yet implemented")

def check_airmar_data(): #collects and returns json of airmar data
    return "not yet implemented"


if __name__ == '__main__':
    main()
