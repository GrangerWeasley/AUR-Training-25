#!/usr/bin/env python3

import rclpy 
from rclpy.node import Node


class timer_node(Node):
    def __init__(self):
        super().__init__('timer_node')
        self.timer = self.create_timer(1, self.timer_callback)
        self.count = 10

    def timer_callback(self):
        print(self.count)
        if self.count == 0:
            self.get_logger().info('Time is up!')
            exit()
        self.count -= 1
        

def main():
    rclpy.init()
    node = timer_node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()