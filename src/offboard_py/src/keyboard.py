#!/usr/bin/env python3

# control drone using wasd852 , control husky using uhjkn

import rospy
from geometry_msgs.msg import TwistStamped, Twist
from std_msgs.msg import Header, Float32MultiArray
import sys, termios, tty, select

# Initialize ROS node and publisher
rospy.init_node('keyboard_twist_publisher')
#twist_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)
husky_pub = rospy.Publisher('/husky_velocity_controller/cmd_vel', Twist, queue_size=10)
input_pub = rospy.Publisher('/keyboard_input', Float32MultiArray, queue_size=10)
# Set up TwistStamped message
twist = TwistStamped()
husky = Twist()
twist.header = Header()
input_msg = Float32MultiArray()
dx = dy = dz = hx = hz = 0

# Define function to get keyboard input
def get_keyboard_input():
    global dx, dy, dz, hx, hz
    # Use special keyboard settings to read single characters without waiting for enter key
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        
        # Read keyboard input continuously
        while not rospy.is_shutdown():
            # Check if there is any data available on stdin
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                # Read a single character from the keyboard
                c = sys.stdin.read(1)

                # Create twist message based on keyboard input
                if c == 'w':
                    dx += 0.5
                elif c == 's':
                    dx -= 0.5
                elif c == 'a':
                    dy += 0.5
                elif c == 'd':
                    dy -= 0.5
                elif c == '8':
                    dz += 1
                elif c == '2':
                    dz -= 1
                elif c == '5':
                    dx = dy = dz = 0
                elif c == 'u':
                    hx += 0.5
                    husky.linear.x = hx
                elif c == 'j':
                    hx -= 0.5
                    husky.linear.x = hx
                elif c == 'h':
                    hz += 0.5
                    husky.angular.z = hz
                elif c == 'k':
                    hz -= 0.5
                    husky.angular.z = hz
                elif c == 'n':
                    hx = 0
                    hz = 0
                    husky.linear.x = hx
                    husky.angular.z = hz

            else:
                # No data available on stdin, set twist to current data
                '''twist.twist.linear.x = dx
                twist.twist.linear.y = dy
                twist.twist.linear.z = dz'''
                husky.linear.x = hx
                husky.angular.z = hz
            input_msg.data = [ dx, dy, dz]
            input_pub.publish(input_msg)

            # Sleep briefly to avoid hogging the CPU
            rospy.sleep(0.01)
    finally:
        # Restore normal keyboard settings when done
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

# Start thread to get keyboard input
import threading
input_thread = threading.Thread(target=get_keyboard_input)
input_thread.start()

# Define main loop
rate = rospy.Rate(200) # 200hz
while not rospy.is_shutdown():
    # Publish twist message
    twist.header.stamp = rospy.Time.now()
    #twist_pub.publish(twist)
    husky_pub.publish(husky)
    # Sleep to maintain desired loop rate
    rate.sleep()

# Wait for input thread to finish
input_thread.join()
