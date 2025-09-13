#!/usr/bin/env python3

import rclpy 
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim_msgs.srv import Spawn, Kill
from turtlesim_msgs.msg import Pose
from std_msgs.msg import Int32
import random
import math


class turtle_chase(Node):
    def __init__(self):
        super().__init__('turtle_chase')
        self.spawn_client = self.create_client(Spawn, '/spawn')
        self.kill_client = self.create_client(Kill, '/kill')

        self.get_logger().info('Waiting for services...')
        self.spawn_client.wait_for_service()
        self.kill_client.wait_for_service()
        self.get_logger().info('Services available!')

        self.publisher = self.create_publisher(Int32,'/score',10)
        self.score = Int32()
        self.score.data = 0
        self.publisher.publish(self.score)

        self.player = Pose()
        self.enemy_positions ={
            'enemy1' : Pose() ,
            'enemy2' : Pose() ,
            'enemy3' : Pose() ,
        }

        self.spawn_enemy( 'enemy1')
        self.spawn_enemy( 'enemy2')
        self.spawn_enemy( 'enemy3')
        self.active_enemies = set(['enemy1', 'enemy2', 'enemy3'])

        self.player_sub = self.create_subscription(Pose , '/turtle1/pose' , self.player_callback, 10) 
        self.enemy1_sub = self.create_subscription(Pose , '/enemy1/pose' , self.enemy1_callback, 10)
        self.enemy2_sub = self.create_subscription(Pose , '/enemy2/pose' , self.enemy2_callback, 10)
        self.enemy3_sub = self.create_subscription(Pose , '/enemy3/pose' , self.enemy3_callback, 10)

        self.timer = self.create_timer(0.1, self.check_collisions)


    def player_callback(self,msg):
        self.player = msg
    def enemy1_callback(self,msg):
        self.enemy_positions['enemy1'] = msg
    def enemy2_callback(self,msg):
        self.enemy_positions['enemy2'] = msg
    def enemy3_callback(self,msg):
        self.enemy_positions['enemy3'] = msg


        

    def check_collisions(self):
        for name, pose in list(self.enemy_positions.items()):
            if name in self.active_enemies and (pose.x != 0 and pose.y != 0):

                if self.find_distance( pose) <= 0.5:
                    self.get_logger().info(f'{name} was hit')
                    self.active_enemies.remove(name)

                    if self.kill_enemy(name):
                        self.get_logger().info(f'{name} killed successfully')
                    else:
                        self.get_logger().error(f'Failed to kill {name}')
                        continue
                    
                    if self.spawn_enemy(name):
                        self.get_logger().info(f'{name} spawned')
                        self.active_enemies.add(name)
                    self.publisher.publish(self.score)
                    break

    def spawn_enemy (self,  name):
        while not self.spawn_client.wait_for_service():
            self.get_logger().info('waiting...')

        self.request = Spawn.Request()
        self.request.y = float(random.randint(1,10))
        self.request.x = float(random.randint(1,10))
        self.request.theta = random.uniform(0.0 , 6.28)
        self.request.name = name

        future = self.spawn_client.call_async(self.request)
        rclpy.spin_until_future_complete(self, future, timeout_sec=0.5)
        self.enemy_positions[name] = Pose()
       
        return True


    def kill_enemy(self,name):
        while not self.kill_client.wait_for_service():
            self.get_logger().info('waiting for kill...')
        
        self.request = Kill.Request()
        self.request.name = name      

        future = self.kill_client.call_async(self.request)
        rclpy.spin_until_future_complete(self, future, timeout_sec=0.5)
        self.score.data += 1

        return True
    
    
            
        

        

    def find_distance(self,pose: Pose):
       distance = math.sqrt(math.pow(self.player.x-pose.x , 2) + math.pow(self.player.y-pose.y,2) )
       return distance

def main():
    rclpy.init()
    node = turtle_chase()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()