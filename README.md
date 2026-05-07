# Parcial Simulación - Nataly Agudelo



Razonamiento de la modificación y lógica implementada

El objetivo técnico de esta actividad consistió en garantizar la sincronización espacial entre un efector final (mano derecha del humanoide) y un objeto dinámico (BeerBottle). Para lograrlo, se aplicó el siguiente razonamiento:



Identificación de la Jerarquía de Nodos: Se procedió a identificar y extraer la referencia del nodo de la mano derecha dentro del árbol de escenas (Scene Tree). Esto es fundamental para establecer el sistema de referencia global del robot respecto al entorno virtual.



Extracción de Cinemática mediante Matrices de Pose: En lugar de utilizar coordenadas simples, se empleó para capturar la matriz de transformación 4x4 de la mano. Esta matriz integra tanto el vector de traslación ($x, y, z$) como la matriz de rotación, permitiendo un seguimiento preciso en los seis grados de libertad.



Aplicación de Álgebra Matricial para el Seguimiento: Para que la botella se mantenga "solidaria" al movimiento del robot de forma independiente a su desplazamiento por el escenario, se implementó un bucle de control que actualiza en tiempo real los campos translation y rotation de la botella.



Lógica: La pose de la botella se iguala a la pose de la mano en cada $step$ de la simulación, actuando la botella como un hijo virtual del nodo de la mano, asegurando que el objeto siempre permanezca en el efector final sin importar las aceleraciones o cambios de trayectoria del humanoide.G

