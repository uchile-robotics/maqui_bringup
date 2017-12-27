#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import sys
import rospy
from std_msgs.msg import  String
from os import environ

class Tablet(object):
    def __init__(self):
        super(Tablet, self).__init__()

        try:
             # Initialize qi framework.
            connection_url = "tcp://" + environ["robot_ip"] + ":" + environ["robot_port"]
            app = qi.Application(["Indicators", "--qi-url=" + connection_url])
        except RuntimeError:
            print ("Can't connect to Naoqi at ip \"" + environ["robot_ip"] + "\" on port " + environ["robot_port"] +".\n"
                   "Please check your script arguments. Run with -h option for help.")
            sys.exit(1)

        app.start()
        
        self.session = app.session


        self.memory = self.robot.session.service("ALMemory")

        self._console_pub = rospy.Publisher('maqui/tablet/console_msg', String, queue_size=10)

        self.error_subscriber = self.memory.subscriber("ALTabletService/error")
        self._error_subscriberID = self.error_subscriber.signal.connect(self.onError_cb)

    
        self._console_pub = rospy.Publisher('maqui/tablet/console_msg', String, queue_size=10)
        self._console_msgID = self.tablet.onConsoleMessage.connect(self.onConsole_msg)

    

        self.rate = rospy.Rate(1)

    def onError_cb(self):
        rospy.logerr("Tablet Error")
        
        pass
        
    def onConsole_msg(self, msg):
        self.console_msg = msg
        rospy.loginfo("Console MSG : " + msg)

        return self._console_msg_pub.publish(self.console_msg)


def main():
    rospy.init_node('tablet')
    rospy.loginfo('tablet Indicators Node')
    indi = Tablet()
    indi.run()
    rospy.spin()

if __name__ == '__main__':
    main()
