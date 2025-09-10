#!/usr/bin/env python3

import rclpy 
from rclpy.node import Node
from std_msgs.msg import Int32


class monitor_node(Node):
    def __init__(self):
        super().__init__('monitor_node')
        self.temp_sub = self.create_subscription(Int32,'temperature',self.temp_callback,10)
        self.humidity_sub = self.create_subscription(Int32,'humidity',self.humidity_callback,10)
        self.pressure_sub= self.create_subscription(Int32,'pressure',self.pressure_callback,10)

        self.temperature = None
        self.humidity = None
        self.pressure = None

        
        

    def temp_callback(self,msg:Int32):
        self.temperature = msg.data
        self.get_logger().info(f'Temp = {self.temperature} °C,' \
        f' Humidity = {self.humidity} %, Pressure = {self.pressure} hPa.')

        with open('data.txt', 'a') as file:
            file.write(f'Temp = {self.temperature} °C,' \
        f' Humidity = {self.humidity} %, Pressure = {self.pressure} hPa.\n')
            
    def humidity_callback(self,msg:Int32):
        self.humidity = msg.data
    def pressure_callback(self,msg:Int32):
        self.pressure = msg.data
        
    
        
        

def main():
    rclpy.init()
    node = monitor_node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()