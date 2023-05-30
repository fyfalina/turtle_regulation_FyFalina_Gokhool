#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import math
from turtlesim.msg import Pose
from rospy.exceptions import ROSInterruptException

def set_way_point():
        global turtlePose
        turtlePose = None
        rospy.init_node("set_way_point")
        #souscrire au topic "pose" et met à jour la pose
        #de la tortue avec getPose
        rospy.Subscriber("pose",Pose, getPose)

        #définition de waypoint=(7,7)
        waypoint=Pose()
        waypoint.x=7
        waypoint.y=7

        #définition du paramètre privé Kp=constante
        Kp = rospy.get_param("~Kp",1.0) #si Kp n'est pas précisé, Kp=1.0

        pub = rospy.Publisher("cmd_vel",Twist,queue_size=1)
        rate=rospy.Rate(30)

        while not rospy.is_shutdown():
              if (turtlePose != None) :
                    #calcule l'angle de la droite passant par la tortue et le waypoint
                    angle_desire = math.atan2(waypoint.y-turtlePose.y, waypoint.x-turtlePose.x)


                    #calcule l'erreur en cap
                    e=math.atan(math.tan((angle_desire-turtlePose.theta)/2))


                    #Calcule u : la commande en cap
                    u = Kp*e

                    cmd=Twist()
                    cmd.angular.z=u

                    #Publier un cmd_vel  avec u la  vitesse  angulaire en z.
                    pub.publish(cmd)

                    rate.sleep()

#prend la position de la tortue en temps réel
def getPose(pose):
        global turtlePose
        turtlePose=pose

if __name__=="__main__":
        try:
                set_way_point()
        except ROSInterruptException:
                pass
