#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

if __name__ == '__main__':
    rospy.init_node("Publisher")
    rospy.loginfo("Node has started.")

    pub = rospy.Publisher("/turtle1/cmd_vel", Twist,queue_size=10)

    rate = rospy.Rate(2)
    while not rospy.is_shutdown():
        msg = Twist()
        msg.linear.x = 1
        msg.angular.z = 1
        pub.publish(msg)
        rate.sleep()