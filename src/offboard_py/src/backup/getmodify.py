#!/usr/bin/env python

import rospy
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Float32MultiArray
from calculate import backupcontroller

cb = 5
beta = 0.1
dx, dy, dz, hx, hy, hz, hvx, hvy, x, y, z = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

def getdata(data):
    global hx, hy, hz, hvx, hvy, x, y, z
    # Loop over all models in the message
    idx = data.name.index("husky")
    idx1 = data.name.index("iris")

    # Print the position of each model
    hx = data.pose[idx].position.x
    hy = data.pose[idx].position.y
    hz = data.pose[idx].position.z
    hvx = data.twist[idx].linear.x
    hvy = data.twist[idx].linear.y
    #print("Position of husky : x={:.2f}, y={:.2f}, z={:.2f}, hx={:.2f}, hy={:.2f}".format(hx, hy, hz, hvx, hvy))
        
    # Print the position of each model
    x = data.pose[idx1].position.x
    y = data.pose[idx1].position.y
    z = data.pose[idx1].position.z
    #print("Position of iris : x={:.2f}, y={:.2f}, z={:.2f}".format(x, y, z))
       
    return hx, hy, hz, hvx, hvy, x, y, z

# Define callback function to handle incoming messages
def input_callback(msg):
    global dx, dy, dz
    linear = msg.data
    dx, dy, dz = linear[0], linear[1], linear[2]
    return dx, dy, dz

# Initialize ROS node and subscriber
rospy.init_node('keyboard_input_subscriber')
rospy.Subscriber('/keyboard_input', Float32MultiArray, input_callback)
rospy.Subscriber("/gazebo/model_states", ModelStates, getdata)
#rospy.init_node("model_position_subscriber")

rospy.spin()

# Loop to print the values
rate = rospy.Rate(100) # 100 Hz
while not rospy.is_shutdown():
    print('dx = {}, dy = {}, dz = {},hx = {}, hy = {}, hz = {}, hvx = {}, hvy = {}, x = {}, y = {}, z = {}'.format(dx, dy, dz))
    print('hx = {}, hy = {}, hz = {}, hvx = {}, hvy = {}'.format(hx, hy, hz, hvx, hvy))
    print('x = {}, y = {}, z = {}'.format(x, y, z))
    print(".................") 
    rate.sleep()
