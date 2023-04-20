#! /usr/bin/env python
from maqui_skills import robot_factory
import rospy

def main(robot):
    frases =["Muchas gracias Ossccar",
    "muy buenos dias Presidenta",
    "Agradezco al Canciyer Heraldo Munioz por la invitacion a este lanzamiento. \\pau=500\\ Los invito a conocer los Anhelos al dos mil treinta.",
    "^start(animations/Stand/Gestures/Hey_2)  \\pau=500\\ Nos vemos el dos mil treinta! \\pau=500\\  ^wait(animations/Stand/Gestures/Hey_2)"]

    robot.tts.set_gestures_mode(1)
    robot.neck.home()
    robot.tts.set_speed(95)
    robot.tablet.show_image("http://198.18.0.1/apps/media/amtc_png.png","#FFFFFF")
    
    raw_input("Press enter to Continue")
    robot.basic_motion.wake_up()
    # robot.behavior_manager.run_behavior("animations/Stand/Waiting/WakeUp_1")
    # robot.behavior_manager.run_behavior("animations/Stand/Waiting/ScratchEye_1")
    # robot.behavior_manager.run_behavior("animations/Stand/Emotions/Positive/Laugh_3")
    # robot.behavior_manager.run_behavior("animations/Stand/Waiting/LoveYou_1")

    for frase in frases:    
        raw_input("Press enter to Continue")
        robot.tts.say_with_gestures(frase) 

    raw_input("Press enter to Continue")
    robot.basic_awareness.active_stimulus(["People","Touch","TabletTouch","Sound","Movement"])
    robot.basic_awareness.start()
if __name__ == "__main__":
    rospy.init_node("personal_information")
    robot = robot_factory.build(["basic_motion","neck","tts","behavior_manager","tablet","basic_awareness"],core=False)
    robot.check()
    main(robot)
