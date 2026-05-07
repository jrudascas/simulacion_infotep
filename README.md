# Parcial Simulación - Sebastián Hernández



\## Razonamiento de la modificación

Para que la botella siga la mano del humanoide:

1\. Se identificó el nodo de la mano derecha en el árbol de escenas.

2\. Se utilizó el controlador para obtener la matriz de pose de la mano.

3\. Se aplicaron operaciones de álgebra matricial para que la posición y rotación de la botella coincidan con las del efector final del robot en cada paso de tiempo.

