import sys

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QGridLayout
)


class TurtleGUI(Node):

    def __init__(self):
        super().__init__('turtle_gui')

        self.publisher = self.create_publisher(
            String,
            '/turtle_command',
            10
        )

    def send_command(self, command):
        msg = String()
        msg.data = command
        self.publisher.publish(msg)


class MainWindow(QWidget):

    def __init__(self, ros_node):
        super().__init__()

        self.ros_node = ros_node

        self.setWindowTitle('Turtle Control')
        self.setFixedSize(300, 250)

        layout = QGridLayout()

        up_button = QPushButton('↑')
        down_button = QPushButton('↓')
        left_button = QPushButton('←')
        right_button = QPushButton('→')
        reset_button = QPushButton('RESET')

        up_button.clicked.connect(
            lambda: self.ros_node.send_command('up')
        )

        down_button.clicked.connect(
            lambda: self.ros_node.send_command('down')
        )

        left_button.clicked.connect(
            lambda: self.ros_node.send_command('left')
        )

        right_button.clicked.connect(
            lambda: self.ros_node.send_command('right')
        )

        reset_button.clicked.connect(
            lambda: self.ros_node.send_command('reset')
        )

        layout.addWidget(up_button, 0, 1)
        layout.addWidget(left_button, 1, 0)
        layout.addWidget(right_button, 1, 2)
        layout.addWidget(down_button, 2, 1)
        layout.addWidget(reset_button, 3, 1)

        self.setLayout(layout)


def main():
    rclpy.init()

    ros_node = TurtleGUI()

    app = QApplication(sys.argv)

    window = MainWindow(ros_node)
    window.show()

    while rclpy.ok():
        rclpy.spin_once(ros_node, timeout_sec=0.01)
        app.processEvents()

    ros_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()