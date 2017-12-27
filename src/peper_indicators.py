#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import sys
import rospy
from std_msgs.msg import Float32, Float32MultiArray, String
from os import environ
import psutil

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

        #Indicators for the Storage

        self.mem_service = session.service('ALSystem')
        self.free_memory = float
        self.total_memory = float
        self.mem_pair = Float32MultiArray()
        self.mem_pub = rospy.Publisher('/memstatus', Float32MultiArray, queue_size=10)
        #Indicators for the IP Adress

        #Indicators for the Autonomous Status

        self.autolife_service = session.service('ALBasicAwareness')
        self.current_state = "Off"
        self.autolife_pub = rospy.Publisher('/autolifestatus', String, queue_size=10)

        #Indicators for the CPU Status

<<<<<<< HEAD
        self.cpu_pub = rospy.Publisher('/cpustatus', Float32, queue_size=10)
        self.cpu_st = float
=======
        self.cpu_st = Float32MultiArray()
        self.cpu_pub = rospy.Publisher('/cpustatus', Float32MultiArray, queue_size=10)
>>>>>>> 2c323a11a02453272faa6f34eeb0a0550069b489

        #Indicators for the Memory Status
 
        self.memory_pub = rospy.Publisher('/memorystatus', Float32MultiArray, queue_size=10)
        self.mem_st = Float32MultiArray()

        #Indicators for the Network Status

        self.network_pub = rospy.Publisher('/Networkstatus', String, queue_size=10)
        self.net_st = ""
       
        #Indicators for the Temperature Status

        self.temp_service = session.service('ALBodyTemperature')
        self.temp_pair = []
        self.temp_status = float
        self.temp_devices = ""
        self.temp_pub_st = rospy.Publisher('/tempstatus', Float32, queue_size=10)
        self.temp_pub_dev = rospy.Publisher('/tempdevicesstatus', String, queue_size=10)

        self.rate = rospy.Rate(1)
              

    def run(self):
        while not rospy.is_shutdown():

            try:
                self.temp_pair = self.temp_service.getTemperatureDiagnosis()
                
                if self.temp_pair is not None:
                    self.temp_status = self.temp_pair[0]
                    s="-"
                    self.temp_devices = s.join(self.temp_pair[1])

                    self.temp_pub_st.publish(self.temp_status)
                    self.temp_pub_dev.publish(self.temp_devices)

            except Exception as e:
                rospy.logerr("Error getting Pepper Devices Temperature: {0}".format(e))

            try:
                self.free_memory = self.mem_service.freeMemory()
                self.total_memory = self.mem_service.totalMemory()

                self.mem= [self.free_memory, self.total_memory]
                self.mem_pair.data = self.mem
                self.mem_pub.publish(self.mem_pair)
            
            except Exception as e:
                rospy.logerr("Error getting Pepper Memory : {0}".format(e))

            try:
                self.battery_level.data = self.battery_service.getBatteryCharge()
                self.battery_pub.publish(self.battery_level)
                rospy.loginfo('baterry: ' + str(self.battery_level.data) )

            except Exception as e:
                rospy.logerr("Error getting Pepper Battery Status : {0}".format(e))

            try:
                self.hatch_status.data = self.hatch_service.getData("Device/SubDeviceList/Platform/ILS/Sensor/Value")
                self.hatch_pub.publish(self.hatch_status)
            except Exception as e:
                rospy.logerr("Error getting Pepper Hatch Status: {0}".format(e))                
                
            try:
                self.current_state = str(self.autolife_service.isEnabled())
                self.autolife_pub.publish(self.current_state)
            except Exception as e:
                rospy.logerr("Error getting Autonomous Life Status : {0}".format(e))
                
            try:

                a = psutil.virtual_memory()

                self.mem_st.data = [a.total, a.available, a.percent]
                if a.percent > 90.0:
                    rospy.logwarn("Maqui Use of Memory has reached 90%")
                self.memory_pub.publish(self.mem_st)

            except Exception as e:
                rospy.logerr("Error getting Virtual Memory: {0}".format(e))

            try:
<<<<<<< HEAD
                self.cpu_st = psutil.cpu_percent(interval=0.0, percpu=False)
=======
                self.cpu_st.data = psutil.cpu_percent(interval=0.0, percpu=True)
>>>>>>> 2c323a11a02453272faa6f34eeb0a0550069b489
                self.cpu_pub.publish(self.cpu_st)
                
            except Exception as e:
                rospy.logerr("Error getting CPU Percent: {0}".format(e))

            try:
                self.net_st = psutil.net_if_stats()
                self.network_pub.publish(str(self.net_st))
                
            except Exception as e:
                rospy.logerr("Error getting NET Status: {0}".format(e))

            self.rate.sleep()

def main():
    rospy.init_node('indicators_node')
    rospy.loginfo('Init Indicators Node')
    indi = Indicators()
    indi.run()
    rospy.spin()

if __name__ == '__main__':
    main()
