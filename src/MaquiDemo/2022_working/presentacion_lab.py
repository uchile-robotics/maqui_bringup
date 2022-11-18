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

    robot.tablet.show_image("https://i.ytimg.com/vi/GytgZ0JvQZI/maxresdefault.jpg","#FFFFFF")

    robot.behavior_manager.run_behavior("animations/Stand/Waiting/WakeUp_1")

    robot.behavior_manager.run_behavior("animations/Stand/Waiting/ScratchEye_1")

    #raw_input("Press enter to Continue")
    robot.tts.say_with_gestures("^start(animations/Stand/Gestures/Hey_1) Hola que tal, como se encuentran hoy. \\pau=800\\  Mi nombre es Maqui! \\pau=800\\  ^wait(animations/Stand/Gestures/Hey_1) El equipo U Chile jombreiquers les da la bienvenida al laboratorio de robotica ") 
    
    #raw_input("Press enter to Continue")
    robot.tts.say_with_gestures("^start(animations/Stand/Stand/Gestures/Surprised_1) Vienen a visitarme desde muy lejos,verdad?^wait(animations/Stand/Stand/Gestures/Surprised_1) ")
    
    #raw_input("Press enter to Continue")
    robot.behavior_manager.run_behavior("animations/Stand/Emotions/Positive/Laugh_2")

    robot.tts.say_with_gestures("  He querido conocerles por un laaargo tiempo ^wait(animations/Stand/Gestures/Far_1) ")

    #raw_input("Press enter to Continue")

    robot.tts.say_with_gestures(" ^start(animations/Stand/Emotions/Positive/Excited_1) Estoy muy emocionado que hayan venido a visitarme a mi y a mis amigos Jaime, y Bender \\pau=800\\   ^wait(animations/Stand/Emotions/Positive/Excited_1) ") 

    #raw_input("Press enter to Continue")

    robot.tts.say_with_gestures(" Como pueden ver, soy un robot humanoide ^start(animations/Stand/Waiting/Robot_1) ^wait(animations/Stand/Waiting/Robot_1) Y estoy en Chile trabajando con los chicos y chicas del laboratorio de robotica del departamento de ingenieria electrica") 

    #raw_input("Press enter to Continue")

    robot.tts.say_with_gestures(" Ahora, mis amigos les contaran un poco mas sobre el trabajo que se realiza en el laboratorio y les presentaran a mis hermanos Bender, Jaime y los queridos Naos")

    #robot.behavior_manager.run_behavior("animations/Stand/Waiting/LoveYou_1")

#    raw_input("Press enter to Continue")

    l_arm = [ -1.1152, 0.61666, -1.73647, -0.00920391, 0.889678, 0.279438 ]
    r_arm = [ -0.0536892, -0.167204, 0.474, 1.1014, 0.667248, 0.484183 ]

    #robot.l_arm.send_joint_goal(l_arm,0.5,10,False)
    #robot.r_arm.send_joint_goal(r_arm,0.5,10,False)
    #robot.neck.send_joint_goal(-1.0,0.5)
    robot.behavior_manager.run_behavior("animations/Stand/Gestures/Hey_2")
    
if __name__ == "__main__":
    main()
