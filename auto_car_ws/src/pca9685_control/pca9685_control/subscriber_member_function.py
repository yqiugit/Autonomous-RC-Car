# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist

import time
from adafruit_servokit import ServoKit 

global init_throttle, init_steering, maxthr, minthr, maxleft, maxright 

kit = ServoKit(channels=16) 

throttle_pwm=kit.continuous_servo[0]
steering_pwm=kit.servo[1]

throttle_pwm.set_pulse_width_range(1230,2000)
steering_pwm.set_pulse_width_range(1230,1850)

steering_pwm.actuation_range=50

init_throttle=0
init_steering=25
maxthr=1
minthr=-1
maxleft=50
maxright=0

throttle_pwm.throttle=init_throttle
steering_pwm.angle=init_steering

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        throttle=msg.linear.x
        steering=msg.angular.z
        self.get_logger().info('Throttle: "%s"' % throttle)
        self.get_logger().info('Steering: "%s"' % steering)

        throttle, steering = keyboard_scaling(throttle, steering)

        drive_controls(throttle,steering)

def keyboard_scaling(keythr, keystr):
    keystr=(25*keystr)+25
    if(keystr<maxright): keystr=maxright
    if(keystr>maxleft): keystr=maxleft

    if(keythr<minthr): keythr=minthr
    if(keythr>maxthr): keythr=maxthr
    
    return keythr, keystr


def drive_controls(thrnum, strnum):
    throttle_pwm.throttle=thrnum
    steering_pwm.angle=strnum



def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
