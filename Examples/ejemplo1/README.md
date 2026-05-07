Bitácora de Implementación: Sistema de Acoplamiento Dinámico,
Autor: [Antonio Bravo]
Materia: Simulación y Robótica

Sobre el Desarrollo,
Este repositorio contiene la solución al parcial práctico donde se integró un nodo BeerBottle al controlador de un humanoide. El objetivo no fue solo colocar el objeto, sino programar una dependencia jerárquica artificial mediante código.

Desafíos Técnicos y Soluciones,
El Problema del "Deslizamiento",
,
Al mover al humanoide con el teclado, la botella inicialmente se quedaba estática. Para solucionar esto, en lugar de usar una relación de "Parenting" en el árbol de nodos, implementé un seguimiento por software. 
Solución: Utilicé la función getSFVec3f() para capturar la posición global del robot en cada frame y re-ubicar la botella instantáneamente.,

Implementación de Álgebra Lineal,
,
Para cumplir con el requerimiento de álgebra matricial, el código realiza una Transformación de Cuerpo Rígido:
Rotación en Z: Se extrae el ángulo actual del robot para que la botella rote en sincronía.,
Inclinación Estética: Se añadió una matriz de rotación en el eje Y local (R_y_inclinacion) con un ángulo de 0.5 rad. Esto permite que la botella no se vea rígida, sino que tenga una inclinación natural hacia el frente.,

Sincronización de Sistemas de Referencia,
,
El mayor reto fue el OFFSET_MANO. Al ser un vector fijo, si el robot giraba 180°, la botella terminaba en el lado opuesto. 
Lógica aplicada: Se multiplicó el vector de posición local por la matriz de rotación del robot. Esto transforma el vector del "espacio del robot" al "espacio del mundo", garantizando que la botella siempre "persiga" la coordenada exacta de la mano derecha.,

Requisitos de Ejecución,
Webots R2023b o superior.,
Librería sympy de Python instalada.,
Nodo con DEF pedestrian1 y BeerBottle presentes en la escena.