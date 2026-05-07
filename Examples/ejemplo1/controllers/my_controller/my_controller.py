from controller import Supervisor, Keyboard
from sympy import Matrix, cos, sin, pi
import math

supervisor = Supervisor()
paso_tiempo = int(supervisor.getBasicTimeStep())

# --- Obtener nodos ---
nodo_peaton = supervisor.getFromDef("pedestrian1")
if nodo_peaton is None:
    print("ERROR: No se encontró el nodo con DEF 'pedestrian1'")

# Obtener el nodo del gato
nodo_gato = supervisor.getFromDef("cat")
if nodo_gato is None:
    print("ERROR: No se encontró el nodo con DEF 'cat'")
    
    
# Obtener el nodo del gato
nodo_botella = supervisor.getFromDef("bottle")
if nodo_botella is None:
    print("ERROR: No se encontró el nodo con DEF 'bottle'")

# Parámetros de movimiento
TAMANO_PASO = 0.05          # metros por paso
PASO_ANGULO = math.pi / 36  # 5 grados por paso

# Coordenadas relativas del gato (Hombro izquierdo)
# Estas son las que proporcionaste: x=0.08, y=0.22, z=1.5
OFFSET_GATO = Matrix([0.08, 0.22, 0.2])

OFFSET_BOTELLA = Matrix([0.05, -0.3, -0.6])

# Activar teclado
teclado = supervisor.getKeyboard()
teclado.enable(paso_tiempo)

# ---------------------------------------------------------------
# Función para sincronizar al gato
# ---------------------------------------------------------------
def actualizar_posicion_accesorios():
    if nodo_peaton is not None and nodo_gato is not None:
        # Obtener posición y rotación actual del humanoide
        campo_tras = nodo_peaton.getField("translation")
        campo_rot = nodo_peaton.getField("rotation")
        
        pos = campo_tras.getSFVec3f()
        _, _, _, angulo = campo_rot.getSFRotation()
        
        P_humano = Matrix([pos[0], pos[1], pos[2]])

        # Matriz de rotación R_z(θ) del humanoide
        R_z = Matrix([
            [cos(angulo), -sin(angulo), 0],
            [sin(angulo),  cos(angulo), 0],
            [          0,            0, 1]
        ])

        # Calcular posición mundial del gato: P_h + R_z * Offset
        P_nueva_gato = P_humano + (R_z * OFFSET_GATO)
        # Calcular posición mundial de la botella: P_h + R_z * Offset
        P_nueva_botella = P_humano + (R_z * OFFSET_BOTELLA)
        
        
        # Aplicar al gato
        nodo_gato.getField("translation").setSFVec3f([
            float(P_nueva_gato[0]),
            float(P_nueva_gato[1]),
            float(P_nueva_gato[2])
        ])
        
        
        # Aplicar a lA BOTELLA
        nodo_botella.getField("translation").setSFVec3f([
            float(P_nueva_botella[0]),
            float(P_nueva_botella[1]),
            float(P_nueva_botella[2])
        ])
        # Que el gato rote igual que el humano
        nodo_gato.getField("rotation").setSFRotation([0, 0, 1, angulo])
        
        # Que la botella rote igual que el humano
        nodo_botella.getField("rotation").setSFRotation([0, 0, 1, angulo])

# ---------------------------------------------------------------
# Desplazamiento del humanoide
# ---------------------------------------------------------------
def trasladar(nodo, dx_local, dy_local):
    campo_traslacion = nodo.getField("translation")
    pos = campo_traslacion.getSFVec3f()
    P_vieja = Matrix([pos[0], pos[1], pos[2]])

    campo_rotacion = nodo.getField("rotation")
    _, _, _, angulo = campo_rotacion.getSFRotation()

    R_z = Matrix([
        [cos(angulo), -sin(angulo), 0],
        [sin(angulo),  cos(angulo), 0],
        [          0,            0, 1]
    ])

    d_local = Matrix([dx_local, dy_local, 0])
    d_mundial = R_z * d_local
    P_nueva = P_vieja + d_mundial

    campo_traslacion.setSFVec3f([
        float(P_nueva[0]),
        float(P_nueva[1]),
        float(P_nueva[2])
    ])

# ---------------------------------------------------------------
# Rotación del humanoide
# ---------------------------------------------------------------
def rotar_z(nodo, delta_angulo):
    campo_rotacion = nodo.getField("rotation")
    _, _, _, angulo = campo_rotacion.getSFRotation()
    campo_rotacion.setSFRotation([0, 0, 1, angulo + delta_angulo])

# ---------------------------------------------------------------
# Instrucciones
# ---------------------------------------------------------------
print("=== Control con Gato en el Hombro ===")
print("Flechas: Mover | Q/E: Rotar")
print("=====================================")

# --- Verificación de Nodos ---
if nodo_peaton is None:
    print("❌ ERROR CRÍTICO: No se encuentra 'pedestrian1' en el mundo.")
else:
    print("✅ Humanoide encontrado.")

if nodo_gato is None:
    print("❌ ERROR CRÍTICO: No se encuentra 'cat' en el mundo. Revisa el DEF en Webots.")
else:
    print("✅ Gato encontrado.")

# ---------------------------------------------------------------
# Bucle principal
# ---------------------------------------------------------------
while supervisor.step(paso_tiempo) != -1:
    tecla = teclado.getKey()

    if nodo_peaton is not None:
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

    # Actualizar al gato siempre (para que siga al humano incluso al rotar)
    actualizar_posicion_accesorios()
