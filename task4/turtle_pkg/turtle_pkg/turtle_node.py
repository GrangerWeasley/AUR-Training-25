#!/usr/bin/env python3

import rclpy 
from rclpy.node import Node
from geometry_msgs.msg import Twist
import readchar


class turtle_node(Node):
    def __init__(self):
        super().__init__('turtle_node')
        self.pub1 = self.create_publisher(Twist,'/turtle1/cmd_vel',10)
        self.pub2 = self.create_publisher(Twist,'/turtle2/cmd_vel',10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        

    def timer_callback(self):
        control1 = Twist()
        control2 = Twist()
        key = readchar.readkey() 
        
        #turtle1
        if key == readchar.key.UP:
            control1.linear.x = 2.0
        elif key == readchar.key.DOWN:
            control1.linear.x = -2.0
        if key == readchar.key.LEFT:
            control1.angular.z = 2.0
        elif key == readchar.key.RIGHT:
            control1.angular.z = -2.0

        #turtle2
        if key == 'w':
            control2.linear.x = 2.0
        elif key == 's':
            control2.linear.x = -2.0
        if key == 'a':
            control2.angular.z = 2.0
        elif key == 'd':
            control2.angular.z = -2.0

        if key == 'q':
            exit()

        self.pub1.publish(control1)
        self.pub2.publish(control2)

        
        

def main():
    rclpy.init()
    node = turtle_node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()