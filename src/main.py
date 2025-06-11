import pygame
import json
import sys
import random
from src.constants import *
from src.player import Jugador
from src.enemies import crear_enemigos, mover_enemigos, crear_nuevo_enemigo, crear_jefe, Enemigo
from src.powerups import crear_powerup, aplicar_powerup
from src.ui import mostrar_vidas, mostrar_puntuacion, mostrar_game_over
from src.atajos import manejar_atajos

def cargar_record():
    try:
        with open('record.json', 'r') as f:
            return json.load(f)['record']
    except:
        return 0

def guardar_record(record):
    with open('record.json', 'w') as f:
        json.dump({'record': record}, f)

def crear_nuevo_enemigo(grupo_todos, grupo_enemigos):
    """Crea un nuevo enemigo en una posición aleatoria"""
    x = random.randint(0, ANCHO - 40)
    y = random.randint(50, ALTO // 2)
    enemigo = Enemigo(x, y)
    grupo_todos.add(enemigo)
    grupo_enemigos.add(enemigo)

def main():
    # Inicialización de Pygame
    pygame.init()
    pygame.display.init()
    
    # Crear la ventana
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Space Invaders")
    reloj = pygame.time.Clock()

    # Grupos de sprites
    grupo_todos = pygame.sprite.Group()
    grupo_jugador = pygame.sprite.Group()
    grupo_enemigos = pygame.sprite.Group()
    grupo_disparos = pygame.sprite.Group()
    grupo_powerups = pygame.sprite.Group()

    # Crear jugador
    jugador = Jugador()
    grupo_todos.add(jugador)
    grupo_jugador.add(jugador)

    # Crear enemigos iniciales
    crear_enemigos(grupo_todos, grupo_enemigos)

    # Variables del juego
    vidas = 3
    puntuacion = 0
    ultimo_disparo = 0
    ultimo_powerup = 0
    ultimo_enemigo = 0
    jefe_aparecido = False  # Para controlar si el jefe ya apareció
    intervalo_disparo = 333  # Reducido de 500 a 333 para aumentar la cadencia en un 33%
    intervalo_powerup = 20000  # 20 segundos entre powerups
    intervalo_enemigo = 500  # 500ms entre enemigos nuevos
    powerup_activo = False
    tiempo_powerup = 0
    game_over = False
    ejecutando = True

    # Bucle principal
    while ejecutando:
        tiempo_actual = pygame.time.get_ticks()
        
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and tiempo_actual - ultimo_disparo > intervalo_disparo:
                    jugador.disparar(grupo_todos, grupo_disparos)
                    ultimo_disparo = tiempo_actual
                elif evento.key == pygame.K_r and game_over:
                    # Reiniciar juego
                    vidas = 3
                    puntuacion = 0
                    game_over = False
                    jefe_aparecido = False
                    grupo_todos.empty()
                    grupo_enemigos.empty()
                    grupo_disparos.empty()
                    grupo_powerups.empty()
                    jugador = Jugador()
                    grupo_todos.add(jugador)
                    grupo_jugador.add(jugador)
                    crear_enemigos(grupo_todos, grupo_enemigos)
            
            # Manejar atajos
            manejar_atajos(evento, grupo_todos, grupo_enemigos, grupo_powerups, jugador)

        if not game_over:
            # Actualizar
            grupo_jugador.update()
            grupo_disparos.update()
            grupo_powerups.update()
            mover_enemigos(grupo_enemigos, jugador)
            
            # Crear nuevos enemigos
            if tiempo_actual - ultimo_enemigo > intervalo_enemigo:
                crear_nuevo_enemigo(grupo_todos, grupo_enemigos)
                ultimo_enemigo = tiempo_actual

            # Crear jefe al alcanzar 500 puntos
            if puntuacion >= 500 and not jefe_aparecido:
                print(f"¡Aparece el jefe! Puntuación: {puntuacion}")
                try:
                    crear_jefe(grupo_todos, grupo_enemigos)
                    print("Jefe creado correctamente")
                    jefe_aparecido = True
                except Exception as e:
                    print(f"Error al crear el jefe: {e}")

            # Crear powerups
            if tiempo_actual - ultimo_powerup > intervalo_powerup:
                crear_powerup(grupo_todos, grupo_powerups)
                ultimo_powerup = tiempo_actual

            # Colisiones
            # Disparos normales con enemigos
            if not powerup_activo:
                colisiones = pygame.sprite.groupcollide(grupo_disparos, grupo_enemigos, True, False)
                for disparo, enemigos in colisiones.items():
                    for enemigo in enemigos:
                        if enemigo.recibir_daño(disparo.daño):
                            enemigo.kill()
                            puntuacion += 10 if not enemigo.es_jefe else 50  # Más puntos por matar al jefe
                            print(f"Puntuación actual: {puntuacion}")  # Debug
                            # Crear powerup aleatoriamente al matar enemigos
                            if random.random() < 0.1:  # 10% de probabilidad
                                crear_powerup(grupo_todos, grupo_powerups)
            else:
                # Rayo con enemigos
                colisiones_rayo = pygame.sprite.groupcollide(grupo_disparos, grupo_enemigos, False, False)
                for disparo, enemigos in colisiones_rayo.items():
                    for enemigo in enemigos:
                        if enemigo.recibir_daño(disparo.daño):
                            enemigo.kill()
                            puntuacion += 10 if not enemigo.es_jefe else 50  # Más puntos por matar al jefe
                            print(f"Puntuación actual: {puntuacion}")  # Debug
                            # Crear powerup aleatoriamente al matar enemigos
                            if random.random() < 0.1:  # 10% de probabilidad
                                crear_powerup(grupo_todos, grupo_powerups)

            # Disparos con powerups (se activa el powerup)
            colisiones_powerup = pygame.sprite.groupcollide(grupo_disparos, grupo_powerups, True, True)
            for disparo, powerups in colisiones_powerup.items():
                for powerup in powerups:
                    powerup_activo = True
                    tiempo_powerup = tiempo_actual
                    aplicar_powerup(jugador, powerup.tipo)

            # Jugador con enemigos
            if pygame.sprite.spritecollide(jugador, grupo_enemigos, True):
                vidas -= 1
                if vidas <= 0:
                    game_over = True

            # Jugador con powerups
            powerups_recogidos = pygame.sprite.spritecollide(jugador, grupo_powerups, True)
            for powerup in powerups_recogidos:
                powerup_activo = True
                tiempo_powerup = tiempo_actual
                aplicar_powerup(jugador, powerup.tipo)

            # Actualizar powerup activo
            if powerup_activo and tiempo_actual - tiempo_powerup > 5000:  # 5 segundos de duración
                powerup_activo = False
                jugador.velocidad_disparo = 1
                jugador.ancho_rayo = 5  # Volver al ancho normal

        # Dibujar
        pantalla.fill(NEGRO)
        grupo_todos.draw(pantalla)
        
        # Dibujar barras de vida de los enemigos
        for enemigo in grupo_enemigos:
            enemigo.dibujar_vida(pantalla)
            
        mostrar_vidas(pantalla, vidas)
        mostrar_puntuacion(pantalla, puntuacion)
        
        if game_over:
            if not mostrar_game_over(pantalla, puntuacion):
                ejecutando = False
            else:
                # Reiniciar juego
                vidas = 3
                puntuacion = 0
                game_over = False
                jefe_aparecido = False
                grupo_todos.empty()
                grupo_enemigos.empty()
                grupo_disparos.empty()
                grupo_powerups.empty()
                jugador = Jugador()
                grupo_todos.add(jugador)
                grupo_jugador.add(jugador)
                crear_enemigos(grupo_todos, grupo_enemigos)

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 