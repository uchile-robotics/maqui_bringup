import sys
import cv2
import numpy as np
#ROS modules
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image,CameraInfo

from std_srvs.srv import Empty



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

        self.rgb_images_pub = rospy.Publisher('top/custom/image_raw',Image,queue_size=1)
        self.depth_images_pub = rospy.Publisher('depth/custom/image_raw',Image,queue_size=1)
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
            self.rgb_top = self.video.subscribeCamera('rgb_t',0,3,11,20)
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

    def publish_image_to_ros(self):
        numpy_image = self.get_rgb()
        ros_image = self.numpyimg_to_rosimg(numpy_image)
        numpy_depth_image = self.get_depth()
        ros_depth_image = self.numpyimg_to_rosimg(numpy_depth_image,encoding="mono16")
        self.rgb_images_pub.publish(ros_image)
        self.depth_images_pub.publish(ros_depth_image)

def main():

    pepper = PepperImagesPublisher("10.72.168.126","9559")
    pepper.subscribe_cameras()
    while not rospy.is_shutdown():
        pepper.publish_image_to_ros()

    

if __name__ == "__main__":
    main()
