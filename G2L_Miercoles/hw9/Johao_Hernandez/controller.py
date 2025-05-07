"""
Ejemplo de un controlador de un robot tipo supervisor

Este ejemplo actúa en una simulación con dos nodos con DEF llamados "robot" y "robot1".
El controlador mueve ambos robots y detecta una posible colisión entre ellos,
imprimiendo un mensaje cuando están cerca.
"""

from controller import Supervisor
import math

supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())

#  robots
robot_nodo = supervisor.getFromDef("robot")
robot1_nodo = supervisor.getFromDef("robot1")

if robot_nodo is None or robot1_nodo is None:
    print(" No se encontraron uno o ambos nodos de los robots (robot, robot1)")
else:
    robot_posicion_field = robot_nodo.getField("translation")
    robot1_posicion_field = robot1_nodo.getField("translation")

    delta_robot = [0.01, 0, 0]  
    delta_robot1 = [-0.01, 0, 0] 
    distancia_umbral = 0.15 

    print("Controlador supervisor iniciado")

    while supervisor.step(timestep) != -1:

        robot_posicion = robot_posicion_field.getSFVec3f()
        robot1_posicion = robot1_posicion_field.getSFVec3f()

        distancia = math.sqrt(
            (robot_posicion[0] - robot1_posicion[0]) ** 2 +
            (robot_posicion[1] - robot1_posicion[1]) ** 2 +
            (robot_posicion[2] - robot1_posicion[2]) ** 2
        )

        if distancia < distancia_umbral:
            print(f" ¡Peligro de colisión! Distancia entre robots: {distancia:.3f}")

        robot_posicion[0] += delta_robot[0]
        robot1_posicion[0] += delta_robot1[0]


        robot_posicion_field.setSFVec3f(robot_posicion)
        robot1_posicion_field.setSFVec3f(robot1_posicion)