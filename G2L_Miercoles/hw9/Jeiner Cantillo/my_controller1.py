from controller import Supervisor, Keyboard
import math

supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())

keyboard = Keyboard()
keyboard.enable(timestep)

print("Controlador supervisor iniciado.")

nombre_robot1 = "robot"
nombre_robot2 = "robot2"

nodo1 = supervisor.getFromDef(nombre_robot1)
nodo2 = supervisor.getFromDef(nombre_robot2)

if nodo1 is None or nodo2 is None:
    print(" No se encontraron nodos.")
    exit()

pos1 = nodo1.getField("translation")
rot1 = nodo1.getField("rotation")

pos2 = nodo2.getField("translation")
rot2 = nodo2.getField("rotation")

delta = 0.001
delta_r = math.pi / 180

rot1.setSFRotation([0, 1, 0, math.pi / 24])
rot2.setSFRotation([0, 1, 0, math.pi / 24])


def calcular_distancia(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

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

   
    p1 = pos1.getSFVec3f()
    p2 = pos2.getSFVec3f()

 
    p1[2] += delta
    p2[2] -= delta

    r1 = rot1.getSFRotation()
    r2 = rot2.getSFRotation()

    r1[3] += delta_r
    r2[3] -= delta_r

    pos1.setSFVec3f(p1)
    pos2.setSFVec3f(p2)

    rot1.setSFRotation(r1)
    rot2.setSFRotation(r2)

    centro_mesa = [0, 0, 0]
    d_entre_robots = calcular_distancia(p1, p2)
    d_robot1_centro = calcular_distancia(p1, centro_mesa)
    d_robot2_centro = calcular_distancia(p2, centro_mesa)

   
    print(f"Distancia entre robots: {d_entre_robots:.3f}")
    print(f"Distancia Robot 1 al centro: {d_robot1_centro:.3f}")
    print(f"Distancia Robot 2 al centro: {d_robot2_centro:.3f}")
