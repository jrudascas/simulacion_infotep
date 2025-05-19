from controller import Supervisor
import numpy as np

def rotation_matrix_y(theta):
    """Rotación 3x3 sobre eje Y"""
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([
        [ c, 0, s],
        [ 0, 1, 0],
        [-s, 0, c]
    ])

def homogeneous_matrix(R, t):
    """Devuelve matriz homogénea 4x4"""
    H = np.eye(4)
    H[:3, :3] = R
    H[:3, 3] = t
    return H

# Iniciar supervisor
robot = Supervisor()
timestep = int(robot.getBasicTimeStep())

# Obtener nodos
caja1 = robot.getFromDef("caja1")
caja2 = robot.getFromDef("caja2")

# Constantes
radius_orbit = 0.3   # radio de la órbita de 2 alrededor de 1
angular_speed = 0.5  # radianes por segundo

# Loop principal
while robot.step(timestep) != -1:
    t = robot.getTime()  # tiempo actual en segundos

    # 1. Obtener posición fija de caja 1
    trans_a = np.array(caja1.getField("translation").getSFVec3f())
    H_wa = homogeneous_matrix(np.eye(3), trans_a)

    # 2. Rotación incremental
    theta = angular_speed * t
    R = rotation_matrix_y(theta)

    # 3. Posición relativa de 2 respecto a 1 (en el eje X)
    t_ab = np.array([radius_orbit, 0, 0])
    H_ab = homogeneous_matrix(R, R @ t_ab)

    # 4. Transformar a coordenadas globales
    H_wb = H_wa @ H_ab
    pos_b = H_wb[:3, 3]

    # 5. Aplicar nueva posición a la caja 2
    caja2.getField("translation").setSFVec3f(pos_b.tolist())
