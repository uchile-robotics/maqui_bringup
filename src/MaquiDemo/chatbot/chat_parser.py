#!/usr/bin/env python3.9
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class speech_manager():
    def __init__(self):
        self.subscriber = rospy.Subscriber('/maqui/speech_recognition/input', String, self._callback)
        self.publisher = rospy.Publisher('/maqui/speech_recognition/output', String , queue_size=10)

    def _callback(self, msg):
        self.publisher.publish(msg)

def main():
    rospy.init_node('speech_manager')
    speech_manager()
    rospy.spin()

if __name__ == '__main__':
    main()