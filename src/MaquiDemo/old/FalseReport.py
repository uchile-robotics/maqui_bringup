#!/usr/bin/env python
import os
import rospy
import smach
import smach_ros

from maqui_skills import robot_factory

#States
from uchile_states.interaction.states import Speak
from uchile_states.base.states import RotateState
# # from uchile_states.interaction.states import Tell
from uchile_states.navigation.states import GoState
from uchile_states.misc.states import CodeRunner
from uchile_robocup.SPR import BlindManGame, RiddleGame
from uchile_states.head.states import LookFront, LookHome, LookPerson, LookCrowd
from uchile_states.perception import crowd_information, wait_face_detection, personal_information
from uchile_states.knowledge.report_states import SavePDF

#State Machines
from uchile_states.perception import wait_open_door


class MaquiSetup(smach.State):

    def __init__(self, robot):
        smach.State.__init__(self, outcomes=['succeeded','aborted','preempted'])
        self._reportskill = robot.get("report_generator")

    def execute(self,userdata):
        self._reportskill.start(test = "SPR", team = "UChilePeppers")
        #Audio / Commands / Images
        return "succeeded"


class ReportGenerator(smach.State):

    def __init__(self, robot):
        smach.State.__init__(self, outcomes=['succeeded','aborted','preempted'])
        self._reportskill = robot.get("report_generator")

    def execute(self,userdata):
        #Audio / Commands / Image
        return "succeeded"

class Wait(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded','aborted','preempted'])

    def execute(self,userdata):
        #Audio / Commands / Image
        raw_input("Press Enter Pliss")
        return "succeeded"

def CP(robot):
    sm = smach.StateMachine(outcomes=['succeeded','aborted','preempted'])

    sm.userdata.recognized_sentence = ""
    sm.userdata.features = ['gender','age']

    sm.userdata.input_text = ""

    with sm:

        smach.StateMachine.add('SETUP', MaquiSetup(robot),
             transitions={'succeeded'    :'waitINIT'})

        smach.StateMachine.add('waitINIT', Wait(),
             transitions={'succeeded'    :'WAIT_OPERATOR'})


        smach.StateMachine.add('WAIT_OPERATOR',wait_face_detection.getInstance(robot),
            transitions={
                'succeeded':'PERSONAL_INFORMATION'})
        
        smach.StateMachine.add('PERSONAL_INFORMATION',personal_information.getInstance(robot),
            transitions={
                'succeeded': 'wait1',
                'failed' : 'PERSONAL_INFORMATION',
                'aborted' : 'PERSONAL_INFORMATION',
                'preempted' : 'PERSONAL_INFORMATION'})

        smach.StateMachine.add('wait1', Wait(),
             transitions={'succeeded'    :'WAIT_OPERATOR2'})


        smach.StateMachine.add('WAIT_OPERATOR2',wait_face_detection.getInstance(robot),
            transitions={
                'succeeded':'PERSONAL_INFORMATION2'})

        smach.StateMachine.add('PERSONAL_INFORMATION2',personal_information.getInstance(robot),
            transitions={
                
                'succeeded': 'REPORT',
                'failed' : 'REPORT',
                'aborted' : 'REPORT'})

        smach.StateMachine.add('REPORT', ReportGenerator(robot),
             transitions={'succeeded'    :'PDF'})
       
        
        smach.StateMachine.add('PDF', SavePDF(robot),
             transitions={'succeeded'    :'succeeded'})

        initial_data = smach.UserData()
        sm.set_initial_state(['SETUP'],initial_data)# 
        return sm


def SPR(robot):
    sm = smach.StateMachine(outcomes=['succeeded','aborted','preempted'])

    sm.userdata.recognized_sentence = ""
    sm.userdata.features = ['gender','age','posture']

    sm.userdata.input_text = ""

    with sm:

        smach.StateMachine.add('SETUP', MaquiSetup(robot),
             transitions={'succeeded'    :'waitINIT'})

        smach.StateMachine.add('waitINIT', Wait(),
             transitions={'succeeded'    :'CROWD_INFORMATION'})

        smach.StateMachine.add('CROWD_INFORMATION',crowd_information.getInstance(robot),
            transitions={# <<<<<<< HEAD
                'succeeded': 'wait1',
                'aborted'  : 'aborted',
                'failed'   : 'aborted'})

        smach.StateMachine.add('wait1', Wait(),
             transitions={'succeeded'    :'WAIT_OPERATOR'})

        smach.StateMachine.add('WAIT_OPERATOR',wait_face_detection.getInstance(robot),
            transitions={
                'succeeded':'wait2'})

        smach.StateMachine.add('wait2', Wait(),
             transitions={'succeeded'    :'PERSONAL_INFORMATION'})

        smach.StateMachine.add('PERSONAL_INFORMATION',personal_information.getInstance(robot),
            transitions={
                
                'succeeded': 'REPORT',
                'failed' : 'aborted'})

        smach.StateMachine.add('REPORT', ReportGenerator(robot),
             transitions={'succeeded'    :'PDF'})
       
        smach.StateMachine.add('PDF', SavePDF(robot),
             transitions={'succeeded'    :'succeeded'})

        initial_data = smach.UserData()
        sm.set_initial_state(['SETUP'],initial_data)# 
        return sm

if __name__ == '__main__':

    rospy.init_node('SPR')

    skills_base = [
                    "AI",
                    "report_generator",
                    "facial_features",
                    "person_detector",
                    "knowledge",
                    "tts"]

    skills = skills_base
    robot = robot_factory.build( skills , core=False)
    robot.check()
    sm = CP(robot)
    sis = smach_ros.IntrospectionServer('FR_SM', sm, '/FR')
    sis.start()
    outcome = sm.execute()
    sis.stop()