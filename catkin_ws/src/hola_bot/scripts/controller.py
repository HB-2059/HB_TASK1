#!/usr/bin/env python3


import rospy

# publishing to /cmd_vel with msg type: Twist
from geometry_msgs.msg import Point ,Twist
# subscribing to /odom with msg type: Odometry
from nav_msgs.msg import Odometry

# for finding sin() cos() 
import math

# Odometry is given as a quaternion, but for the controller we'll need to find the orientaion theta by converting to euler angle
from tf.transformations import euler_from_quaternion

hola_x = 0
hola_y = 0
hola_theta = 0

pi = 3.1415926535897

def odometryCb(msg):
	global hola_x, hola_y, hola_theta
	hola_x = msg.pose.pose.position.x
	hola_y = msg.pose.pose.position.y

	rot_q = msg.pose.pose.orientation
	orientation_list = [rot_q.x, rot_q.y, rot_q.z, rot_q.w]
	(roll,pitch,hola_theta) = euler_from_quaternion(orientation_list)
	
	
	
	
	# Write your code to take the msg and update the three variables

def euclediandistance(goal):
	return (math.sqrt(pow((goal.x - hola_x), 2) + pow((goal.y - hola_y), 2)))

def linearvel(goal):
	return 1 * euclediandistance(goal)

def steering(goal):
	return math.atan2(goal.y - hola_y, goal.x - hola_x)


def angularvel(goal):
	return 2 * (steering(goal) - hola_theta)

# def movetogoal(goal):
		# inc_x = goal.x -hola_x
		# inc_y = goal.y -hola_y

	# vel= Twist()

	# while euclediandistance(goal)>=0.1:
	# 	vel.linear.x=linearvel(goal)
	# 	vel.angular.z=angularvel(goal)

		# angle_to_goal = math.atan2(inc_y, inc_x)

		# if abs(angle_to_goal - hola_theta) > 0.1:
		# 	vel.linear.x = 0.0
		# 	vel.angular.z = 1
		# else:
		# 	vel.linear.x = 1
		# 	vel.angular.z = 0.0

def main():
	rospy.init_node('controller')
	# Initialze Publisher and Subscriber
	# We'll leave this for you to figure out the syntax for
	# initialising publisher and subscriber of cmd_vel and odom respectively
    
	pub = rospy.Publisher('/cmd_vel',Twist, queue_size=10)
	sub = rospy.Subscriber('/odom',Odometry, odometryCb)
	
	
		
	# Declare a Twist message
	vel = Twist()

	rate = rospy.Rate(10)
	# Initialise the required variables to 0
	# <This is explained below>
	vel.linear.x=0
	vel.linear.y=0
	vel.angular.z=0

	x_goals = [1, -1, -1, 1, 0]
	y_goals = [1, 1, -1, -1, 0]
	theta_goals =[ pi/4, 3*pi/4, -3*pi/4, -pi/4, 0]
	goal = Point()
	# goal.x = 1
	# goal.y = 1
	
	for i in range(len(x_goals)):
		goal.x = x_goals[i]
		goal.y = y_goals[i]
		vel= Twist()

		while euclediandistance(goal)>=0.02:
			vel.linear.x=linearvel(goal)
			vel.angular.z=angularvel(goal)
			pub.publish(vel)
			rate.sleep()

		vel.linear.x=0
		vel.angular.z=0
		
		while not abs(pi/4-hola_theta)<=0.04:
			vel.linear.x=0
			vel.angular.z=1
			pub.publish(vel)
			rate.sleep()

		vel.linear.x=0
		vel.angular.z=0
		pub.publish(vel)
		
		
		# For maintaining control loop rate.
		rate = rospy.Rate(100)
		#increment goals
	
	

	# Initialise variables that may be needed for the control loop
	# For ex: x_d, y_d, theta_d (in **meters** and **radians**) for defining desired goal-pose.
	# and also Kp values for the P Controller
	#
	# movetogoal(goal)
	# 
	# Control Loop goes here
	#
	#
	while not rospy.is_shutdown():

		# Find error (in x, y and theta) in global frame
		# the /odom topic is giving pose of the robot in global frame
		# the desired pose is declared above and defined by you in global frame
		# therefore calculate error in global frame

		# (Calculate error in body frame)
		# But for Controller outputs robot velocity in robot_body frame, 
		# i.e. velocity are define is in x, y of the robot frame, 
		# Notice: the direction of z axis says the same in global and body frame
		# therefore the errors will have have to be calculated in body frame.
		# 
		# This is probably the crux of Task 1, figure this out and rest should be fine.

		# Finally implement a P controller 
		# to react to the error with velocities in x, y and theta.

		# Safety Check
		# make sure the velocities are within a range.
		# for now since we are in a simulator and we are not dealing with actual physical limits on the system 
		# we may get away with skipping this step. But it will be very necessary in the long run.
		 
		# inc_x = goal.x -hola_x
		# inc_y = goal.y -hola_y

		# angle_to_goal = math.atan2(inc_y, inc_x)

		# if abs(angle_to_goal - hola_theta) > 0.1:
		# 	vel.linear.x = 0.0
		# 	vel.angular.z = 1
		# else:
		# 	vel.linear.x = 1
		# 	vel.angular.z = 0.0
		# movetogoal(goal)


		pub.publish(vel)
		rate.sleep()



if __name__ == "__main__":
	try:
		main()
	except rospy.ROSInterruptException:
		pass