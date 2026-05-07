# Parcial de Simulación

Estudiante: César Luis Arteaga Garcia
Materia: Simulación
UNICARIBE
2026

---

# Implementación de BeerBottle en Webots usando matrices homogéneas

Contexto

Este parcial toma como base el ejemplo trabajado en clase y le agrega una botella de cerveza (BeerBottle) la cual debe estar agarrada por el personaje virtual con su mano derecha. La botella debe moverse juntamente con el humanoide es decir si se mueve a la derecha, izquierda, adelante o hacia atrás esta se debe mover con él, gracias al uso de matrices homogéneas para el cambio de sistema de referencia.

---

Punto 1. Agregado del nodo BeerBottle a la escena (t1.wbt)

Para agregar la botella dentro de la simulación, en el panel izquierdo del árbol de la escena hice clic en el botón de añadir nodo, busqué BeerBottle dentro de la categoría objects/drinks y lo inserté. Una vez en la escena le asigné el nombre DEF botella para poder referenciarlo desde el controlador.

Luego lo ubiqué manualmente cerca de la mano derecha del humanoide usando las flechas de movimiento que Webots muestra al seleccionar el objeto en la vista 3D, ajustando su posición y rotación hasta que quedó en una posición aproximada a la mano. El controlador se encarga de mantenerlo exactamente en esa posición durante la simulación.

Por qué se necesita el DEF:* sin ese identificador, el controlador no puede encontrar el nodo con getFromDef() y no podría manipularlo en tiempo de ejecución.



Punto 2. Función obtener_T_humanoide — Matriz homogénea 4×4 (my_controller.py)

Para que la botella siga correctamente la mano sin importar hacia dónde mire el humanoide, construí una matriz de transformación homogénea que representa tanto la posición como la orientación del humanoide en el mundo:


    | cos θ  -sin θ  0  Px |


T =     | sin θ   cos θ  0  Py |
|   0      0     1  Pz |
|   0      0     0   1 |

Donde Px, Py, Pz son las coordenadas mundiales del humanoide y θ es su ángulo de rotación sobre el eje Z.

Por qué se hace así:* esta matriz permite expresar cualquier punto del sistema local del humanoide en coordenadas del mundo con una sola multiplicación. Si solo usara la traslación, la botella quedaría en la posición correcta cuando el humanoide mira hacia un lado pero se descolocaría al rotar. La matriz homogénea resuelve eso al combinar rotación y traslación en una sola operación.

---

Punto 3. Función calcular_posicion_mano — Posición de la mano en el mundo (my_controller.py)

Con la matriz homogénea construida, calcular la posición mundial de la mano es simplemente multiplicarla por el vector offset que representa dónde está la mano en el sistema local del humanoide:

P_mano_mundial = T × [ox, oy, oz, 1]^T

El offset que usé fue:

python
OFFSET_MANO_DERECHA = Matrix([-0.10, -0.22, -0.45])
```

Estos valores los fui ajustando observando la posición de la botella en la vista 3D de Webots hasta que coincidió con la mano derecha del humanoide.

Por qué funciona independientemente del movimiento:* al leer la posición y ángulo actuales del humanoide en cada paso de tiempo y reconstruir la matriz T, el cálculo siempre refleja el estado real del humanoide en ese instante. Da igual si giró 90 grados o si se movió al otro lado del arena, la botella siempre va a estar en la misma posición relativa a la mano.



Punto 4. Rotación de la botella para simular el agarre (my_controller.py)

La botella por defecto aparecía parada verticalmente. Para que se vea natural en la mano del humanoide la roté aplicando en cada paso:

python
nodo_botella.getField("rotation").setSFRotation([-0.5, 0.2, 0, math.pi / 2])


Esto la inclina aproximadamente 90° con una ligera corrección en el eje Y, que fue el ángulo que mejor simuló visualmente la forma en que una persona sostiene una botella.



Punto 5. Estabilización con resetPhysics() (my_controller.py)

La BeerBottle tiene física activa por defecto, lo que hace que la gravedad la jale hacia abajo en cada paso de simulación. Para evitarlo, después de actualizar su posición y rotación en cada iteración del bucle llamo:

python
nodo_botella.resetPhysics()


Esto reinicia la velocidad y aceleración acumuladas por el motor físico, de modo que la gravedad nunca llega a desplazar la botella de forma visible entre un paso y el siguiente.



Punto 6. Conservación de la altura del humanoide (my_controller.py)

Al mover el humanoide con el teclado usando setSFVec3f, el motor físico intentaba aplicarle gravedad y comenzaba a descender lentamente. Para evitarlo guardé su altura Z original al inicio del programa:

```python
Z_FIJO = nodo_peaton.getField("translation").getSFVec3f()[2]
```

Y en cada traslación fuerzo ese valor de Z, de modo que el humanoide siempre se mantiene a la misma altura sin importar cuántos movimientos se realicen.



Controles de movimiento del personaje virtual



flecha hacia arriba = Mover adelante    
flecha hacia abajo = Mover atrás       
flecha hacia la izquierda = Mover izquierda   
flecha hacia la derecha = Mover derecha     
tecla "Q"      Rotar antihorario 
tecla "E" Rotar horario     

La botella se actualiza automáticamente en cada paso y siempre permanece en la mano derecha del personaje virtual.
