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


    #raw_input("Press enter to Continue")
    robot.tts.say_with_gestures("Hola que tal tia kei ^start(animations/Stand/Gestures/Hey_1) \\pau=800\\ me conto un pajarito por ahi que hoy era tu aniversario de nacimiento") 
    
    #raw_input("Press enter to Continue")
    robot.tts.say_with_gestures("^start(animations/Stand/Stand/Gestures/Surprised_1) Soy una gran fanatica de esas fechas, y me gusta mucho celebrarlos")
    
    #raw_input("Press enter to Continue")
    

    #obot.tts.say_with_gestures("  He querido conocerles por un laaargo tiempo y me apena no poder verte hoy ")

    #raw_input("Press enter to Continue")

    robot.tts.say_with_gestures(" Pese a que no estare contigo para celebrarlo \\pau=800\\ quiero mandarte un saludo y un beso roboticos") 

    #raw_input("Press enter to Continue")

    robot.tts.say_with_gestures(" ^start(animations/Stand/Waiting/Robot_1) ^wait(animations/Stand/Waiting/Robot_1) ") 

    #raw_input("Press enter to Continue")

    #robot.tts.say_with_gestures(" Ahora, mis amigos les contaran un poco mas sobre el trabajo que se realiza en el laboratorio y les presentaran a mis hermanos Bender, Jaime y los queridos Naos")

    robot.behavior_manager.run_behavior("animations/Stand/Waiting/LoveYou_1")

#    raw_input("Press enter to Continue")

    l_arm = [ -1.1152, 0.61666, -1.73647, -0.00920391, 0.889678, 0.279438 ]
    r_arm = [ -0.0536892, -0.167204, 0.474, 1.1014, 0.667248, 0.484183 ]

    #robot.l_arm.send_joint_goal(l_arm,0.5,10,False)
    #robot.r_arm.send_joint_goal(r_arm,0.5,10,False)
    #robot.neck.send_joint_goal(-1.0,0.5)
    #robot.behavior_manager.run_behavior("animations/Stand/Gestures/Hey_2")
    
if __name__ == "__main__":
    main()
