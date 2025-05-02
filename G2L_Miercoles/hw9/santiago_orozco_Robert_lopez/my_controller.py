from controller import Supervisor, Keyboard
import math

supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())

keyboard = Keyboard()
keyboard.enable(timestep)

print("Controlador")
caja_x = "cajax"
caja_y = "cajay"

nodo = supervisor.getFromDef(caja_x)
nodo_caja_y = supervisor.getFromDef(caja_y)

if nodo is None:
    print("No se encontro el nodo 'cajax'")
else:
    posicion = nodo.getField("translation")
    orientacion = nodo.getField("rotation")

if nodo_caja_y is None:
    print("No se encontro un nodo 'cajay'")
else:
    posicion_caja_y = nodo_caja_y.getField("translation")

delta = 0.001
delta_r = math.pi / 180

address_subida_cajax = 1
speed_cajax = 0.01

address_subida_cajay = -1
speed_cajay = 0.01

nueva_rotacion = [0, 1, 0, math.pi / 24]
orientacion.setSFRotation(nueva_rotacion)

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

    pos_actual_1 = posicion.getSFVec3f()
    pos_actual_1[2] += address_subida_cajax * speed_cajax
    pos_actual_1[0] = 0.0 
    pos_actual_1[1] = 0.05 
    
    if pos_actual_1[2] > 1.0:
        address_subida_cajax = -1
    elif pos_actual_1[2] < -1.0:  
        address_subida_cajax = 1

    posicion.setSFVec3f(pos_actual_1)

    rot_actual_1 = orientacion.getSFRotation()
    rot_actual_1[3] += delta_r
    orientacion.setSFRotation(rot_actual_1)

    if nodo_caja_y is not None:
        pos_actual_2 = posicion_caja_y.getSFVec3f()
        pos_actual_2[1] = 0.05 
        pos_actual_2[0] = 0.0
        pos_actual_2[2] += address_subida_cajay * speed_cajay
        
        if pos_actual_2[2] > 1.0:
            address_subida_cajay = -1
        elif pos_actual_2[2] < -1.0:
            address_subida_cajay = 1

        posicion_caja_y.setSFVec3f(pos_actual_2)

    distancia_objeto = math.sqrt(
        pos_actual_1[0]**2 +
        pos_actual_1[1]**2 +
        pos_actual_1[2]**2
    )
    
    #Punto 1
    print(f"Distancia entre la caja'x' y la arena: {distancia_objeto:.4f} m")

    #Calculo entre caja x y caja y
    if nodo_caja_y is not None:
        distancia_entre_cajax_y_cajay = math.sqrt(
            (pos_actual_1[0] - pos_actual_2[0])**2 +
            (pos_actual_1[1] - pos_actual_2[1])**2 +
            (pos_actual_1[2] - pos_actual_2[2])**2
        )
        print(f" Distancia entre la caja'x' y caja'y': {distancia_entre_cajax_y_cajay:.4f} m")

        # Punto 2: Detencion de la colision teniendo en cuenta el tamaño de los objetos
        radio_cajax = 0.1
        radio_cajay = 0.1
        if distancia_entre_cajax_y_cajay < (radio_cajax + radio_cajay + distancia_colision):
            print("Se detecto colision con caja'x' y caja'y'")