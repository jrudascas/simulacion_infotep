from controller import Supervisor, Keyboard
import math

control = Supervisor()
paso_tiempo = int(control.getBasicTimeStep())

teclado = Keyboard()
teclado.enable(paso_tiempo)

print("Controlador principal activado.")
etiqueta_objeto_a = "bloqueA"
etiqueta_objeto_b = "bloqueB"

nodo_a = control.getFromDef(etiqueta_objeto_a)
nodo_b = control.getFromDef(etiqueta_objeto_b)

def calcular_distancia(post1):
    return  math.sqrt(
        post1[0]**2 +
        post1[1]**2 +
        post1[2]**2
    )

def calcular_distancia_bloques(posta,postb):
    return math.sqrt(
            (posicion_actual_a[0] - posicion_actual_b[0])**2 +
            (posicion_actual_a[1] - posicion_actual_b[1])**2 +
            (posicion_actual_a[2] - posicion_actual_b[2])**2
        )

if nodo_a is None or nodo_b is None
    print("No se encontró un nodo con DEF 'bloqueA', 'bloque b")
else:
    posicion_a = nodo_a.getField("translation")
    rotacion_a = nodo_a.getField("rotation")
    posicion_b = nodo_b.getField("translation")

incremento = 0.001
ajuste_rotacion = math.pi / 180

direccion_bloque_a = 1
vel_bloque_a = 0.01

direccion_bloque_b = -1
vel_bloque_b = 0.01

nueva_orientacion = [0, 1, 0, math.pi / 24]
rotacion_a.setSFRotation(nueva_orientacion)

distancia_minima = 0.1

while control.step(paso_tiempo) != -1:
    tecla = teclado.getKey()
    if tecla != -1:
        if tecla == ord('Q'):
            break
        if tecla == Keyboard.UP:
            incremento += 0.01
        if tecla == Keyboard.DOWN:
            incremento -= 0.01
        if tecla == Keyboard.LEFT:
            ajuste_rotacion -= 0.01
        if tecla == Keyboard.RIGHT:
            ajuste_rotacion += 0.01

    posicion_actual_a = posicion_a.getSFVec3f()
    posicion_actual_a[2] += direccion_bloque_a * vel_bloque_a
    posicion_actual_a[0] = 0.0 
    posicion_actual_a[1] = 0.05 
    
    if posicion_actual_a[2] > 1.0:
        direccion_bloque_a = -1
    elif posicion_actual_a[2] < -1.0:  
        direccion_bloque_a = 1

    posicion_a.setSFVec3f(posicion_actual_a)

    rot_actual_a = rotacion_a.getSFRotation()
    rot_actual_a[3] += ajuste_rotacion
    rotacion_a.setSFRotation(rot_actual_a)

    if nodo_b is not None:
        posicion_actual_b = posicion_b.getSFVec3f()
        posicion_actual_b[1] = 0.05 
        posicion_actual_b[0] = 0.0
        posicion_actual_b[2] += direccion_bloque_b * vel_bloque_b
        
        if posicion_actual_b[2] > 1.0:
            direccion_bloque_b = -1
        elif posicion_actual_b[2] < -1.0:
            direccion_bloque_b = 1

        posicion_b.setSFVec3f(posicion_actual_b)

    distancia_base = calcular_distancia(posicion_actual_a)
    
    # Punto 1: Calcular distancia entre bloqueA y la base de referencia
    print(f"Distancia de bloqueA a la base: {distancia_base:.4f} m")

    # Calcular distancia entre bloqueA y bloqueB
    if nodo_b is not None:
        distancia_entre_bloques = calcular_distancia_bloques(posicion_actual_a, posicion_actual_b)
       
        print(f"Distancia entre bloqueA y bloqueB: {distancia_entre_bloques:.4f} m")

        # Punto 2: Detectar colisión entre bloqueA y bloqueB
        radio_a = 0.1
        radio_b = 0.1
        if distancia_entre_bloques < (radio_a + radio_b + distancia_minima):
            print("Colisión detectada entre bloqueA y bloqueB")

        