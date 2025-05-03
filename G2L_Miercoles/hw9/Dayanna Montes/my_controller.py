from controller import Supervisor, Keyboard
import math

supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())

keyboard = Keyboard()
keyboard.enable(timestep)

print("Controlador supervisor iniciado.")
nombre_objeto_1 = "cajax"
nombre_objeto_2 = "cajay"

nodo1 = supervisor.getFromDef(nombre_objeto_1)
nodo2 = supervisor.getFromDef(nombre_objeto_2)

if nodo1 is None:
    print("❌ No se encontró un nodo con DEF 'cajax'")
else:
    posicion1 = nodo1.getField("translation")
    orientacion1 = nodo1.getField("rotation")

if nodo2 is None:
    print("❌ No se encontró un nodo con DEF 'cajay'")
else:
    posicion2 = nodo2.getField("translation")

delta = 0.001
delta_r = math.pi / 180

direccion_subida_cajax = 1
velocidad_cajax = 0.01

direccion_subida_cajay = -1
velocidad_cajay = 0.01

nueva_rotacion = [0, 1, 0, math.pi / 24]
orientacion1.setSFRotation(nueva_rotacion)

distancia_colision = 0.1

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

    pos_actual_1 = posicion1.getSFVec3f()
    pos_actual_1[2] += direccion_subida_cajax * velocidad_cajax
    pos_actual_1[0] = 0.0 
    pos_actual_1[1] = 0.05 
    
    if pos_actual_1[2] > 1.0:
        direccion_subida_cajax = -1
    elif pos_actual_1[2] < -1.0:  
        direccion_subida_cajax = 1

    posicion1.setSFVec3f(pos_actual_1)

    rot_actual_1 = orientacion1.getSFRotation()
    rot_actual_1[3] += delta_r
    orientacion1.setSFRotation(rot_actual_1)

    if nodo2 is not None:
        pos_actual_2 = posicion2.getSFVec3f()
        pos_actual_2[1] = 0.05 
        pos_actual_2[0] = 0.0
        pos_actual_2[2] += direccion_subida_cajay * velocidad_cajay
        
        if pos_actual_2[2] > 1.0:
            direccion_subida_cajay = -1
        elif pos_actual_2[2] < -1.0:
            direccion_subida_cajay = 1

        posicion2.setSFVec3f(pos_actual_2)

    distancia_objeto = math.sqrt(
        pos_actual_1[0]**2 +
        pos_actual_1[1]**2 +
        pos_actual_1[2]**2
    )
    
    #Punto 1: Calcular distancia entre cajax y la mesita de ajedrez
    print(f"Distancia de caja'x' a la base: {distancia_objeto:.4f} m")

    #Calcula la distancia entre 'cajax' y 'cajay'
    if nodo2 is not None:
        dist_entre_cajax_y_cajay = math.sqrt(
            (pos_actual_1[0] - pos_actual_2[0])**2 +
            (pos_actual_1[1] - pos_actual_2[1])**2 +
            (pos_actual_1[2] - pos_actual_2[2])**2
        )
        print(f" Distancia entre caja'x' y caja'y': {dist_entre_cajax_y_cajay:.4f} m")

        # Punto 2: Detectar colisión considerando el tamaño de los objetos
        radio_cajax = 0.1
        radio_cajay = 0.1
        if dist_entre_cajax_y_cajay < (radio_cajax + radio_cajay + distancia_colision):
            print("Se detectó colisión entre caja'x' y caja'y'")
