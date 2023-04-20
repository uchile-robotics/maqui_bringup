#!/usr/bin/env python
import rospy
import smach
import smach_ros
from smach_ros import IntrospectionServer

#Robot building

from maqui_skills import robot_factory
from uchile_states.misc.states import SleepState
from uchile_states.head.states import  StartFaceTracking, StopTracking
from uchile_states.perception import person_detection
from uchile_states.interaction.states import SpeakGestures, Speak, Hear, Tell, NoiseCheck
from uchile_states.interaction.tablet_states import WaitTouchScreen, ShowWebpage
from uchile_states.perception import shirt
from uchile_states.navigation.move_to import *
from uchile_states.perception import  wait_face_detection

# Utils
import subprocess
from std_msgs.msg import String

class GetInput(smach.State):
    def __init__(self, robot):
        smach.State.__init__(self, outcomes='succeeded', 
                             output_keys=['entered_text'])

    def execute(self, userdata):
        print("Ready to chat \n")
        userdata.entered_text = input("Enter your chat: ")
        if userdata.entered_text == "0": return 'abort'
        return 'succeeded'

class SendChat2GPT(smach.State):
    def __init__(self, robot):
        smach.State.__init__(outcomes=['succeeded','failed','aborted'], 
                             input_keys='entered_input')
    def execute(self, ud):
        text = ud.entered_input
        print("message recieved")
        output = String()
        output.data = text
        publisher = rospy.Publisher('/chatbot/input', String,queue_size=10)
        publisher.publish(output)
        return 'succeeded'

class W84GPT(smach.State):
    def __init__(self, robot):
        smach.State.__init__(outcomes=['succeeded','failed'],  
                             output_keys='response_text')
    def execute(self, ud):
        try:
            response = rospy.wait_for_message("chatbot/output", String, timeout=10)
            ud.response_text = response.data
            return 'succeded'
        except: return 'failed'

class SayResponse(smach.State):
    def __init__(self, robot):
        smach.State.__init__(self, outcomes='succeeded', 
                             input_keys=['response_text'])

    def execute(self, userdata):
        reply = userdata.response_text 
        robot.tts.say_with_gestures(reply)
        return 'succeeded'

class Introduce(smach.State):
    def __init__(self,robot):
        
        smach.State.__init__(self, outcomes=['succeeded'],
                            input_keys=['recognized_name','drink_text'])
    def execute(self, userdata):
        name = userdata.recognized_name
        drink = userdata.drink_text
        robot.tts.say_with_gestures("Hello John.")
        robot.tts.say_with_gestures( name + "has arrived to the party.")
        robot.tts.say_with_gestures(name + "s" +"favourite drink is." + drink)
        return 'succeeded' 





def getInstance(robot):
    """
    - Go To John
    - Introduce Guest to John and John to Guest
    
    if first:
        - Ask the guest to sit down in the coach
            - Pointing to the couch! D: ( need something like point to map point)
        
        - succeeded 

    if second:
        
        - Introduce to first guest

        - Ask the guest to sit down somewhere

        - (Second iteration) if second is older:
            - ask first to stand up and sit down in other place
            - ask second to sit down in the couch

    """
    sm = smach.StateMachine(outcomes=['succeeded','aborted','preempted','failed'])

    with sm:

        #smach.StateMachine.add('TabletStart', WaitTouchScreen(robot,image=None),
            #transitions={
                #'succeeded':'Start',
                #'preempted':'TabletStart'
            #})

        smach.StateMachine.add('Start',SpeakGestures(robot,text="I'm waiting for someone to talk to."),
            transitions={'succeeded':'StartFaceTracking'} )
        
        smach.StateMachine.add('StartFaceTracking', StartFaceTracking(robot),
            transitions={
                'succeeded':'DETECT_PERSON'
            }        )

        smach.StateMachine.add('DETECT_PERSON', wait_face_detection.getInstance(robot, face_size = 60, timeout= 15),
            transitions={ 
                'succeeded' :'INTRODUCE_SELF',
                'aborted'   :'DETECT_PERSON',
                'preempted' :'DETECT_PERSON'
            }
        ) 

        smach.StateMachine.add('INTRODUCE_SELF',SpeakGestures(robot,text="Oh, hello there! ^start(animations/Stand/Gestures/Hey_1) My name is "+robot.name + ", you can ask me anything!"),
            transitions={'succeeded':'SAVE_NAME'})


        smach.StateMachine.add('GetInput', GetInput(robot),
            transitions={
                'succeeded':'SEND_TEXT_2_GPT',
                'failed':'RECOVER',
                'aborted': 'succeeded'
            },

            remapping={
                'entered_input':'entered_input'
            })
        
        smach.StateMachine.add('SEND_TEXT_2_GPT', SendChat2GPT(),
            transitions={
                'succeeded':'SAY_RESPONSE',
            })
        
        smach.StateMachine.add('W84GPT', W84GPT(),
            transitions={
                'succeeded':'SAY_RESPONSE',
            },
            remapping={
                'response_text':'response_text'
            })
        

        smach.StateMachine.add('RECOVER', Speak(robot, text = "Somethign went wrong, ty again."),
            transitions = {
                'succeeded': 'GetInput'
            }
        )

        smach.StateMachine.add('SAY_RESPONSE', SayResponse(robot),
            transitions = {
                'succeeded': 'GetInput'
            }
        )
        

       
        return sm

if __name__ == '__main__':


    rospy.init_node('RECEPTIONIST')
    base_skills = [
        "tts", 
        "audition",
        "marker",
        "tablet",
        "tabletapp",
        "person_detector",
        "facial_features"
        ,"behavior_manager",
        "track_person"]#,
        #"sitting_person_detector"] not sure if we need this

    extra_skills = []
    robot = robot_factory.build( base_skills + extra_skills, core = True)

    sm = getInstance(robot)
    sis = IntrospectionServer('maqui_chat', sm, '/MAQUI_CHAT_SM') #Smach Viewer
    sis.start()
    outcome = sm.execute() # here is where the test begin
    sis.stop()
