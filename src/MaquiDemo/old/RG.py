#!/usr/bin/env python
import rospy
import smach
import smach_ros
import os

#Robot building
if os.environ['UCHILE_ROBOT']=="bender":
    from bender_skills import robot_factory
else:
    from maqui_skills import robot_factory
    
# #State Machines
from uchile_states.perception import personal_information
from uchile_states.perception import wait_face_detection

#States
from uchile_states.interaction.states import Speak
from uchile_states.interaction import AnswerQuestion
from uchile_states.head.states import LookFront, LookHome, LookPerson, LookCrowd


class IteratorManager(smach.State):

    def __init__(self,questions_number):
        smach.State.__init__(self, outcomes=['succeeded','aborted','preempted','continue'],
                            output_keys=['input_text'])
        self.it =0
        self.max_times = questions_number
    def execute(self,userdata):

        self.it+=1
        if self.it<=self.max_times:
            userdata.input_text = "Please ask question "+ str(self.it)
            return "continue"

        return "succeeded"

class Iterator(smach.State):

    def __init__(self,ques):
        smach.State.__init__(self, outcomes=['succeeded','aborted','preempted'])
        self.iterator = 3
    def execute(self,userdata):
        if self.iterator ==0:
            return "aborted"
        self.iterator -= 1
        #Audio / Commands / Images
        return "succeeded"

class DefaultInfo(smach.State):

    def __init__(self, robot):
        smach.State.__init__(self, outcomes=['succeeded','aborted','preempted'], io_keys = ['facial_features'])
        self._ai = robot.get("AI")

    def execute(self,userdata):

        self.personal_information  = {'personal_gender': 'male',
                                'personal_age': '25',                                 
                                'personal_phase': 'adult'}
        print self.personal_information
        self._ai.addProperties(self.personal_information)
        return 'succeeded'

def getInstance(robot, questions_number):
    sm = smach.StateMachine(outcomes=['succeeded','aborted','preempted'],
                            input_keys=['features','facial_features'])

    sm.userdata.input_text = ""

    with sm:
        # smach.StateMachine.add('LOOKPERSON',LookPerson(robot),
        #     transitions={
        #         'succeeded':'WAIT_OPERATOR'
        #     }
        # )
        
        # smach.StateMachine.add('WAIT_OPERATOR',wait_face_detection.getInstance(robot),
        #     transitions={
        #         'succeeded':'NOTIFY_OPERATOR'
        #     }
        # )
        # smach.StateMachine.add('NOTIFY_OPERATOR',Speak(robot,text="Hi operator, please look into my eyes, so I can get a good look at you."),
        #     transitions={
        #         'succeeded':'PERSONAL_INFORMATION'
        #     }
        # )

        # smach.StateMachine.add('PERSONAL_INFORMATION',personal_information.getInstance(robot),
        #     transitions={
                
        #         'succeeded': 'NOTIFY_READY',
        #         'aborted'  : 'DEFAULT_INFORMATION',
        #         'preempted': 'DEFAULT_INFORMATION',
        #         'failed'   : 'DEFAULT_INFORMATION'
        #     }
        # )


        # smach.StateMachine.add('DEFAULT_INFORMATION',DefaultInfo(robot),
        #     transitions={
        #         'succeeded':'NOTIFY_READY',
        #         'aborted':'NOTIFY_READY',
        #         'preempted':'NOTIFY_READY'
        #     }
        # )

        # # smach.StateMachine.add('ITERATOR',Iterator(),
        # #     transitions={
        # #         'succeeded':'PERSONAL_INFORMATION',
        # #         'aborted'  :'DEFAULT_INFORMATION'
        # #     }
        # # )


        smach.StateMachine.add('NOTIFY_READY',Speak(robot,text="I am ready to answer your questions"),
            transitions={
                'succeeded':'ITERATOR_MANAGER'})
        
        smach.StateMachine.add('ITERATOR_MANAGER',IteratorManager(questions_number),
            transitions={
                'succeeded':'NOTIFY_END_RIDDLE',
                'continue':'NOTIFY'})
        
        smach.StateMachine.add('NOTIFY',Speak(robot,text=sm.userdata.input_text),
            transitions={
                'succeeded':'ANSWER'})

        smach.StateMachine.add('ANSWER',AnswerQuestion.getInstance(robot),
            transitions={'succeeded' : 'ITERATOR_MANAGER',
                         'preempted' : 'ITERATOR_MANAGER'})
        
        smach.StateMachine.add('NOTIFY_END_RIDDLE',Speak(robot,text="I finished the riddle game"),
            transitions={
                'succeeded':'succeeded'})
        
        return sm


if __name__ == '__main__':

    rospy.init_node('WAIT_OPERATOR')

    #Only for testing 
    robot = robot_factory.build(["tts","AI","audition","neck"], core=False)

    robot.check()
    sm = getInstance(robot,10)
    outcome = sm.execute()
