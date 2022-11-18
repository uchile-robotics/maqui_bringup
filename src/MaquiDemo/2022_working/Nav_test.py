#!/usr/bin/env python


__autor__ = "Poppers"
from maqui_skills import robot_factory
from gettext import translation
from re import S
import rospy
import smach
import smach_ros
from uchile_states.interaction.states import SpeakGestures, Speak, Hear, Tell, NoiseCheck
from uchile_states.interaction.tablet_states import WaitTouchScreen, ShowWebpage
from uchile_states.perception import shirt
from uchile_states.navigation.move_to import *

"""
This State Machine receives a recognized text (through the input_keys) and ask for confirmation about it
"""


class NavGo1(smach.State):
    def __init__(self,robot):
        smach.State.__init__(self, outcomes=['succeeded'])
    def execute(self, userdata):
        robot.tts.say_with_gestures("Voy a la primera posicion")
        m = Move()
        x = -0.3029
        y = 1.81
        w = 0.955
        m.set_pose(x,y,w) 
        m.go()
        return 'succeeded'

class NavGo2(smach.State):
    def __init__(self,robot):
        smach.State.__init__(self, outcomes=['succeeded'])
    def execute(self, userdata):
        robot.tts.say_with_gestures("Voy de vuelta al lugar de inicio")
        m = Move()
        x = -1.801
        y = -0.252
        w = 1.501
        m.set_pose(x,y,w) 
        m.go()
        return 'succeeded'

class Say(smach.State):
    def __init__(self,robot):
        smach.State.__init__(self, outcomes=['succeeded'])
    def execute(self, userdata):
        robot.tts.say_with_gestures("He llegado al punto de inicio. Gracias por su atencion")
        robot.behavior_manager.run_behavior("animations/Stand/Gestures/Hey_2")
        return 'succeeded'

def getInstance(robot):

    sm = smach.StateMachine(outcomes=['succeeded','aborted'])
    sm.userdata.test_data = "data"
    with sm:


        smach.StateMachine.add('TabletStart', WaitTouchScreen(robot,image=None),
            transitions={
                'succeeded':'NavGo1',
                'preempted':'TabletStart'
            })


        smach.StateMachine.add('NavGo1', NavGo1(robot),
            transitions={
                'succeeded':'NavGo2'
            }        )


        smach.StateMachine.add('NavGo2', NavGo2(robot),
            transitions={
                'succeeded':'cuzbai'
            }        )

        smach.StateMachine.add('cuzbai', Say(robot),
            transitions={
                'succeeded':'succeeded'
            }        )



    return sm

if __name__ == '__main__':

    import os
    if os.environ['UCHILE_ROBOT']=="bender":
        from bender_skills import robot_factory
    else:
        from maqui_skills import robot_factory

    rospy.init_node('test')
    robot = robot_factory.build(["tts", "audition","tablet","person_detector","basic_motion","l_arm","r_arm","neck","tts","behavior_manager","basic_awareness"], core=False)
    sm = getInstance(robot)
    
    outcome = sm.execute()
