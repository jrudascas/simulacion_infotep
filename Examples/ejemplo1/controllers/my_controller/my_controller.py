from controller import Supervisor, Keyboard
from sympy import Matrix, cos, sin
import math

# ==========================================
# INICIALIZACIÓN DEL SISTEMA
# ==========================================
motor_simulacion = Supervisor()
tiempo_refresco = int(motor_simulacion.getBasicTimeStep())

# Nodos del entorno
robot_principal = motor_simulacion.getFromDef("pedestrian1")
nodo_botella = motor_simulacion.getFromDef("BOTELLA")

if not robot_principal:
    print("Advertencia: Humanoide no detectado.")

# Configuración de entradas
panel_teclado = motor_simulacion.getKeyboard()
panel_teclado.enable(tiempo_refresco)

# Valores de desplazamiento
AVANCE_METROS = 0.05
GIRO_RADIANES = math.pi / 36

# ==========================================
# MOTOR MATEMÁTICO (Requisito Sympy)
# ==========================================
def calcular_traslacion(nodo, delta_x, delta_y):
    """Calcula la nueva posición global mediante álgebra de matrices."""
    campo_pos = nodo.getField("translation")
    campo_rot = nodo.getField("rotation")
    
    posicion_actual = campo_pos.getSFVec3f()
    _, _, _, angulo_z = campo_rot.getSFRotation()
    
    # Creación de vectores y matrices con Sympy
    vector_posicion = Matrix([posicion_actual[0], posicion_actual[1], posicion_actual[2]])
    
    matriz_rotacion_z = Matrix([
        [cos(angulo_z), -sin(angulo_z), 0],
        [sin(angulo_z),  cos(angulo_z), 0],
        [            0,              0, 1]
    ])
    
    vector_movimiento = Matrix([delta_x, delta_y, 0])
    
    # Producto matricial para hallar el desplazamiento en el mundo
    desplazamiento_global = matriz_rotacion_z * vector_movimiento
    nueva_posicion = vector_posicion + desplazamiento_global
    
    # Asignación de datos (convirtiendo de sympy a flotantes de Python)
    campo_pos.setSFVec3f([float(nueva_posicion[0]), float(nueva_posicion[1]), float(nueva_posicion[2])])


def modificar_angulo(nodo, ajuste_radianes):
    """Actualiza la rotación en el eje Z."""
    campo_rot = nodo.getField("rotation")
    _, _, _, angulo_z = campo_rot.getSFRotation()
    campo_rot.setSFRotation([0, 0, 1, angulo_z + ajuste_radianes])

# ==========================================
# BUCLE DE CONTROL Y SIMULACIÓN
# ==========================================
while motor_simulacion.step(tiempo_refresco) != -1:
    
    tecla_pulsada = panel_teclado.getKey()
    
    if robot_principal and tecla_pulsada != -1:
        
        # --- Traslación Lineal ---
        if tecla_pulsada == Keyboard.UP:
            calcular_traslacion(robot_principal, AVANCE_METROS, 0.0)
            
        elif tecla_pulsada == Keyboard.DOWN:
            calcular_traslacion(robot_principal, -AVANCE_METROS, 0.0)
            
        elif tecla_pulsada == Keyboard.LEFT:
            calcular_traslacion(robot_principal, 0.0, AVANCE_METROS)
            
        elif tecla_pulsada == Keyboard.RIGHT:
            calcular_traslacion(robot_principal, 0.0, -AVANCE_METROS)
            
        # --- Rotación Axial ---
        elif tecla_pulsada == ord('Q'):
            modificar_angulo(robot_principal, GIRO_RADIANES)
            
        elif tecla_pulsada == ord('E'):
            modificar_angulo(robot_principal, -GIRO_RADIANES)
            
    # --- Seguimiento de la Botella ---
    if robot_principal and nodo_botella:
        # Igualación de vectores de posición para el control cinemático
        coord_robot = robot_principal.getPosition()
        # Se aplica un desfase en X y Z para evitar colisión de mallas
        nodo_botella.getField("translation").setSFVec3f([coord_robot[0] + 0.3, coord_robot[1], coord_robot[2] + 0.5])