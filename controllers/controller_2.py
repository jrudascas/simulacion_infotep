"""
Ejemplo  de un controlador de un robot tipo supervisor

2 esferas ball1 y ball2. ball2 hace seguimiento de la posición de ball1
"""

from controller import Supervisor
import numpy as np

supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())

ball1 = supervisor.getFromDef("ball1")
ball2 = supervisor.getFromDef("ball2")

translation_field = ball2.getField("translation")

def get_position(node):
    return np.array(node.getField("translation").getSFVec3f())

speed = 0.01  # Velocidad constante

while supervisor.step(timestep) != -1:
    pos1 = get_position(ball1)
    pos2 = get_position(ball2)
    
    direction = pos1 - pos2
    distance = np.linalg.norm(direction)

    if distance > 0.001:
        direction_normalized = direction / distance
        new_pos = pos2 + direction_normalized * speed
        # Mantener altura Y
        #new_pos[1] = pos2[1]
        print(new_pos)

        translation_field.setSFVec3f(new_pos.tolist())