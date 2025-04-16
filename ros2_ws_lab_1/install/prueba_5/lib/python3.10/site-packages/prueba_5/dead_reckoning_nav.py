import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32MultiArray
from geometry_msgs.msg import Twist
import math
import time

class DeadReckoningNav(Node):
    def __init__(self):
        super().__init__('dead_reckoning_nav_node')
        self.i = 0

        self.pos_actual_x = 0
        self.pos_actual_y = 0
        self.orientacion_actual = 0

        self.tiempo_actual = time.time()
        tiempo_anterior = time.time()

        self.movimiento_siguiente = []

        self.angulo_actual = 0

        self.publisher_ = self.create_publisher(Twist, "/cmd_vel_mux/input/navigation", 10)

        self.subscription = self.create_subscription(
            Int32MultiArray, 'goal_list', self.accion_mover_cb, 10)




    def aplicar_velocidad(self, speed_command_list): #mandar velocidades y angulos al robot
        msg = Twist()
        msg.linear.x = float(speed_command_list[0])
        msg.angular.z = float(speed_command_list[1])

        print("entre al nodo")
        while abs(time.time() - self.tiempo_actual) < float(speed_command_list[2]):
            self.publisher_.publish(msg)
            print(self.i, msg)
            # self.get_logger().info('Publishing: "%s"' % msg)
            self.i += 1
        self.tiempo_actual = time.time()
        self.publisher_.publish(Twist())


        self.orientacion_actual += speed_command_list[1]
        self.pos_actual_x += speed_command_list[0] * math.cos(self.orientacion_actual)
        self.pos_actual_y += speed_command_list[0] * math.sin(self.orientacion_actual)





    def mover_robot_a_destino(self, goal_pose): #Angulos y velocidades para llegar al punto
        vel_lineal = 0.2
        vel_angular = 1

        coordenada_1 = goal_pose[0]
        coordenada_2 = goal_pose[1]
        angulo_final = goal_pose[2]

        tiempo_1 = coordenada_1/ vel_lineal
        tiempo_2 = coordenada_2/ vel_lineal
        tiempo_3 = angulo_final/ vel_angular

        tiempo_rotacion_correccion = (coordenada_2/abs(coordenada_2)) * ((math.pi/2)/vel_angular)

        print('justo antes de entrar a aplicar velocidad')
        self.aplicar_velocidad([vel_lineal, 0,tiempo_1]) 
        print('justo despues de entrar a aplicar velocidad')

        self.aplicar_velocidad([0, vel_angular,tiempo_rotacion_correccion])

        self.aplicar_velocidad([vel_lineal, 0,tiempo_2])

        self.aplicar_velocidad([0, vel_angular,tiempo_3])



        #aplicar_velocidad(destino)
            



    def accion_mover_cb(self, list_msg): #puntos
        lista_coordenadas = []
        list_msg = list_msg.data

        for i in range(int(len(list_msg)/3)):
            obj1 = list_msg.pop(0)
            obj2 = list_msg.pop(0)
            obj3 = list_msg.pop(0)
            lista = [obj1, obj2, obj3]
            lista_coordenadas.append(lista)

        print('Escuche:' + str(list_msg))

        print(lista_coordenadas)

        for coordenada in lista_coordenadas:
            pass
            self.mover_robot_a_destino(coordenada)


#keyboard teleop





    def orientarse(self, eje):

        if eje == "x":
            while abs(self.orientacion_actual) > 0.1:
                if self.orientacion_actual < 0:
                    self.aplicar_velocidad([0, -1, 0.1])
                else:
                    self.aplicar_velocidad([0, 1, 0.1])

        elif eje == "y":
            while abs(self.orientacion_actual - math.pi/2) > 0.1:
                if self.orientacion_actual < 0:
                    self.aplicar_velocidad([0, -1, 0.1])
                else:
                    self.aplicar_velocidad([0, 1, 0.1])







def main(args=None):
    print("corriendo")
    rclpy.init(args=args)
    node = DeadReckoningNav()

    rclpy.spin(node)
    node.aplicar_velocidad([0, 1, 5])
    rclpy.shutdown()


if __name__ == "__main__":
    main()