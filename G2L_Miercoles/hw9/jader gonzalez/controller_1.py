"""
Ejemplo  de un controlador de un robot tipo supervisor

Este ejemplo actua en una simulación sobre un nodo con DEF llamado cajax. Dicho nodo será trasladado y 
rotado indefinidamente según parametros de la aplicación. 

Se habilta manipulación por teclado para administrar dichos parametros
"""

from controller import Supervisor, Keyboard
import math

supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())

keyboard = Keyboard()
keyboard.enable(timestep)

print("Controlador supervisor iniciado.")

nodo = supervisor.getFromDef("robot")
nodo2 = supervisor.getFromDef("robot2")

if nodo is None:
    print("❌ No se encontró el nodo con DEF 'robot'")
    exit()
if nodo2 is None:
    print("❌ No se encontró el nodo con DEF 'robot2'")
    exit()

# Obtener campos de posición y rotación
posicion = nodo.getField("translation")
orientacion = nodo.getField("rotation")

posicion2 = nodo2.getField("translation")
orientacion2 = nodo2.getField("rotation")

delta = 0.001
delta_r = math.pi / 180
delta2 = 0.001
delta_r2 = math.pi / 180

nueva_rotacion = [0, 1, 0, math.pi / 24]
orientacion.setSFRotation(nueva_rotacion)
orientacion2.setSFRotation(nueva_rotacion)

while supervisor.step(timestep) != -1:
    key = keyboard.getKey()
    if key != -1:

        if key == ord('Q'):
            break
        if key == Keyboard.UP:
            delta += 0.01
        if key == Keyboard.DOWN:
            delta -= 0.01
        if key == Keyboard.LEFT:
            delta_r -= 0.01
        if key == Keyboard.RIGHT:
            delta_r += 0.01

        if key == ord('W'):
            delta2 += 0.01
        if key == ord('S'):
            delta2 -= 0.01
        if key == ord('A'):
            delta_r2 -= 0.01
        if key == ord('D'):
            delta_r2 += 0.01

        posicion_actual = posicion.getSFVec3f()
        posicion_actual[2] = delta

        orientacion_actual = orientacion.getSFRotation()
        orientacion_actual[3] = delta_r

        posicion.setSFVec3f(posicion_actual)
        orientacion.setSFRotation(orientacion_actual)

        distancia_objeto = math.sqrt(
            posicion_actual[0]**2 +
            posicion_actual[1]**2 +
            posicion_actual[2]**2
        )
        print(f" Distancia del objeto: {distancia_objeto:.4f} m")

        posicion_actual2 = posicion2.getSFVec3f()
        posicion_actual2[2] = delta2

        orientacion_actual2 = orientacion2.getSFRotation()
        orientacion_actual2[3] = delta_r2

        posicion2.setSFVec3f(posicion_actual2)
        orientacion2.setSFRotation(orientacion_actual2)

        distancia_objeto2 = math.sqrt(
            posicion_actual2[0]**2 +
            posicion_actual2[1]**2 +
            posicion_actual2[2]**2
        )
        print(f" Distancia del objeto2: {distancia_objeto2:.4f} m")
        
        
        distancia_entre_robots = math.sqrt(
        (posicion_actual2[0] - posicion_actual[0])**2 +
        (posicion_actual2[1] - posicion_actual[1])**2 +
        (posicion_actual2[2] - posicion_actual[2])**2
        )
        print(f" Distancia entre robot y robot2: {distancia_entre_robots:.4f} m")