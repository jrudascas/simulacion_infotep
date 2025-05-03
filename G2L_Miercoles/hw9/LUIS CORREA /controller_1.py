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
nombre_objeto1 = "cajat"

nodo = supervisor.getFromDef(nombre_objeto)
nodo2 = supervisor.getFromDef(nombre_objeto1)

if nodo is None or nodo2 is None:
    print("No se encontró uno o ambos nodos con DEF")
else:
    posicion = nodo.getField("translation")
    orientacion = nodo.getField("rotation")

    delta = 0.001
    delta_r = math.pi / 180

    nueva_rotacion = [0, 1, 0, math.pi / 24]
    orientacion.setSFRotation(nueva_rotacion)

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
        
        posicion_actual = posicion.getSFVec3f()
        posicion_actual[2] += delta
        
        orientacion_actual = orientacion.getSFRotation()
        orientacion_actual[3] += delta_r
        
        posicion.setSFVec3f(posicion_actual)
        orientacion.setSFRotation(orientacion_actual)

        # Distancia del centroide a la arena
        distancia_centroide_arena = abs(posicion_actual[2])
        print(f"Distancia del centroide a la arena: {distancia_centroide_arena:.4f} metros")

        # Distancia entre cajax y cajat
        posicion_obj2 = nodo2.getField("translation").getSFVec3f()
        distancia = math.sqrt(
            (posicion_actual[0] - posicion_obj2[0]) ** 2 +
            (posicion_actual[1] - posicion_obj2[1]) ** 2 +
            (posicion_actual[2] - posicion_obj2[2]) ** 2
        )
        print(f"Distancia entre cajax y cajat: {distancia:.4f} metros")
