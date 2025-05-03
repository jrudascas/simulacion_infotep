"""
Ejemplo de un controlador de un robot tipo supervisor

Este ejemplo actúa en una simulación sobre un nodo con DEF llamado cajax. Dicho nodo será trasladado y 
rotado indefinidamente según parámetros de la aplicación. 

Se habilita manipulación por teclado para administrar dichos parámetros.
"""

from controller import Supervisor, Keyboard
import math

supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())

keyboard = Keyboard()
keyboard.enable(timestep)

print("Controlador supervisor iniciado.")
nombre_objeto = "cajax"
nombre_objeto2 = "caja2"  # Cambiado de 'cajat' a 'caja2'

nodo1 = supervisor.getFromDef(nombre_objeto)
nodo2 = supervisor.getFromDef(nombre_objeto2)

if nodo1 is None or nodo2 is None:
    print("No se encontró uno o ambos nodos con DEF")
else:
    posicion1 = nodo1.getField("translation")
    orientacion1 = nodo1.getField("rotation")

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

        pos1 = posicion1.getSFVec3f()
        pos1[2] += delta

        rot1 = orientacion1.getSFRotation()
        rot1[3] += delta_r

        posicion1.setSFVec3f(pos1)
        orientacion1.setSFRotation(rot1)

        # Mostrar distancia del centroide de cajax a la arena (eje Z)
        distancia_centroide_arena = abs(pos1[2])
        
        # Calcular y mostrar distancia entre cajax y caja2
        pos2 = nodo2.getField("translation").getSFVec3f()
        distancia_entre_objetos = math.sqrt(
            (pos1[0] - pos2[0]) ** 2 +
            (pos1[1] - pos2[1]) ** 2 +
            (pos1[2] - pos2[2]) ** 2
        )

        print("---- Información de posición ----")
        print(f"> Distancia del centroide de 'cajax' a la arena: {distancia_centroide_arena:.4f} m")
        print(f"> Distancia entre 'cajax' y 'caja2': {distancia_entre_objetos:.4f} m")
        