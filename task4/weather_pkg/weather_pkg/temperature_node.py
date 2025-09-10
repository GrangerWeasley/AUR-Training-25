#!/usr/bin/env python3

import rclpy 
from rclpy.node import Node
from std_msgs.msg import Int32
import random

class temperature_node(Node):
    def __init__(self):
        super().__init__('temperature_node')
        self.publisher_ = self.create_publisher(Int32,'temperature',10)
        self.timer = self.create_timer(1, self.timer_callback)
        

    def timer_callback(self):
        msg = Int32()
        msg.data = random.randint(10,40) 
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data} ')
        
        

def main():
    rclpy.init()
    node = temperature_node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()