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
nombre_objeto1 = "cajax"
nombre_objeto2 = "cajav"

nodo1 = supervisor.getFromDef(nombre_objeto1)
nodo2 = supervisor.getFromDef(nombre_objeto2)

if nodo1 is None or nodo2 is None:
    print("❌ No se encontraron uno o ambos nodos con DEF especificados")
    exit()

# Obtener campos de posición y orientación
posicion1 = nodo1.getField("translation")
orientacion1 = nodo1.getField("rotation")

posicion2 = nodo2.getField("translation")

delta = 0.001
delta_r = math.pi / 180

nueva_rotacion = [0, 1, 0, math.pi / 24]
orientacion1.setSFRotation(nueva_rotacion)


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

    # movimiento del objeto 1
    posicion_actual1 = posicion1.getSFVec3f()
    posicion_actual1[2] += delta
    orientacion_actual1 = orientacion1.getSFRotation()
    orientacion_actual1[3] += delta_r
    posicion1.setSFVec3f(posicion_actual1)
    orientacion1.setSFRotation(orientacion_actual1)

    # Distancia del centroide a la arena
    arena = 0
    distancia = abs(posicion_actual1[2] - arena)
    print(f"Distancia del centroide de '{nombre_objeto1}' a la arena: {distancia:.4f} m")

    # Distancia entre objeto 1 y objeto 2
    posicion_actual2 = posicion2.getSFVec3f()
    dx = posicion_actual1[0] - posicion_actual2[0]
    dy = posicion_actual1[1] - posicion_actual2[1]
    dz = posicion_actual1[2] - posicion_actual2[2]
    distancia_entre_objetos = math.sqrt(dx**2 + dy**2 + dz**2)
    print(f"Distancia entre '{nombre_objeto1}' y '{nombre_objeto2}': {distancia_entre_objetos:.4f} m")
