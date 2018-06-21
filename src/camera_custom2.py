import sys
import cv2
import numpy as np
import os
#ROS modules
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image,CameraInfo

from std_srvs.srv import Empty

from sensor_msgs.msg import CompressedImage
from uchile_srvs.srv import Onoff, OnoffResponse
#Pepper naoqi modules
import qi

class PepperImagesPublisher(object):

	def __init__(self,ip,port): #requires ip and port
		rospy.init_node("pepper_images_publisher")

		#Create NaoQI session
		self.ip = ip 
		self.port = port
		self.session = qi.Session()

		try:
			self.session.connect("tcp://" + self.ip + ":" + str(self.port))
		except RuntimeError:
			print ("Connection Error!")
			sys.exit(1)
		self.cvbridge = CvBridge()
		# Camera
		self.video = self.session.service("ALVideoDevice")
		self.video_subs_list = ['rgb_t_0','rgb_b_0','dep_0']
		print self.video.getSubscribers()

		self.rgb_images_pub = rospy.Publisher('top/custom/image_raw', Image, queue_size=1)
		self.depth_images_pub = rospy.Publisher('depth/custom/image_raw',Image,queue_size=1)
		self.rgb_info_pub =  rospy.Publisher('top/custom/camera_info',CameraInfo,queue_size=1)
		self.depth_info_pub = rospy.Publisher('depth/custom/camera_info',CameraInfo,queue_size=1)
		self.active_service = rospy.Service('/maqui/custom_image/send_images', Onoff, self._send_recognize)

		for sub_name in self.video_subs_list:
			print sub_name, self.video.unsubscribe(sub_name)
		self.already_subscribed_ = False

		# self.rgb_top = self.video.subscribeCamera('rgb_t',0,2,11,20)   #name, idx, resolution, colorspace, fps
		# self.rgb_bottom = self.video.subscribeCamera('rgb_b',1,2,11,20)
		# self.depth = self.video.subscribeCamera('dep',2,1,17,20)
		#print self.video.getSubscribers()

	def __del__(self):
		if self.already_subscribed_:
			self.video.unsubscribe(self.rgb_top)
			self.video.unsubscribe(self.depth)
			self.already_subscribed_ = False

	def unsubscribe(self):
		if self.already_subscribed_:
			self.video.unsubscribe(self.rgb_top)
			self.video.unsubscribe(self.depth)

	def subscribe_cameras(self):
		if self.already_subscribed_:
			return 
		else:
			self.rgb_top = self.video.subscribeCamera('rgb_t',0,2,11,20)
			self.depth = self.video.subscribeCamera('dep',2,1,17,20)
			self.already_subscribed_ = True

	def get_rgb(self): #return current RGB image from camera (top camera)
		if not self.already_subscribed_:
			rospy.logerr("The NAOQi it is not subscribed")
			return
		msg = self.video.getImageRemote(self.rgb_top)
		w = msg[0]
		h = msg[1]
		c = msg[2]
		data = msg[6]
		ba = str(bytearray(data))

		nparr = np.fromstring(ba, np.uint8)
		img_np = nparr.reshape((h,w,c))
		img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

		return img_np

	def get_depth(self): #return current Depth image from camera (Xtion)
		msg = self.video.getImageRemote(self.depth)

		w = msg[0]
		h = msg[1]
		c = msg[2]
		data = msg[6]
		ba = str(bytearray(data))

		nparr = np.fromstring(ba, np.uint16)
		img_np = nparr.reshape((h,w,1))
		#img_np = cv2.cvtself.head_fixColor(img_np, cv2.COLOR_RGB2BGR)

		return img_np

	def numpyimg_to_rosimg(self,npimg,encoding='bgr8'):
		return self.cvbridge.cv2_to_imgmsg(npimg,encoding)

	def FrontInfo(self):
		info = CameraInfo()
		info.header.frame_id = 'CameraTop_optical_frame'
		info.height = 480
		info.width = 640
		info.distortion_model = 'plumb_bob'
		info.D = [-0.0545211535376379, 0.0691973423510287, -0.00241094929163055, -0.00112245009306511, 0.0]
		info.K = [556.845054830986, 0.0, 309.366895338178, 0.0, 555.898679730161, 230.592233628776, 0.0, 0.0, 1.0]
		info.R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
		info.P = [551.589721679688, 0.0, 308.271132841983, 0.0, 0.0, 550.291320800781, 229.20143668168, 0.0, 0.0, 0.0, 1.0, 0.0]
		return info

	def DepthInfo(self):
		info = CameraInfo()
		info.header.frame_id ='CameraDepth_optical_frame'
		info.height = 240
		info.width = 320
		info.distortion_model = 'plumb_bob'
		info.D = [-0.0688388724945936, 0.0697453843669642, 0.00309518737071049, -0.00570486993696543, 0.0]
		info.K = [262.5, 0.0, 159.75, 0.0, 262.5, 119.75, 0.0, 0.0, 1.0]
		info.R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
		info.P = [262.5, 0.0, 159.75, 0.0, 0.0, 262.5, 119.75, 0.0, 0.0, 0.0, 1.0, 0.0]
		return info

	def publish_image_to_ros(self):
		stamp = rospy.Time.now()
		numpy_image = self.get_rgb()
		ros_image = self.numpyimg_to_rosimg(numpy_image)
		ros_image.header.stamp = stamp
		ros_image.header.frame_id = "CameraTop_optical_frame"
		
		front_info = self.FrontInfo()
		front_info.header.stamp = stamp
		numpy_depth_image = self.get_depth()

		ros_depth_image = self.numpyimg_to_rosimg(numpy_depth_image,encoding="mono16")
		ros_depth_image.header.stamp = stamp
		ros_depth_image.header.frame_id = "CameraDepth_optical_frame"
		depth_info = self.DepthInfo()
		depth_info.header.stamp = stamp
		self.rgb_images_pub.publish(ros_image)
		self.rgb_info_pub.publish(front_info)

		self.depth_images_pub.publish(ros_depth_image)
		self.depth_info_pub.publish(depth_info)
	
	def _send_recognize(self, req):
		self.publish_image_to_ros()
		rospy.loginfo('Sending 1 Image')
		return OnoffResponse()


def main():
	pepper = PepperImagesPublisher(os.environ['robot_ip'],"9559")
	pepper.subscribe_cameras()
	rospy.spin()
	

if __name__ == "__main__":
	main()
