from controller import Supervisor, Keyboard
from sympy import Matrix, cos, sin, pi
import math

# Inicialización del Supervisor
supervisor = Supervisor()
paso_tiempo = int(supervisor.getBasicTimeStep())

# 1. Obtener los nodos necesarios (Asegúrate que los DEF coincidan en Webots)
nodo_peaton = supervisor.getFromDef("pedestrian1")
nodo_botella = supervisor.getFromDef("BeerBottle")

if nodo_peaton is None:
    print("ERROR: No se encontró el nodo del humanoide (pedestrian1)")
if nodo_botella is None:
    print("ERROR: No se encontró el nodo de la botella (BeerBottle)")

# Parámetros de movimiento
TAMANO_PASO = 0.05
PASO_ANGULO = math.pi / 40  # 5 grados

# --- OFFSET DE LA MANO ---
# [X (adelante), Y (lateral), Z (altura)]
# Estos valores ubican la botella respecto al centro del personaje
OFFSET_MANO = Matrix([0.0, -0.20, -0.50])

# Activar teclado
teclado = supervisor.getKeyboard()
teclado.enable(paso_tiempo)

def trasladar(nodo, dx_local, dy_local):
    campo_traslacion = nodo.getField("translation")
    pos = campo_traslacion.getSFVec3f()
    P_vieja = Matrix([pos[0], pos[1], pos[2]])

    campo_rotacion = nodo.getField("rotation")
    _, _, _, angulo = campo_rotacion.getSFRotation()

    # Matriz de rotación R_z(θ) para el movimiento
    R_z = Matrix([
        [cos(angulo), -sin(angulo), 0],
        [sin(angulo),  cos(angulo), 0],
        [          0,             0, 1]
    ])

    d_local = Matrix([dx_local, dy_local, 0])
    d_mundial = R_z * d_local
    P_nueva = P_vieja + d_mundial

    campo_traslacion.setSFVec3f([
        float(P_nueva[0]),
        float(P_nueva[1]),
        float(P_nueva[2])
    ])

def rotar_z(nodo, delta_angulo):
    campo_rotacion = nodo.getField("rotation")
    rot = campo_rotacion.getSFRotation()
    nuevo_angulo = rot[3] + delta_angulo
    campo_rotacion.setSFRotation([0, 0, 1, nuevo_angulo])

print("=== CONTROL INICIADO ===")
print("Lógica: Seguimiento de botella con inclinación matricial activa.")

# 
while supervisor.step(paso_tiempo) != -1:
    tecla = teclado.getKey()

    # A. Control de movimiento del humanoide
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

    # B. Lógica de seguimiento e inclinación (Punto IV del parcial)
    if nodo_peaton is not None and nodo_botella is not None:
        # 1. Obtener traslación y rotación actual del personaje
        campo_h_tras = nodo_peaton.getField("translation")
        campo_h_rot = nodo_peaton.getField("rotation")
        
        pos_h = campo_h_tras.getSFVec3f()
        ang_h = campo_h_rot.getSFRotation()[3]
        
        P_humanoide = Matrix([pos_h[0], pos_h[1], pos_h[2]])

        # 2. Matriz de rotación del personaje (Rz)
        R_z_personaje = Matrix([
            [cos(ang_h), -sin(ang_h), 0],
            [sin(ang_h),  cos(ang_h), 0],
            [          0,           0, 1]
        ])

        # 3. Definir inclinación hacia adelante (Rotación en Y local)
        # 0.3 radianes son aprox 17 grados. Ajústalo si quieres más/menos.
        ang_inc = 0.5 
        R_y_inclinacion = Matrix([
            [cos(ang_inc),  0, sin(ang_inc)],
            [0,             1,            0],
            [-sin(ang_inc), 0, cos(ang_inc)]
        ])

        # 4. Cálculo de posición final de la botella
        P_botella_final = P_humanoide + (R_z_personaje * OFFSET_MANO)

        # 5. Cálculo de rotación final combinada: R_total = R_z * R_y
        R_total = R_z_personaje * R_y_inclinacion

        # 6. Actualizar Traslación
        campo_b_tras = nodo_botella.getField("translation")
        campo_b_tras.setSFVec3f([float(P_botella_final[0]), 
                                 float(P_botella_final[1]), 
                                 float(P_botella_final[2])])

        # 7. Convertir R_total a Axis-Angle para Webots [x, y, z, angle]
        # Algoritmo de extracción de eje-ángulo desde matriz de rotación
        trace = R_total[0,0] + R_total[1,1] + R_total[2,2]
        cos_theta = (trace - 1) / 2
        
        # Validación para evitar errores numéricos fuera de [-1, 1]
        cos_theta = max(min(float(cos_theta), 1.0), -1.0)
        theta = math.acos(cos_theta)

        if theta > 0.001:
            # Eje de rotación (v_x, v_y, v_z)
            v_x = (R_total[2,1] - R_total[1,2])
            v_y = (R_total[0,2] - R_total[2,0])
            v_z = (R_total[1,0] - R_total[0,1])
            
            # Normalización del eje
            norma = math.sqrt(v_x**2 + v_y**2 + v_z**2)
            nodo_botella.getField("rotation").setSFRotation([
                float(v_x/norma), float(v_y/norma), float(v_z/norma), float(theta)
            ])
        else:
            # Si no hay rotación, eje Z por defecto
            nodo_botella.getField("rotation").setSFRotation([0, 0, 1, 0])