"# Parcial Simulación - Fares Zuñiga Perez - Miercoles" 
Primero cree el nodo de la botella y lo agregue a la escena. Como no quería que la botella se cayera o se moviera sola, le puse físicas NULL para tener control total sobre ella.

Despues definí tres variables para la botella: `desplazamiento_x`, `desplazamiento_y`, `desplazamiento_z`. Los valores los ajuste al ojo:

```
desplazamiento_x = 0.0` (hacia adelante/atrás)
desplazamiento_y = -0.3` (hacia la derecha del peatón, porque negativo es derecha)
desplazamiento_z = -0.5` (hacia abajo, como para que quede a la altura de la mano)
```

todo esto es en el sistema local del peatón, donde X es mirando hacia donde él ve, Y es izquierda/derecha y Z es arriba/abajo.

El problema es que el peatón puede girar, entonces no puedo sumar esos valores directamente a su posición mundial. Si el peatón rota, su "derecha" ya no es la misma que la derecha del mundo.

Dentro del `while supervisor.step(...)` obtengo la posición del peatón y su rotación Con eso aplico una matriz de rotación para transformar el desplazamiento local a global:

```
dx_mundial = desplazamiento_x * cos(angulo) - desplazamiento_y * sin(angulo)
dy_mundial = desplazamiento_x * sin(angulo) + desplazamiento_y * cos(angulo)
```

Después, la nueva posición de la botella seria:

```
nueva_posicion_botella = [
    posicion_peaton[0] + dx_mundial,
    posicion_peaton[1] + dy_mundial,
    posicion_peaton[2] + desplazamiento_z
]
```

La altura Z la sumo directamente, entonces el eje Z local es igual al global siempre apunta arriba.

Para que la botella también gire con el peatón, le asigno la misma rotación en cada fotograma:

```
nodo_botella.getField("rotation").setSFRotation([0, 0, 1, angulo_peaton])
```

Con `[0,0,1]` porque es el eje vertical.

Y listo. Al hacerlo en cada paso de simulación, la botella sigue al peatón en tiempo real, esto hace que paresca que está pegada a la mano Esto fue los mas complejo del parcial