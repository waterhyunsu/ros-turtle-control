import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_srvs.srv import Empty


class TurtleController(Node):

    def __init__(self):
        super().__init__('turtle_controller')

        self.publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.subscription = self.create_subscription(
            String,
            '/turtle_command',
            self.command_callback,
            10
        )

        self.reset_client = self.create_client(
            Empty,
            '/reset'
        )

    def command_callback(self, msg):
        if msg.data == 'reset':
            self.reset_turtle()
            return

        twist = Twist()

        if msg.data == 'up':
            twist.linear.x = 2.0

        elif msg.data == 'down':
            twist.linear.x = -2.0

        elif msg.data == 'left':
            twist.angular.z = 2.0

        elif msg.data == 'right':
            twist.angular.z = -2.0

        self.publisher.publish(twist)

    def reset_turtle(self):
        if not self.reset_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('/reset service is not available')
            return

        request = Empty.Request()
        self.reset_client.call_async(request)


def main(args=None):
    rclpy.init(args=args)

    node = TurtleController()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()