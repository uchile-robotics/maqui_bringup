#! /usr/bin/env python
from maqui_skills import robot_factory
import rospy



def main():
    rospy.init_node("personal_information")
    robot = robot_factory.build(["basic_motion","l_arm","r_arm","neck","tts","behavior_manager","tablet","basic_awareness"],core=False)
    robot.check()


    # self.tablet.init_touch(image = "")
 #    self.tablet.wait_touch(timeout = 0)
    robot.tts.set_gestures_mode(1)
    robot.neck.home()
    
    robot.basic_awareness.active_stimulus(["People","Touch","TabletTouch","Sound","Movement"])
    
    robot.tts.set_speed(95)
    
    robot.basic_awareness.start()
    
    robot.basic_motion.wake_up()

    robot.behavior_manager.run_behavior("animations/Stand/Waiting/WakeUp_1")

    robot.behavior_manager.run_behavior("animations/Stand/Waiting/ScratchEye_1")

    raw_input("Press enter to Continue")
    robot.tts.say_with_gestures("^start(animations/Stand/Gestures/Hey_1) Hello Everyone, how are you? \\pau=800\\  I am Maqui! \\pau=800\\  ^wait(animations/Stand/Gestures/Hey_1) The Team U Chile Homebreakers welcomes you to our Robotics Lab  ") 
    
    raw_input("Press enter to Continue")
    robot.tts.say_with_gestures("^start(animations/Stand/Stand/Gestures/Surprised_1) you are from the Colegio D 84 of Capacitacion Laboral from Santiago right?^wait(animations/Stand/Stand/Gestures/Surprised_1) ")
    
    raw_input("Press enter to Continue")
    robot.behavior_manager.run_behavior("animations/Stand/Emotions/Positive/Laugh_3")

    robot.tts.say_with_gestures("  I have been waiting to meet you for a  ^start(animations/Stand/Gestures/Far_1) \\pau=1000\\ very looong time ^wait(animations/Stand/Gestures/Far_1) ")

    raw_input("Press enter to Continue")

    robot.tts.say_with_gestures(" ^start(animations/Stand/Emotions/Positive/Excited_1) I am very excited that you are visiting me \\pau=800\\   ^wait(animations/Stand/Emotions/Positive/Excited_1) ") 

    raw_input("Press enter to Continue")

    robot.tts.say_with_gestures(" As you can see I am a humanoid robot ^start(animations/Stand/Waiting/Robot_1) ^wait(animations/Stand/Waiting/Robot_1) And i am here in Chile working with the guys in the robotics lab of the Electrical Engineering Department") 

    raw_input("Press enter to Continue")

    robot.tts.say_with_gestures(" Now my friends Lukas , Jose and Enammuel will tell you more of me and the people who works in the laboratory")

    robot.behavior_manager.run_behavior("animations/Stand/Waiting/LoveYou_1")

    raw_input("Press enter to Continue")

    l_arm = [ -1.1152, 0.61666, -1.73647, -0.00920391, 0.889678, 0.279438 ]
    r_arm = [ -0.0536892, -0.167204, 0.474, 1.1014, 0.667248, 0.484183 ]

    robot.l_arm.send_joint_goal(l_arm,0.5,10,False)
    robot.r_arm.send_joint_goal(r_arm,0.5,10,False)
    robot.neck.send_joint_goal(-1.0,0.5)

if __name__ == "__main__":
    main()
