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


class Shirt2Color(smach.State):
    def __init__(self,robot):
        
        smach.State.__init__(self, outcomes=['succeeded'],
                            input_keys=['tshirts', 'recognized_sentence'])
        self._pd = robot.get("tts")
    def execute(self, userdata):
        tshirts = userdata.tshirts
        for key in tshirts:
            if tshirts[key]:
                print("color: " + key)
                print(userdata.recognized_sentence)
                robot.tts.say_with_gestures(userdata.recognized_sentence + ",what a beautifull name.")
                robot.tts.say_with_gestures("wow" + userdata.recognized_sentence + "you look stunning today, i love your " + key + "shirt, that is my favourite colour ")
                robot.behavior_manager.run_behavior("animations/Stand/Waiting/LoveYou_1")
        return 'succeeded'

def getInstance(robot):

    sm = smach.StateMachine(outcomes=['succeeded','aborted'])
    sm.userdata.test_data = "data"
    with sm:

        smach.StateMachine.add('TabletStart', WaitTouchScreen(robot,image=None),
            transitions={
                'succeeded':'Photo',
                'preempted':'TabletStart'
            })
        smach.StateMachine.add('Photo',ShowWebpage(robot,page="https://",timeout=10),
            transitions={
                'succeeded':'succeeded',
                'preempted':'Photo'
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
