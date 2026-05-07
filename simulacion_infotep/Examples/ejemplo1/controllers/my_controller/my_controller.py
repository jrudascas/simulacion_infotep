from controller import Supervisor, Keyboard
from sympy import Matrix, cos, sin, pi
import math

supervisor = Supervisor()
paso_tiempo = int(supervisor.getBasicTimeStep())

# Obtener el nodo del humanoide
nodo_peaton = supervisor.getFromDef("pedestrian1")
if nodo_peaton is None:
    print("ERROR: No se encontró el nodo con DEF del humanoide")

# Parámetros de movimiento
TAMANO_PASO = 0.05          # metros por paso
PASO_ANGULO = math.pi / 36  # 5 grados por paso

# Activar teclado
teclado = supervisor.getKeyboard()
teclado.enable(paso_tiempo)

# ---------------------------------------------------------------
# Desplazamiento en X o Y del sistema de referencia del humanoide
# ---------------------------------------------------------------
def trasladar(nodo, dx_local, dy_local):
    """
    P_nueva = P_vieja + R_z(θ) * d_local

    R_z(θ) = | cos θ  -sin θ  0 |   d_local = | dx_local |
              | sin θ   cos θ  0 |              | dy_local |
              |   0       0    1 |              |    0     |
    """
    # Posición actual como vector columna
    campo_traslacion = nodo.getField("translation")
    pos = campo_traslacion.getSFVec3f()
    P_vieja = Matrix([pos[0], pos[1], pos[2]])

    # Ángulo actual del humanoide
    campo_rotacion = nodo.getField("rotation")
    _, _, _, angulo = campo_rotacion.getSFRotation()

    # Matriz de rotación R_z(θ)
    R_z = Matrix([
        [cos(angulo), -sin(angulo), 0],
        [sin(angulo),  cos(angulo), 0],
        [          0,            0, 1]
    ])

    # Vector de desplazamiento en sistema local
    d_local = Matrix([dx_local, dy_local, 0])

    # Rotación del vector local al sistema mundial
    d_mundial = R_z * d_local

    # Suma vectorial
    P_nueva = P_vieja + d_mundial

    # Aplicar al nodo (evaluar a float antes de enviar a Webots)
    campo_traslacion.setSFVec3f([
        float(P_nueva[0]),
        float(P_nueva[1]),
        float(P_nueva[2])
    ])


# ---------------------------------------------------------------
# Rotación alrededor de Z (horario / antihorario)
# ---------------------------------------------------------------
def rotar_z(nodo, delta_angulo):
    """
    R_nueva = R_z(Δθ) * R_z(θ) = R_z(θ + Δθ)
    """

    # Formato axis-angle [0, 0, 1, θ]
    campo_rotacion.setSFRotation([0, 0, 1, angulo + delta_angulo])


# ---------------------------------------------------------------
# Instrucciones en consola
# ---------------------------------------------------------------
print("=== Control de teclado ===")
print("↑ / ↓  → Mover adelante / atrás    (eje X local)")
print("← / →  → Mover izquierda / derecha (eje Y local)")
print("Q / E  → Rotar antihorario / horario (alrededor de Z)")
print("==========================")

# ---------------------------------------------------------------
# Bucle principal - Tiempo - Simulación
# ---------------------------------------------------------------
while supervisor.step(paso_tiempo) != -1:

    tecla = teclado.getKey()

    if nodo_peaton is not None and tecla != -1:

        # --- Traslación en eje X del humanoide (adelante / atrás) ---
        if tecla == Keyboard.UP:
            print("Adelante")
            trasladar(nodo_peaton, TAMANO_PASO, 0.0)

        elif tecla == Keyboard.DOWN:
            print("Atras")
            trasladar(nodo_peaton, -TAMANO_PASO, 0.0)

        # --- Traslación en eje Y del humanoide (izquierda / derecha) ---
        elif tecla == Keyboard.LEFT:
            print("Izquierda")
            trasladar(nodo_peaton, 0.0, TAMANO_PASO)

        elif tecla == Keyboard.RIGHT:
            print("Derecha")
            trasladar(nodo_peaton, 0.0, -TAMANO_PASO)

        # --- Rotación alrededor de Z ---
        elif tecla == ord('Q'):
            rotar_z(nodo_peaton, PASO_ANGULO)   # Antihorario

        elif tecla == ord('E'):
            rotar_z(nodo_peaton, -PASO_ANGULO)  # Horario