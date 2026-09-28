import sys
import os
from datetime import datetime

import mysql.connector

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from turtlesim.msg import Pose

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel
)
from PyQt5.QtCore import Qt


class TurtleGUI(Node):

    def __init__(self):
        super().__init__('turtle_gui')

        self.publisher = self.create_publisher(
            String,
            '/turtle_command',
            10
        )

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.pose_subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

    def send_command(self, command):
        msg = String()
        msg.data = command
        self.publisher.publish(msg)

    def pose_callback(self, msg):
        self.x = msg.x
        self.y = msg.y
        self.theta = msg.theta


class MainWindow(QWidget):

    def __init__(self, ros_node):
        super().__init__()

        self.ros_node = ros_node

        # 창
        self.setWindowTitle('Turtle Control')
        self.setFixedSize(300, 250)

        # 제목
        title = QLabel('Turtle Control', self)
        title.setGeometry(0, 10, 300, 25)
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
            }
        """)

        # 방향 버튼
        up_button = QPushButton('↑', self)
        left_button = QPushButton('←', self)
        right_button = QPushButton('→', self)
        down_button = QPushButton('↓', self)

        # 하단 버튼
        reset_button = QPushButton('RESET', self)
        save_button = QPushButton('SAVE', self)

        # 버튼 위치
        up_button.setGeometry(108, 45, 85, 30)
        left_button.setGeometry(17, 82, 85, 30)
        right_button.setGeometry(200, 82, 85, 30)
        down_button.setGeometry(108, 119, 85, 30)

        reset_button.setGeometry(17, 202, 85, 30)
        save_button.setGeometry(200, 202, 85, 30)

        # 방향 버튼 스타일
        direction_style = """
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                border: 1px solid #999999;
                border-radius: 5px;
                background-color: #f5f5f5;
            }

            QPushButton:hover {
                background-color: #e8e8e8;
            }

            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """

        up_button.setStyleSheet(direction_style)
        left_button.setStyleSheet(direction_style)
        right_button.setStyleSheet(direction_style)
        down_button.setStyleSheet(direction_style)

        # RESET
        reset_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                font-weight: bold;
                border: 1px solid #999999;
                border-radius: 5px;
                background-color: #eeeeee;
            }

            QPushButton:hover {
                background-color: #dddddd;
            }

            QPushButton:pressed {
                background-color: #cccccc;
            }
        """)

        # SAVE
        save_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                font-weight: bold;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                background-color: #555555;
            }

            QPushButton:hover {
                background-color: #444444;
            }

            QPushButton:pressed {
                background-color: #333333;
            }
        """)

        # 현재 좌표 표시
        self.position_label = QLabel(self)
        self.position_label.setGeometry(10, 160, 280, 25)
        self.position_label.setAlignment(Qt.AlignCenter)

        self.position_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #333333;
            }
        """)

        # 버튼 연결
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

        save_button.clicked.connect(
            self.save_position
        )

    def update_position(self):
        self.position_label.setText(
            f'X: {self.ros_node.x:.2f}    '
            f'Y: {self.ros_node.y:.2f}    '
            f'θ: {self.ros_node.theta:.2f}'
        )

    def save_position(self):
        conn = mysql.connector.connect(
            user='rosuser',
            password=os.environ['ROS_DB_PASSWORD'],
            host='localhost',
            database='rosdb'
        )

        cursor = conn.cursor()

        sql = """
            INSERT INTO turtlepos (x, y, theta, time)
            VALUES (%s, %s, %s, %s)
        """

        values = (
            self.ros_node.x,
            self.ros_node.y,
            self.ros_node.theta,
            datetime.now()
        )

        cursor.execute(sql, values)

        conn.commit()

        cursor.close()
        conn.close()

        print(
            f'SAVED: x={self.ros_node.x}, '
            f'y={self.ros_node.y}, '
            f'theta={self.ros_node.theta}'
        )


def main():
    rclpy.init()

    ros_node = TurtleGUI()

    app = QApplication(sys.argv)

    window = MainWindow(ros_node)
    window.show()

    while rclpy.ok():
        rclpy.spin_once(ros_node, timeout_sec=0.01)

        # 좌표 실시간 갱신
        window.update_position()

        app.processEvents()

    ros_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()