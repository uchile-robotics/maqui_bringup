#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import sys
import rospy
from std_msgs.msg import Float32, Float32MultiArray, String
from os import environ


class Indicators(object):
    def __init__(self):
        super(Indicators, self).__init__()

        try:
             # Initialize qi framework.
            connection_url = "tcp://" + environ["robot_ip"] + ":" + environ["robot_port"]
            app = qi.Application(["Indicators", "--qi-url=" + connection_url])
        except RuntimeError:
            print ("Can't connect to Naoqi at ip \"" + environ["robot_ip"] + "\" on port " + environ["robot_port"] +".\n"
                   "Please check your script arguments. Run with -h option for help.")
            sys.exit(1)

        app.start()
        session = app.session

        #Indicators for the battery

        self.battery_service = session.service('ALBattery')
        self.battery_level = Float32(0)
        self.battery_pub = rospy.Publisher('/batterystatus', Float32, queue_size=10)

        #Indicators for the hatch
        
        self.hatch_service = session.service('ALMemory')
        self.hatch_status = Float32(0)
        self.hatch_pub = rospy.Publisher('/hatchstatus', Float32, queue_size=10)

        #Indicators for the Memory

        self.mem_service = session.service('ALSystem')
        self.free_memory = float
        self.total_memory = float
        self.mem_pair = Float32MultiArray()
        self.mem_pub = rospy.Publisher('/memstatus', Float32MultiArray, queue_size=10)
        #Indicators for the IP Adress

        #self.ip_service = session.service('NetworkInfo')
        #self.ip_adress = "Not Found"
        #self.ip_pub = rospy.Publisher('/ipstatus', String, queue_size=10)

        #Indicators for the Autonomous Status

        #self.autolife_service = session.service('ALAutonomousLife')
        #self.current_state = "Off"
        #self.autolife_pub = rospy.Publisher('/autolifestatus', String, queue_size=10)
       
        self.autolife_service = session.service('ALBasicAwareness')
        self.current_state = "False"
        self.autolife_pub = rospy.Publisher('/autolifestatus', String, queue_size=10)

        self.rate = rospy.Rate(1)
              

    def run(self):
        while not rospy.is_shutdown():
            rospy.loginfo('Extracting info')
            try:
                self.free_memory = self.mem_service.freeMemory()
                self.total_memory = self.mem_service.totalMemory()

            except KeyboardInterrupt:
            
                print "Interrupted by user"
                print "Stopping..."

            try:
                rospy.loginfo('Free memory ' + str(self.free_memory) )
                rospy.loginfo('Total memory' + str(self.total_memory) )
                self.mem= [self.free_memory, self.total_memory]
                self.mem_pair.data = self.mem
                self.mem_pub.publish(self.mem_pair)

            except KeyboardInterrupt:
            
                print "Interrupted by user"
                print "Stopping..."

            #try:
            #    self.ip_adress = self.ip_service.ipAdress()
            #    self.ip_pub.publish(self.ip_adress)

            #except KeyboardInterrupt:
            
            #    print "Interrupted by user"
            #    print "Stopping..."

            try:
                self.battery_level.data = self.battery_service.getBatteryCharge()
                self.battery_pub.publish(self.battery_level)
                rospy.loginfo('baterry: ' + str(self.battery_level.data) )

            except KeyboardInterrupt:
            
                print "Interrupted by user"
                print "Stopping..."

            try:
                self.hatch_status.data = self.hatch_service.getData("Device/SubDeviceList/Platform/ILS/Sensor/Value")
                self.hatch_pub.publish((self.hatch_status.data))
                
            except KeyboardInterrupt:
            
                print "Interrupted by user"
                print "Stopping..."
                
            try:
                self.current_state = str(self.autolife_service.isEnabled())
                self.autolife_pub.publish(self.current_state)
                
            except KeyboardInterrupt:
            
                print "Interrupted by user"
                print "Stopping..."

            self.rate.sleep()

def main():
    rospy.init_node('indicators_node')
    rospy.loginfo('Init Indicators Node')
    indi = Indicators()
    indi.run()
    rospy.spin()

if __name__ == '__main__':
    main()