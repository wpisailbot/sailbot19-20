import rclpy
from rclpy.node import Node
import json
from std_msgs.msg import String


class ControlSystem(Node):

    def __init__(self):
        super().__init__('control_system')
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
        
        #create publisher to pwm_control
        self.pwm_control_publisher_ = self.create_publisher(String, 'pwm_control', 10)

        #create publisher to teensy_control
        self.teensy_control_publisher_ = self.create_publisher(String, 'teensy_control', 10)

        #create instance vars for subscribed topics to update
        self.serial_rc = ""
        self.airmar_data = ""
        self.teensy_status = ""
        

    def serial_rc_listener_callback(self, msg):
        self.get_logger().info('Received msg: "%s"' % msg.data)
        self.serial_rc = msg
        
    def airmar_data_listener_callback(self, msg):
        self.get_logger().info('Received msg: "%s"' % msg.data)
        self.airmar_data = msg
        
    def teensy_status_listener_callback(self, msg):
        self.get_logger().info('Received msg: "%s"' % msg.data)
        self.teensy_status = msg
        

def main(args=None):
    rclpy.init(args=args)

    control_system = ControlSystem()

    while( rclpy.ok() ):
        print("test")
        rclpy.spin_once(control_system, timeout_sec=2)
        # now we have new vals from subscribers in:
        # control_system.serial_rc
        # control_system.airmar_data
        # control_system.teensy_status

        # need to publish new values to both control topics based on new values
        # control_system.pwm_control_publisher_.publish()
        # control_system.teensy_control_publisher_.publish()

        #TODO ^^implement

        json_str = json.dumps({"channel":10,"angle":30})
        print(json_str)
        message = String()
        message.data = json_str
        control_system.pwm_control_publisher_.publish(message)
        
    

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    control_system.destroy_node()
    rclpy.shutdown()




if __name__ == '__main__':
    main()
