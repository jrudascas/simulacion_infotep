from controller import Supervisor, Keyboard
from sympy import Matrix, cos, sin
import math

supervisor = Supervisor()
paso_tiempo = int(supervisor.getBasicTimeStep())

# ---------------------------------------------------------------
# NODOS
# ---------------------------------------------------------------
nodo_peaton = supervisor.getFromDef("pedestrian1")
botella = supervisor.getFromDef("BEER")

if nodo_peaton is None:
    print("ERROR: No se encontró el humanoide")

if botella is None:
    print("ERROR: No se encontró la botella")

# ---------------------------------------------------------------
# PARÁMETROS
# ---------------------------------------------------------------
TAMANO_PASO = 0.05
PASO_ANGULO = math.pi / 36

# POSICIÓN MANO DERECHA (ajustada)
offset_mano = Matrix([0.18, -0.28, 1.22])

# SUAVIZADO (efecto realista)
pos_botella_actual = Matrix([0, 0, 0])
alpha = 0.3  # entre 0.1 (suave) y 1 (sin suavizado)

# ---------------------------------------------------------------
# TECLADO
# ---------------------------------------------------------------
teclado = supervisor.getKeyboard()
teclado.enable(paso_tiempo)

# ---------------------------------------------------------------
# TRASLACIÓN
# ---------------------------------------------------------------
def trasladar(nodo, dx_local, dy_local):

    pos = nodo.getField("translation").getSFVec3f()
    P_vieja = Matrix([pos[0], pos[1], pos[2]])

    _, _, _, angulo = nodo.getField("rotation").getSFRotation()

    R_z = Matrix([
        [cos(angulo), -sin(angulo), 0],
        [sin(angulo),  cos(angulo), 0],
        [0, 0, 1]
    ])

    d_local = Matrix([dx_local, dy_local, 0])
    d_mundial = R_z * d_local

    P_nueva = P_vieja + d_mundial

    nodo.getField("translation").setSFVec3f([
        float(P_nueva[0]),
        float(P_nueva[1]),
        float(P_nueva[2])
    ])

# ---------------------------------------------------------------
# ROTACIÓN
# ---------------------------------------------------------------
def rotar_z(nodo, delta_angulo):

    campo_rotacion = nodo.getField("rotation")
    x, y, z, angulo = campo_rotacion.getSFRotation()

    campo_rotacion.setSFRotation([0, 0, 1, angulo + delta_angulo])

# ---------------------------------------------------------------
# BOTELLA AGARRE REALISTA
# ---------------------------------------------------------------
def actualizar_botella():

    global pos_botella_actual

    if nodo_peaton is None or botella is None:
        return

    pos = nodo_peaton.getField("translation").getSFVec3f()
    P_h = Matrix([pos[0], pos[1], pos[2]])

    _, _, _, angulo = nodo_peaton.getField("rotation").getSFRotation()

    R_z = Matrix([
        [cos(angulo), -sin(angulo), 0],
        [sin(angulo),  cos(angulo), 0],
        [0, 0, 1]
    ])

    #  POSICIÓN OBJETIVO EN LA MANO
    P_objetivo = P_h + R_z * offset_mano

    # SUAVIZADO (interpolación)
    pos_botella_actual = pos_botella_actual + alpha * (P_objetivo - pos_botella_actual)

    botella.getField("translation").setSFVec3f([
        float(pos_botella_actual[0]),
        float(pos_botella_actual[1]),
        float(pos_botella_actual[2])
    ])

    #  ROTACIÓN TIPO AGARRE (inclinada)
    botella.getField("rotation").setSFRotation([1, 0, 0, 1.2])

# ---------------------------------------------------------------
# INSTRUCCIONES
# ---------------------------------------------------------------
print("=== CONTROLES ===")
print("Flechas: mover")
print("Q / E: rotar")
print("=================")

# ---------------------------------------------------------------
# BUCLE PRINCIPAL
# ---------------------------------------------------------------
while supervisor.step(paso_tiempo) != -1:

    tecla = teclado.getKey()

    if nodo_peaton is not None and tecla != -1:

        if tecla == Keyboard.UP:
            trasladar(nodo_peaton, TAMANO_PASO, 0)

        elif tecla == Keyboard.DOWN:
            trasladar(nodo_peaton, -TAMANO_PASO, 0)

        elif tecla == Keyboard.LEFT:
            trasladar(nodo_peaton, 0, TAMANO_PASO)

        elif tecla == Keyboard.RIGHT:
            trasladar(nodo_peaton, 0, -TAMANO_PASO)

        elif tecla == ord('Q'):
            rotar_z(nodo_peaton, PASO_ANGULO)

        elif tecla == ord('E'):
            rotar_z(nodo_peaton, -PASO_ANGULO)

    #  SIEMPRE ACTUALIZA LA BOTELLA
    actualizar_botella()