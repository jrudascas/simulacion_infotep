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
nombre_objeto = "cajax"

nodo = supervisor.getFromDef(nombre_objeto)

if nodo is None:
    print("❌ No se encontró un nodo con DEF")
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
            delta = delta + 0.01
        if key == Keyboard.DOWN:
            delta = delta - 0.01
        if key == Keyboard.LEFT:
            delta_r = delta_r - 0.01
        if key == Keyboard.RIGHT:
            delta_r = delta_r + 0.01
    
    posicion_actual = posicion.getSFVec3f()
    posicion_actual[2] = posicion_actual[2] + delta
    
    orientacion_actual = orientacion.getSFRotation()
    orientacion_actual[3] = orientacion_actual[3] + delta_r
    
    posicion.setSFVec3f(posicion_actual)
    orientacion.setSFRotation(orientacion_actual)