README.md

Descripción de la modificación realizada



En esta práctica se modificó el proyecto base de Webots para agregar una botella a la mano derecha del humanoide y hacer que permaneciera unida a ella durante toda la simulación.



Primero se agregó el nodo BeerBottle dentro de la escena del mundo. Luego se hizo clic derecho sobre el nodo y se seleccionó la opción Edit PROTO Source para poder modificar el archivo PROTO original de la botella.



Después de abrir el archivo, se creó una copia personalizada llamada:



myBeerBottle.proto



El objetivo de crear este nuevo PROTO fue utilizar una versión personalizada de la botella dentro del proyecto sin modificar directamente el archivo original de Webots.



Posteriormente se abrió el archivo:



Pedestrian.proto



Dentro de este archivo se agregó la siguiente línea:



EXTERNPROTO "myBeerBottle.proto"



Esto permitió importar el nuevo PROTO de la botella dentro del humanoide.



Luego se buscó el campo:



MFNode rightHandSlot



y dentro de este se agregó el nodo de la botella:



myBeerBottle {

&#x20; translation 0 0 0

&#x20; rotation 1 0 0 1.57

}



La botella fue agregada dentro del rightHandSlot porque este campo representa el espacio donde se colocan los objetos que el humanoide sostiene con la mano derecha.





Cambios en el archivo .wbt



luego el archivo del mundo quedó configurado de esta manera:



DEF pedestrian1 Pedestrian {

&#x20; translation 0.307661247018465 0.357429772402067 1.29

&#x20; rotation 0 0 1 -2.7925268031909254

&#x20; rightHandSlot \[

&#x20;   myBeerBottle {

&#x20;     translation -4.440892098500626e-16 -0.00024146296678762003 8.869441292524982e-10

&#x20;     rotation 1 -1.467083577476598e-16 1.76705773378087e-16 1.5700000000000007

&#x20;   }

&#x20; ]

}



Gracias a esta configuración, la botella permanece siempre en la mano derecha del humanoide durante toda la simulación.



Finalmente se guardaron los cambios y se ejecutó nuevamente la simulación. Como resultado, la botella apareció directamente en la mano derecha del humanoide y comenzó a moverse junto con él automáticamente.

