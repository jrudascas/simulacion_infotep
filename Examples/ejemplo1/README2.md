Andrés José Echeverría rada ----- parcial simulación

-Agrege una botella independiente la llame “bottle” en el mundo esta botella inicialmente tenia una masas de 0.4 lo cual hacía que callera constantemente hasta llegar al suelo ósea nuestra base.
Para las físicas de la botella que queda en la mano hice lo mismo que con el gato

-Primero tome para ver si existía en el mundo usando su nombre que le asigne bottle.

-Despues le asigne coordenadas en el mundo 
OFFSET_BOTELLA = Matrix([0.05, -0.3, -0.6])

-Despues cree una funsion para los dos gato y botella llamada (actualizar_posicion_accesorios())

-Después tome la posición y traslación del humanoide y su matriz de rotación.

-Después busque la nueva posición de la botella si nos damos cuenta tomamos la misma que use con el gato le sumamos la del humanoide debemos tener en cuenta que esto se calcula respecto al mundo 
(# Calcular posición mundial de la botella: P_h + R_z * Offset
P_nueva_botella = P_humano + (R_z * OFFSET_BOTELLA))

-Despues se lo asigno a la botella igual que al gato esto para la traslación
        nodo_botella.getField("translation").setSFVec3f([
            float(P_nueva_botella[0]),
            float(P_nueva_botella[1]),
            float(P_nueva_botella[2])
        ])
-Despues agrege la rotacion
# Que la botella rote igual que el humano
nodo_botella.getField("rotation").setSFRotation([0, 0, 1, angulo])

-y por ultimo llame a la función para actualizar  
# Actualizar accesorios (para que siga al humano incluso al rotar)
actualizar_posicion_accesorios()