# ultrasonic_publisher.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from ultrasonic import setup_pins, get_distance, cleanup

class UltrasonicPublisher(Node):

    def __init__(self):
        super().__init__('ultrasonic_publisher')
        self.publisher_ = self.create_publisher(Float32, 'ultrasonic_distance', 10)
        self.timer = self.create_timer(1.0, self.publish_distance)  # Publish every second
        self.trigger_pin = 23
        self.echo_pin = 24
        setup_pins(self.trigger_pin, self.echo_pin)

    def publish_distance(self):
        try:
            distance = get_distance(self.trigger_pin, self.echo_pin)
            msg = Float32()
            msg.data = distance
            self.publisher_.publish(msg)
            self.get_logger().info(f'Publishing: {distance} cm')
        except Exception as e:
            self.get_logger().error(f'Error reading distance: {e}')

    def __del__(self):
        cleanup()

def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()