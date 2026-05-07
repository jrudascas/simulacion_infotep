from controller import Supervisor, Keyboard
import math

# Inicialización del Supervisor
supervisor = Supervisor()
paso_tiempo = int(supervisor.getBasicTimeStep())

# Obtener los nodos del mundo
nodo_peaton = supervisor.getFromDef("pedestrian1")
nodo_botella = supervisor.getFromDef("botle")

if not nodo_peaton: print("ERROR: No se encontró 'pedestrian1'")
if not nodo_botella: print("ERROR: No se encontró 'botle'")

# Configuración de movimiento
TAMANO_PASO = 0.05
PASO_ANGULO = math.pi / 36  # 5 grados

# Offset de la botella respecto al humano (Mano derecha aproximada)
OFFSET_X, OFFSET_Y, OFFSET_Z = 0.0, -0.2, -0.5

# Activar Teclado
teclado = supervisor.getKeyboard()
teclado.enable(paso_tiempo)

def actualizar_posiciones(dx_local, dy_local, d_theta):
    """Calcula el movimiento relativo al sistema local del humanoide."""
    if not nodo_peaton: return

    f_trans = nodo_peaton.getField("translation")
    f_rot = nodo_peaton.getField("rotation")
    
    pos = f_trans.getSFVec3f()
    rot = f_rot.getSFRotation() # [x, y, z, angulo]
    angulo_actual = rot[3]

    # Nueva rotación
    nuevo_angulo = angulo_actual + d_theta

    # Transformar movimiento local a coordenadas globales (Matriz de rotación simplificada)
    cos_a = math.cos(angulo_actual)
    sin_a = math.sin(angulo_actual)
    
    dx_mundial = dx_local * cos_a - dy_local * sin_a
    dy_mundial = dx_local * sin_a + dy_local * cos_a

    # Aplicar cambios
    f_trans.setSFVec3f([pos[0] + dx_mundial, pos[1] + dy_mundial, pos[2]])
    f_rot.setSFRotation([0, 0, 1, nuevo_angulo])

def anclar_botella():
    """Sincroniza la posición de la botella con el humanoide."""
    if not nodo_peaton or not nodo_botella: return

    pos_h = nodo_peaton.getField("translation").getSFVec3f()
    ang_h = nodo_peaton.getField("rotation").getSFRotation()[3]

    cos_a = math.cos(ang_h)
    sin_a = math.sin(ang_h)

    # Calcular posición de la botella usando el offset rotado
    bx = pos_h[0] + (OFFSET_X * cos_a - OFFSET_Y * sin_a)
    by = pos_h[1] + (OFFSET_X * sin_a + OFFSET_Y * cos_a)
    bz = pos_h[2] + OFFSET_Z

    nodo_botella.getField("translation").setSFVec3f([bx, by, bz])
    nodo_botella.getField("rotation").setSFRotation([0, 0, 1, ang_h])
    nodo_botella.resetPhysics()

# --- Bucle Principal ---
print("Control WASD activo:")
print("W / S -> Adelante / Atrás")
print("A / D -> Izquierda / Derecha")
print("Q / E -> Rotar")

while supervisor.step(paso_tiempo) != -1:
    tecla = teclado.getKey()
    
    dx, dy, dth = 0.0, 0.0, 0.0

    # Mapeo de teclas WASD y rotación QE
    if tecla == ord('W'):    dx = TAMANO_PASO
    elif tecla == ord('S'):  dx = -TAMANO_PASO
    elif tecla == ord('A'):  dy = TAMANO_PASO
    elif tecla == ord('D'):  dy = -TAMANO_PASO
    elif tecla == ord('Q'):  dth = PASO_ANGULO
    elif tecla == ord('E'):  dth = -PASO_ANGULO

    if tecla != -1:
        actualizar_posiciones(dx, dy, dth)
    
    # Mantener la botella anclada en cada frame
    anclar_botella()