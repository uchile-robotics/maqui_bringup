#! /usr/bin/env python

from maqui_skills import robot_factory
import rospy

def main():
	rospy.init_node("personal_information")
	robot = robot_factory.build(["l_arm","r_arm","neck"],core=False)
	robot.check()

	l_arm = [ -1.1152, 0.61666, -1.73647, -0.00920391, 0.889678, 0.279438 ]
	r_arm = [ -0.0536892, -0.167204, 0.474, 1.1014, 0.667248, 0.484183 ]

	robot.l_arm.send_joint_goal(l_arm,0.5,10,False)
	robot.r_arm.send_joint_goal(r_arm,0.5,10,False)
	robot.neck.send_joint_goal(-1.0,0.5)

if __name__ == "__main__":
	main()
