# Taller Parcial — Simulación
**Rama:** `parcialsimulacion_miercoles_luis_bustamante`
**Autor:** Luis Bustamante

---

## ¿De qué trata esto?

En este taller tomé un ejemplo de la clase anterior que tenía un humanoide caminando en Webots, y le hice varios cambios. El principal fue agregarle una botella de cerveza en la mano derecha que lo siga a donde vaya, sin importar si camina o gira.

---

## ¿Qué le cambié al proyecto?

### 1. Agregué el archivo README.md
Este archivo que estás leyendo. Lo puse en la raíz de la carpeta `ejemplo1` para explicar todo lo que hice y por qué lo hice así.

---

### 2. Agregué una botella a la escena

Metí un nodo de tipo `BeerBottle` a la escena de Webots. Lo encontré en:
```
nodos/webots projects/objects/drinks/beerbottle
```

Le puse el nombre `beer_bottle` (con DEF) para poder encontrarlo desde el código del controlador.

Lo ubiqué manualmente cerca de la mano derecha del humanoide mirando la simulación, y anoté las coordenadas que me dio Webots:
```
Posición de la botella: x=0.262, y=-1.046, z=0.801
```

También le quité la física (`physics NULL`) para que la gravedad no la jalara hacia abajo.

---

### 3. Hice que la botella siempre siga la mano derecha

Esta fue la parte más importante. El problema era: ¿cómo hago para que la botella se mueva junto con el humanoide, sin importar para dónde camine o gire?

**La idea:**

La botella siempre está a una distancia fija de la mano derecha del humanoide. Esa distancia la medí una sola vez en Webots comparando la posición de la botella con la posición del humanoide.

Pero hay un problema: cuando el humanoide gira, esa distancia también gira. Entonces no puedo simplemente sumar los números, porque "adelante" cambia dependiendo hacia dónde mira el humanoide.

**La solución con álgebra:**

Usé una matriz de rotación llamada R_z(θ), que sirve para rotar un vector según el ángulo actual del humanoide. Así, el offset de la mano (que está definido desde el punto de vista del humanoide) se convierte al sistema de coordenadas del mundo real:

```
Posición botella = Posición humanoide + R_z(θ) × offset_mano
```

Donde R_z(θ) es:
```
| cos(θ)  -sin(θ)  0 |
| sin(θ)   cos(θ)  0 |
|   0        0     1 |
```

**¿Cómo calculé el offset?**

Medí en Webots:
```
Posición botella   = [0.262,  -1.046,  0.801]
Posición humanoide = [0.279,  -0.791,  1.290]
Ángulo del humanoide θ = -0.349 rad
```

Calculé la diferencia:
```
ΔP = botella - humanoide = [-0.017, -0.255, -0.488]
```

Luego roté esa diferencia al sistema local del humanoide usando R_z(-θ):
```
offset_local = R_z(-θ) × ΔP = [-0.1036, -0.2338]
```

Ese offset es el que quedó fijo en el código.

**¿Por qué fijé la altura Z?**

El humanoide tiene una animación de caminar que hace que su centro suba y baje un poquito con cada paso. Si dejaba que la Z de la botella dependiera de la Z del humanoide, la botella también subía y bajaba, como si estuviera cayendo repetidamente.

La solución fue fijar la altura Z de la botella en el valor que medí manualmente (`z = 0.801`), y solo dejar que X e Y siguieran al humanoide con la rotación.

---

### 4. La botella se actualiza en todo momento

En el bucle principal del controlador, la función que mueve la botella se llama en **cada paso de la simulación**, no solo cuando se presiona una tecla. Así la botella no se queda atrás cuando el humanoide se mueve.

```python
while supervisor.step(paso_tiempo) != -1:
    # ... manejo del teclado ...

    # Esto se ejecuta siempre, con o sin tecla
    actualizar_posicion_botella(nodo_peaton, nodo_botella)
```

---

## ¿Cómo se controla el humanoide?

| Tecla | Acción |
|-------|--------|
| ↑ | Mover adelante |
| ↓ | Mover atrás |
| ← | Mover a la izquierda |
| → | Mover a la derecha |
| Q | Girar a la izquierda |
| E | Girar a la derecha |

---

## Problemas que encontré y no pude resolver

### La botella sigue cayendo de la mano

A pesar de haber puesto `physics NULL` en el nodo de la botella y de haber fijado la altura Z en el código, la botella sigue cayendo lentamente de la mano del humanoide cuando la simulación está corriendo. El movimiento en X e Y funciona bien — la botella sí sigue al humanoide cuando camina o gira — pero en Z se sigue deslizando hacia abajo con el tiempo.

Intenté solucionar esto de varias formas:

- Fijé la Z en un valor constante en el código (`Z_MANO_FIJA = 0.801893`) para que no dependiera de la animación del humanoide.
- Le quité la física al nodo con `physics NULL` desde el panel de Webots.
- Intenté cambiar el valor de `mass` a 0 para eliminar el efecto de la gravedad, pero **al modificar la masa la simulación se cierra sola** y no permite correrla con ese valor.

Hasta el momento no encontré la forma de mantener la botella completamente estática en la mano. El error persiste.

---

## Archivos modificados

| Archivo | ¿Qué cambié? |
|--------|--------------|
| `worlds/c1.wbt` | Agregué el nodo BeerBottle con DEF beer_bottle |
| `controllers/pedestrian/pedestrian.py` | Agregué la lógica para que la botella siga la mano |
| `README.md` | Este archivo, explicando todo |
