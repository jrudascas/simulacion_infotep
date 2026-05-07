

Tabla Comparativa de Cambios



Justificación de los Cambios

1. DeCálculo Simbólico a Cálculo Directo
El código original trataba el movimiento como un problema de álgebra avanzada, creando estructuras complejas (matrices) cada vez que pulsabas una tecla.
en la versión optimizada, cambiamos eso por fórmulas directas es como la diferencia entre usar una enciclopedia para buscar una suma o hacerla de cabeza el resultado es el mismo, pero el ordenador trabaja mucho menos, logrando que el personaje se mueva sin "tirones".

2. Manejo de movimiento con lasTeclas (WASD)
Se sustituyeron las constantes de las flechas por los valores de las letras.
Mejora la experiencia de uso en simulación y videojuegos usar la mano izquierda en **WASD** permite tener la derecha libre para el ratón o para otras funciones, además de evitar conflictos con los comandos de cámara de Webots.

 3. Sincronización de Objetos 
El original ignoraba la existencia de la botella, el nuevo código añade una función que calcula constantemente dónde debería estar la mano del humanoide.
sin esto el humanoide se movería pero la botella se quedaría "flotando o caeria simplemete " en el punto de inicio. Al anclarla matemáticamente, logramos que ambos elementos actúen como una sola unidad en la escena.

4. Unificación de Funciones
En lugar de tener funciones separadas para rotar y trasladar que consultan al simulador varias veces el código optimizado lo procesa todo en un solo bloque de lógica.
cada vez que el código le "pregunta" a Webots "¿dónde está el nodo?", se pierde un poco de tiempo.
 Al preguntar una sola vez y hacer todos los cálculos de golpe, la respuesta del simulador es inmediata.

5. Control de Física (`resetPhysics`)
Se añadió una instrucción para resetear las fuerzas de la botella en cada movimiento.
*   **Por qué:** En los simuladores, si mueves un objeto "teletransportándolo" (cambiando su posición bruscamente), la física a veces intenta corregirlo y el objeto empieza a vibrar o sale disparado. Esta línea de código le dice al simulador: *"Tranquilo, yo sé dónde debe estar, no apliques fuerzas extra"*.