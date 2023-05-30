#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import math
from turtlesim.msg import Pose
from std_msgs.msg import Bool
from rospy.exceptions import ROSInterruptException
from turtle_regulation_FyFalina_Gokhool.srv import waypoint as wp
from turtle_regulation_FyFalina_Gokhool.srv import waypointRequest as wpRequest

def set_way_point():
        global turtlePose, waypoint
        turtlePose = None
        rospy.init_node("set_way_point")
        #création du service
        rospy.Service("set_waypoint_service",wp, set_waypoint_service)
        #souscrire au topic "pose" et met à jour la pose
        #de la tortue avec getPose
        rospy.Subscriber("pose",Pose, getPose)

        #définition de waypoint=(7,7)
        waypoint=Pose()
        waypoint.x=7
        waypoint.y=7

        #définition du paramètre privé Kp=constante pour la vitesse angulaire
        Kp = rospy.get_param("~Kp",1.0) #si Kp n'est pas précisé, Kp=1.0

        #définition du paramètre privé Kp=constante pour la vitesse linéaire
        Kpl = rospy.get_param("~Kpl",1.0) #si Kpl n'est pas précisé, Kp=1.0

        #définir le seuil
        distance_tolerance = rospy.get_param("~distance_tolerance",5.0)

        pub = rospy.Publisher("cmd_vel",Twist,queue_size=1)
        pub_is_moving = rospy.Publisher("is_moving",Bool,queue_size=1)
        rate=rospy.Rate(30)

        while not rospy.is_shutdown():
              if (turtlePose != None) :
                    #calcule l'angle de la droite passant par la tortue et le waypoint
                    angle_desire = math.atan2(waypoint.y-turtlePose.y, waypoint.x-turtlePose.x)

                    #calcule l'erreur en cap
                    e=math.atan(math.tan((angle_desire-turtlePose.theta)/2))

                    #Calcule distance euclidienne
                    d_e = math.sqrt(((waypoint.y - turtlePose.y)**2) + ((waypoint.x - turtlePose.x)**2))
                    #l'erreur linéaire el est la distance entre la tortue et le>
                    el = d_e

                    #Calcule u : la commande en cap
                    u = Kp*e

                    #Calcule v: la commande linéaire
                    v = Kpl * el

                    cmd=Twist()
                    cmd.linear.x=v
                    cmd.angular.z=u

                    if (el > distance_tolerance):
                          pub_is_moving.publish(True)
                    else:
                          #Publier un cmd_vel
                          pub.publish(cmd)
                          pub_is_moving.publish(False)
                    rate.sleep()

#prend la position de la tortue en temps réel
def getPose(pose):
        global turtlePose
        turtlePose=pose

def set_waypoint_service(req):
       global waypoint
       #mettre à jour la valeur de waypoint
       waypoint.x = req.x.data
       waypoint.y = req.y.data

       #réponse du service
       res = Bool()
       res.data = True

       return res
       
 def service_client(x,y):
       # Créer le client pour le service
       rospy.wait_for_service("set_waypoint_service")
       try:
          set_waypoint_client = rospy.ServiceProxy("set_waypoint_service", wp)

          # Vérifier si la tortue est en mouvement
          is_moving = False
          while not rospy.is_shutdown() and not is_moving:
              # Votre condition pour vérifier si la tortue est en mouvement
              is_moving = True  # Mettez votre condition ici
              rospy.sleep(1)

          # Effectuer les appels au service
          if not is_moving:
              # Premier appel au service
              req1 = wpRequest()
              req1.x.data = 10
              req1.y.data = 10
              set_waypoint_client(req1)

              # Deuxième appel au service
              req2 = wpRequest()
              req2.x.data = 5
              req2.y.data = 5
              set_waypoint_client(req2)

              # Troisième appel au service
              req3 = wpRequest()
              req3.x.data = 3
              req3.y.data = 3
              set_waypoint_client(req3)

       except rospy.ServiceException as e:
         print("Service call failed:", str(e))


if __name__=="__main__":
        try:
                set_way_point()
        except ROSInterruptException:
                pass
