from controller import Supervisor, Keyboard
from sympy import Matrix, cos, sin, pi
import math

supervisor = Supervisor()
paso_tiempo = int(supervisor.getBasicTimeStep())

# Referencia a los nodos según los nombres DEF definidos
nodo_peaton = supervisor.getFromDef("pedestrian1")
if nodo_peaton is None:
    print("ERROR: No se encontró el nodo pedestrian1")

# Se ajustó el nombre DEF a "beerbottle" para coincidir con el mundo
nodo_botella = supervisor.getFromDef("beerbottle")
if nodo_botella is None:
    print("ERROR: No se encontró el nodo beerbottle")

# Parámetros de movimiento
TAMANO_PASO = 0.05
PASO_ANGULO = math.pi / 36

# Offset ajustado para la posición de la mano
OFFSET_X = 0.0
OFFSET_Y = -0.2
OFFSET_Z = 0.8  # Se ajustó para que la botella esté sobre el suelo (mano)

teclado = supervisor.getKeyboard()
teclado.enable(paso_tiempo)

def calcular_Rz(angulo):
    """Retorna la matriz de rotación R_z(θ)"""
    return Matrix([
        [cos(angulo), -sin(angulo), 0],
        [sin(angulo),  cos(angulo), 0],
        [          0,            0, 1]
    ])

def trasladar(nodo, dx_local, dy_local):
    """Aplica traslación usando cambio de sistema de referencia"""
    campo_traslacion = nodo.getField("translation")
    pos = campo_traslacion.getSFVec3f()
    P_vieja = Matrix([pos[0], pos[1], pos[2]])

    campo_rotacion = nodo.getField("rotation")
    _, _, _, angulo = campo_rotacion.getSFRotation()

    R_z = calcular_Rz(angulo)
    d_local = Matrix([dx_local, dy_local, 0])
    d_mundial = R_z * d_local
    P_nueva = P_vieja + d_mundial

    campo_traslacion.setSFVec3f([
        float(P_nueva[0]),
        float(P_nueva[1]),
        float(P_nueva[2])
    ])

def rotar_z(nodo, delta_angulo):
    """Aplica rotación incremental sobre el eje Z"""
    campo_rotacion = nodo.getField("rotation")
    _, _, _, angulo = campo_rotacion.getSFRotation()
    campo_rotacion.setSFRotation([0, 0, 1, angulo + delta_angulo])

def anclar_botella():
    """Mantiene la botella vinculada a la mano derecha del personaje"""
    if nodo_peaton is None or nodo_botella is None:
        return

    pos = nodo_peaton.getField("translation").getSFVec3f()
    P_humano = Matrix([pos[0], pos[1], pos[2]])

    _, _, _, angulo = nodo_peaton.getField("rotation").getSFRotation()
    Rz = calcular_Rz(angulo)

    d_local   = Matrix([OFFSET_X, OFFSET_Y, 0])
    P_botella = P_humano + Rz * d_local

    nodo_botella.getField("translation").setSFVec3f([
        float(P_botella[0]),
        float(P_botella[1]),
        float(OFFSET_Z) # Altura relativa al mundo o mano
    ])
    nodo_botella.getField("rotation").setSFRotation([0, 0, 1, angulo])
    nodo_botella.resetPhysics()

while supervisor.step(paso_tiempo) != -1:
    tecla = teclado.getKey()

    if nodo_peaton is not None and tecla != -1:
        if tecla == Keyboard.UP:
            trasladar(nodo_peaton, TAMANO_PASO, 0.0)
        elif tecla == Keyboard.DOWN:
            trasladar(nodo_peaton, -TAMANO_PASO, 0.0)
        elif tecla == Keyboard.LEFT:
            trasladar(nodo_peaton, 0.0, TAMANO_PASO)
        elif tecla == Keyboard.RIGHT:
            trasladar(nodo_peaton, 0.0, -TAMANO_PASO)
        elif tecla == ord('Q'):
            rotar_z(nodo_peaton, PASO_ANGULO)
        elif tecla == ord('E'):
            rotar_z(nodo_peaton, -PASO_ANGULO)

    # La botella sigue al personaje en cada paso
    anclar_botella()
