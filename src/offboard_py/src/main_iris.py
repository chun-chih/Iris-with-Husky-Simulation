#!/usr/bin/env python

import rospy
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import TwistStamped, Twist
from calculate import backupcontroller

cb = 5 
beta = 0.05
dx, dy, dz, hx, hy, hz, hvx, hvy, x, y, z = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
ux = uy = uz = 0
bv = 0.1 #backup velocity
b0v = 0.1

# Initialize publisher
twist_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)

twist = TwistStamped()

# Define callback function to handle incoming messages
def input_callback(msg):
    global dx, dy, dz
    linear = msg.data
    dx, dy, dz = linear[0], linear[1], linear[2]
    return dx, dy, dz

def model_callback(data):
    global hx, hy, hz, hvx, hvy, x, y, z
    # Loop over all models in the message
    idx = data.name.index("husky")
    idx1 = data.name.index("iris")

    # Data of husky
    hx = data.pose[idx].position.x
    hy = data.pose[idx].position.y
    hz = data.pose[idx].position.z
    hvx = data.twist[idx].linear.x
    hvy = data.twist[idx].linear.y
    
        
    # Data of iris
    x = data.pose[idx1].position.x
    y = data.pose[idx1].position.y
    z = data.pose[idx1].position.z

def calculate():
    global ux, uy, uz, distance
    inputdata = [x, y, z, hx, hy, hz, hvx, hvy, cb, beta, dx, dy, dz, bv, b0v]
    ux, uy, uz, distance = backupcontroller(*inputdata)
    twist.twist.linear.x = ux
    twist.twist.linear.y = uy
    twist.twist.linear.z = uz

rospy.init_node("get_all_data")

rospy.Subscriber("/gazebo/model_states", ModelStates, model_callback)
rospy.Subscriber('/keyboard_input', Float32MultiArray, input_callback)

# Loop to print the values
rate = rospy.Rate(200) # 200 Hz
while not rospy.is_shutdown():
    calculate()
    print('dx = {}, dy = {}, dz = {}'.format(dx, dy, dz))
    #print("Position of husky : x={:.2f}, y={:.2f}, z={:.2f}, vx={:.2f}, vy={:.2f}".format(hx, hy, hz, hvx, hvy))
    #print("Position of iris : x={:.2f}, y={:.2f}, z={:.2f}".format(x, y, z))
    print("ux = {:.2f}, uy = {:.2f}, uz = {:.2f}, distance = {:.2f}".format(ux, uy, uz, distance))
    print(".................") 
    twist_pub.publish(twist)
    rate.sleep()