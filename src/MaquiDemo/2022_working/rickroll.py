#!/usr/bin/env python

__autor__ = "Poppers"

from gettext import translation
from re import S
import rospy
import smach
import smach_ros
from uchile_states.interaction.states import SpeakGestures, Speak, Hear, Tell, NoiseCheck
from uchile_states.interaction.tablet_states import WaitTouchScreen, ShowWebpage
from uchile_states.perception import shirt

"""
This State Machine receives a recognized text (through the input_keys) and ask for confirmation about it
"""


class Dance(smach.State):
    def __init__(self,robot):
        smach.State.__init__(self, outcomes=['succeeded'])
    def execute(self, userdata):
                robot.behavior_manager.run_behavior("poppers_behaviors/rickroll")
                return 'succeeded'



def getInstance(robot):

    sm = smach.StateMachine(outcomes=['succeeded','aborted'])
    sm.userdata.test_data = "data"
    with sm:

        smach.StateMachine.add('Photo',ShowWebpage(robot,page="https://media.revistagq.com/photos/5de7a4615ec41f0008094ed7/16:9/w_2560%2Cc_limit/GettyImages-1149186448.jpg",timeout=10),
            transitions={
                'succeeded':'TabletStart',
                'preempted':'TabletStart'
            }        )

        smach.StateMachine.add('TabletStart', WaitTouchScreen(robot,image=None),
            transitions={
                'succeeded':'speech',
                'preempted':'TabletStart'
            })
        smach.StateMachine.add('speech',SpeakGestures(robot,text=" ^start(animations/Stand/BodyTalk/Speaking/BodyTalk_6) Hola te tengo un regalo, acercate a mi tablet a abrirlo"),
            transitions={'succeeded':'Wait'})

        smach.StateMachine.add('Wait', WaitTouchScreen(robot,image=None),
            transitions={
                'succeeded':'Rick',
                'preempted':'TabletStart'
            })

        smach.StateMachine.add('Rick',ShowWebpage(robot,page="https://pbs.twimg.com/media/CnXcWCSUMAAo04_.jpg",timeout=10),
            transitions={
                'succeeded':'Dance',
                'preempted':'Dance'
            }        )

        smach.StateMachine.add('Dance', Dance(robot),
            transitions={
                'succeeded':'end'
            } )
        smach.StateMachine.add('end',SpeakGestures(robot,text=" ^start(animations/Stand/Emotions/Positive/Laugh_2) \\pau=2500\\ has sido rick roleado, soy todo un trol "),
            transitions={'succeeded':'succeeded'})       



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
