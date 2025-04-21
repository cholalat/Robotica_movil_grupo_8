import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from geometry_msgs.msg import Vector3


class ObstacleDetector(Node):
    def __init__(self):
        super().__init__('obstacle_detector_node')


        self.vector_de_obstaculos = [0,0,0]

        self.publisher = self.create_publisher(Vector3, "/occupancy_state", 10)

        self.subscription = self.create_subscription(
            Image, 'camera/depth/image_raw', self.procesar_imagen, 10)
        

        self.bridge = CvBridge()


    def procesar_imagen(self, imagen):
        # print(imagen)
        print("Ejecutando")






def main(args=None):
    print("Corriendo una media maraton")
    rclpy.init(args=args)
    node = ObstacleDetector()

    rclpy.spin(node)
    
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
