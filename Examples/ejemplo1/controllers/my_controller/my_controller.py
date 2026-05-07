from controller import Supervisor, Keyboard
from sympy import Matrix, cos, sin
import math

# ---------------------------------------------------
# INICIALIZAR SUPERVISOR
# ---------------------------------------------------
supervisor = Supervisor()
paso_tiempo = int(supervisor.getBasicTimeStep())

# ---------------------------------------------------
# OBTENER NODO DEL HUMANOIDE
# IMPORTANTE:
# El humanoide debe tener DEF pedestrian1
# ---------------------------------------------------
nodo_peaton = supervisor.getFromDef("pedestrian1")

if nodo_peaton is None:
    print("ERROR: No se encontró el nodo pedestrian1")

# ---------------------------------------------------
# OBTENER BOTELLA
# IMPORTANTE:
# La botella debe tener DEF BOTELLA
# ---------------------------------------------------
botella = supervisor.getFromDef("BOTELLA")

if botella is None:
    print("ERROR: No se encontró BOTELLA")

campo_botella = botella.getField("translation")

# ---------------------------------------------------
# PARÁMETROS DE MOVIMIENTO
# ---------------------------------------------------
TAMANO_PASO = 0.05
PASO_ANGULO = math.pi / 36

# ---------------------------------------------------
# ACTIVAR TECLADO
# ---------------------------------------------------
teclado = supervisor.getKeyboard()
teclado.enable(paso_tiempo)

# ---------------------------------------------------
# FUNCIÓN DE TRASLACIÓN
# ---------------------------------------------------
def trasladar(nodo, dx_local, dy_local):

    # Campo translation
    campo_traslacion = nodo.getField("translation")

    # Posición actual
    pos = campo_traslacion.getSFVec3f()

    # Vector posición
    P_vieja = Matrix([
        pos[0],
        pos[1],
        pos[2]
    ])

    # Obtener rotación
    campo_rotacion = nodo.getField("rotation")

    x, y, z, angulo = campo_rotacion.getSFRotation()

    # Matriz de rotación
    R_z = Matrix([
        [cos(angulo), -sin(angulo), 0],
        [sin(angulo),  cos(angulo), 0],
        [0, 0, 1]
    ])

    # Movimiento local
    d_local = Matrix([
        dx_local,
        dy_local,
        0
    ])

    # Convertir local → mundial
    d_mundial = R_z * d_local

    # Nueva posición
    P_nueva = P_vieja + d_mundial

    # Aplicar nueva posición
    campo_traslacion.setSFVec3f([
        float(P_nueva[0]),
        float(P_nueva[1]),
        float(P_nueva[2])
    ])

# ---------------------------------------------------
# FUNCIÓN DE ROTACIÓN
# ---------------------------------------------------
def rotar_z(nodo, delta_angulo):

    campo_rotacion = nodo.getField("rotation")

    x, y, z, angulo = campo_rotacion.getSFRotation()

    campo_rotacion.setSFRotation([
        0,
        0,
        1,
        angulo + delta_angulo
    ])

# ---------------------------------------------------
# ACTUALIZAR POSICIÓN DE BOTELLA
# ---------------------------------------------------
def actualizar_botella():

    if botella is None or nodo_peaton is None:
        return

    # Posición humanoide
    campo_traslacion = nodo_peaton.getField("translation")
    pos = campo_traslacion.getSFVec3f()

    # Rotación humanoide
    campo_rotacion = nodo_peaton.getField("rotation")
    _, _, _, angulo = campo_rotacion.getSFRotation()

    # Matriz de rotación 2D
    R_z = Matrix([
        [cos(angulo), -sin(angulo)],
        [sin(angulo),  cos(angulo)]
    ])

    # Offset local mano derecha
    offset_local = Matrix([
        0.1,
        -0.22
    ])

    # Transformar local → global
    offset_mundial = R_z * offset_local

    # Nueva posición botella
    # POSICIÓN FINAL BOTELLA
    nueva_x = float(pos[0] + offset_mundial[0])
    nueva_y = float(pos[1] + offset_mundial[1])
    
    # Altura aproximada de la mano
    nueva_z = float(pos[2] - 0.55)

    # Aplicar posición
    campo_botella.setSFVec3f([
        nueva_x,
        nueva_y,
        nueva_z
    ])

# ---------------------------------------------------
# MENSAJES DE CONSOLA
# ---------------------------------------------------
print("===================================")
print("CONTROLES DEL HUMANOIDE")
print("FLECHA ARRIBA    -> Adelante")
print("FLECHA ABAJO     -> Atrás")
print("FLECHA IZQUIERDA -> Izquierda")
print("FLECHA DERECHA   -> Derecha")
print("Q -> Rotar izquierda")
print("E -> Rotar derecha")
print("===================================")

# ---------------------------------------------------
# LOOP PRINCIPAL
# ---------------------------------------------------
while supervisor.step(paso_tiempo) != -1:

    tecla = teclado.getKey()

    if nodo_peaton is not None and tecla != -1:

        # ADELANTE
        if tecla == Keyboard.UP:
            print("Adelante")
            trasladar(nodo_peaton, TAMANO_PASO, 0)

        # ATRÁS
        elif tecla == Keyboard.DOWN:
            print("Atrás")
            trasladar(nodo_peaton, -TAMANO_PASO, 0)

        # IZQUIERDA
        elif tecla == Keyboard.LEFT:
            print("Izquierda")
            trasladar(nodo_peaton, 0, TAMANO_PASO)

        # DERECHA
        elif tecla == Keyboard.RIGHT:
            print("Derecha")
            trasladar(nodo_peaton, 0, -TAMANO_PASO)

        # ROTAR IZQUIERDA
        elif tecla == ord('Q'):
            print("Rotando izquierda")
            rotar_z(nodo_peaton, PASO_ANGULO)

        # ROTAR DERECHA
        elif tecla == ord('E'):
            print("Rotando derecha")
            rotar_z(nodo_peaton, -PASO_ANGULO)

    # Mantener botella en la mano
    actualizar_botella()