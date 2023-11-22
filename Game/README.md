# Descripción del Proyecto

Este proyecto es un juego de disparos (shooter) inspirado en
el universo de Dragon Ball Z. 
El jugador controla a un personaje que puede moverse horizontalmente
y disparar a enemigos que caen desde la parte superior de la pantalla.
El objetivo es sobrevivir el mayor tiempo posible y obtener la
puntuación más alta. 

Clases

1. Player
- Descripción: Representa al jugador en el juego.
- Atributos: image: Imagen del jugador.
- Métodos:
update: Actualiza la posición del jugador en función de la entrada del usuario.
shoot: Crea un objeto de tipo Power (poder) que se dispara hacia arriba.

2. Enemy
- Descripción: Representa a los enemigos en el juego.
- Atributos: image: Imagen del enemigo.
- Métodos: update: Actualiza la posición del enemigo y lo reposiciona si se va fuera de la pantalla.

3. Power
- Descripción: Representa los disparos del jugador. 
- Atributos: image: Imagen del disparo.
- Métodos: update: Actualiza la posición del disparo y lo elimina si se sale de la pantalla.


Funcionalidades
- Disparos del Jugador: El jugador puede disparar con la tecla de espacio (K_SPACE).
- Movimiento del Jugador: El jugador puede moverse horizontalmente con las teclas de flecha izquierda (K_LEFT) y derecha (K_RIGHT).
- Colisiones: El juego verifica las colisiones entre los enemigos y los disparos del jugador, así como las colisiones entre el jugador y los enemigos.
- Pausa y Volumen: El juego se puede pausar con la tecla de escape (K_ESCAPE). Durante la pausa, el jugador puede ajustar el volumen de la música con las teclas de flecha arriba (K_UP) y abajo (K_DOWN).


Requisitos y Ejecución
- Requisitos: Python, Pygame
- Ejecución: Ejecutar archivo main.py en un entorno con Python y Pygame instalados.