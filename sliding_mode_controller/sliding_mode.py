#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
import time

# Init the node
rospy.init_node('sliding_control')

# Init the publisher
motor = rospy.Publisher('/pendulum/x_controller/command',Float64, queue_size = 10)

#Init the subscriber
theta = [0]*2
x = [0] * 4
def callback(data):
    global theta, x
    x[2] = -data.position[1]
    x[3] = -data.velocity[1]
    x[0] = data.position[0]
    x[1] = data.velocity[0]

rospy.Subscriber('/pendulum/joint_states', JointState, callback)

time.sleep(1.5)

r = rospy.Rate(100)
while not rospy.is_shutdown():
    ## Sliding surface
    s = -0.1*x[0] -0.3*x[1] + 3.1*x[2] + 1.3*x[3]

    ## Check the side you're in
    if s*x[0]>0: k1 = 1
    else: k1 = -1
    if s*x[1]>0: k2 = 0.9
    else: k2 = -1.1
    if s*x[2]>0: k3 = 26
    else: k3 = 20
    if s*x[3]>0: k4 = 4.1
    else: k4 = 3.2


    FORCE = -k1*x[0] -k2*x[1] -k3*x[2] -k4*x[3]
    print('Forza: ', FORCE)
    print('Posizione: ', theta[0])
    print('Velocita: ', theta[1])
    motor.publish(FORCE)
    r.sleep()
