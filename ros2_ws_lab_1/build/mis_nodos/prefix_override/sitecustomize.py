import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/paulo/universidad/5to_semestre/robotica_movil/ros2_ws_lab_1/install/mis_nodos'
