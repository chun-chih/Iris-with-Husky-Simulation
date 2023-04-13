#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32MultiArray


dx, dy, dz = 0, 0, 0

# Define callback function to handle incoming messages
def input_callback(msg):
    global dx, dy, dz
    linear = msg.data
    dx, dy, dz = linear[0], linear[1], linear[2]
    return dx, dy, dz
    
# Initialize ROS node and subscriber
rospy.init_node('keyboard_input_subscriber')
input_sub = rospy.Subscriber('/keyboard_input', Float32MultiArray, input_callback)

# Loop to print the values
'''rate = rospy.Rate(100) # 100 Hz
while not rospy.is_shutdown():
    print('x = {}, y = {}, z = {},'.format(dx, dy, dz))
    rate.sleep()'''

