#!/usr/bin/env python
import rospy
import smach
import smach_ros

from uchile_msgs.msg import SemanticObject
from geometry_msgs.msg import Pose

import tf.transformations as tr


class SavePosition(smach.State):
    # skill_req=['knowledge','navigation']
    def __init__(self,robot,position_name=''):
        smach.State.__init__(self, outcomes  =['succeeded'],input_keys=['position_name'])
        self.robot=robot
        self.position_name = position_name

    def execute(self, userdata):
        if not self.position_name == '':
            position_name = self.position_name
        else:
            position_name = userdata.position_name
        place           = SemanticObject()
        place.id        = position_name
        place.type      = 'map_pose'
        place.frame_id  = 'map'
        place.pose      = self.robot.navigation.where_i_am()
        rot=place.pose.orientation
        rotz=tr.euler_from_quaternion((rot.x,rot.y,rot.z,rot.w))[2]
        (rot.x,rot.y,rot.z,rot.w)=tr.quaternion_from_euler(0,0,rotz)
        place.pose.position.z=0
        print place
        self.robot.knowledge.pose.set(place)
        print place
        return 'succeeded'


class FilterPosestampInMap(smach.State):
    def __init__(self,robot,position_name=''):
        smach.State.__init__(self, outcomes  =['succeeded','aborted'],
            io_keys=['list_posestamped'])
        self._knowledgeskill = robot.get("knowledge")

    def execute(self, userdata):

        list_p = []
        for p in userdata.list_posestamped:
            if self._knowledgeskill.map.is_point_in_map(pose_stamped=p):
                list_p.append(p)
        userdata.list_posestamped = list_p
        if len(userdata.list_posestamped) == 0:
            return "aborted"
        return 'succeeded'


def getInstance(robot):
    sm = smach.StateMachine(outcomes=['succeeded','aborted','preempted'])
    with sm:
        smach.StateMachine.add('SAVE_POSITION',SavePosition(robot,position_name='test'),
            transitions={
                'succeeded':'succeeded'
            }
        )
        
    return sm


if __name__ == '__main__':

    import os
    if os.environ['UCHILE_ROBOT']=="bender":
        from bender_skills import robot_factory
    else:
        from maqui_skills import robot_factory
    
    rospy.init_node('map_states_test')
    # robot
    robot = robot_factory.build(["navigation"], core=False)
    robot.knowledge.pose.load_default_map()

    sm = getInstance(robot)
    outcome = sm.execute()