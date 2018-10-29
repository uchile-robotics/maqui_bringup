#!/usr/bin/env python  
import qi
import sys
import time
import numpy as np
import rospy
from sensor_msgs.msg import CameraInfo


def main(msg):	
	global motion

	motion.setStiffnesses("Head",1.0)
	motion.setAngles("Head",[0.,0.],0.05)
	#print motion.getAngles("Head",False)
	time.sleep(2)


if __name__=="__main__":
	ip = "127.0.0.1"
	port = "9559"
	session = qi.Session()

	try:
		session.connect("tcp://" + str(ip) + ":" + str(port))
	except RuntimeError:
		print ("Connection Error!")
		sys.exit(1)

	motion =  session.service("ALMotion")
	
	rospy.init_node('head_fix')
	rospy.Subscriber('/maqui/camera/depth/camera_info', CameraInfo, main, queue_size=1)
	rospy.spin()

