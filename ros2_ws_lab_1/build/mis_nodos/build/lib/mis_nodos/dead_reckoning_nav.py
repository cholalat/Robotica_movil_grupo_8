import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import math


class DeadReckoningNav(Node):
    def __init__(self):
        super().__init__('dead_reckoning_nav_node')
        self.i = 0
        self.pos_actual = [0, 0]
        self.orientacion_actual = 0

        self.movimiento_siguiente = []

        self.angulo_actual = 0

        self.publisher_ = self.create_publisher(Twist, "/commands/velocity", 10)

        self.subscription = self.create_subscription(
            String, 'goal_list', self.accion_mover_cb, 10)




    def aplicar_velocidad(self, speed_command_list): #mandar velocidades y angulos al robot
        msg = Twist()
        msg.linear.x = speed_command_list[0]
        msg.angular.z = speed_command_list[1]
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg)
        self.i += 1


    def mover_robot_a_destino(self, goal_pose): #Angulos y velocidades para llegar al punto
        vel_lineal = 0.2
        vel_angular = 1

        coordenada_1 = goal_pose[0]
        coordenada_2 = goal_pose[1]
        coordenada_3 = goal_pose[2]

        tiempo_1 = coordenada_1/ vel_lineal
        tiempo_2 = coordenada_2/ vel_lineal
        tiempo_3 = coordenada_3/ vel_angular

        self.aplicar_velocidad([coordenada_1, 0,tiempo_1]) 
        self.aplicar_velocidad([0, coordenada_3,tiempo_3])
        self.aplicar_velocidad([coordenada_2, 0,tiempo_2])




        #aplicar_velocidad(destino)
            



    def accion_mover_cb(self, list_msg): #puntos
        
        for msg in list_msg:

            self.mover_robot_a_destino(msg)

#keyboard teleop