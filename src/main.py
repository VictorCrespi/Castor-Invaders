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
    jefe_aparecido = False
    jefe_derrotado = False  # Nueva variable para controlar si el jefe ha sido derrotado
    intervalo_disparo = 333
    intervalo_powerup = 20000
    intervalo_enemigo = 500
    powerup_activo = False
    tiempo_powerup = 0
    duracion_powerup = 1500  # 1.5 segundos
    game_over = False
    ejecutando = True
    enemigos_congelados = False
    powerup_infinito = False

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
                    jefe_derrotado = False  # Reiniciar el estado del jefe
                    grupo_todos.empty()
                    grupo_enemigos.empty()
                    grupo_disparos.empty()
                    grupo_powerups.empty()
                    jugador = Jugador()
                    grupo_todos.add(jugador)
                    grupo_jugador.add(jugador)
                    crear_enemigos(grupo_todos, grupo_enemigos)
                elif evento.key == pygame.K_F11:  # Congelar/descongelar enemigos
                    enemigos_congelados = not enemigos_congelados
                elif evento.key == pygame.K_F2:  # Activar/desactivar power-up infinito
                    powerup_infinito = not powerup_infinito
                    if powerup_infinito:
                        powerup_activo = True
                        jugador.velocidad_disparo = 3
                        jugador.ancho_rayo = ANCHO // 2
                    else:
                        powerup_activo = False
                        jugador.velocidad_disparo = 1
                        jugador.ancho_rayo = 5
            
            # Manejar atajos
            manejar_atajos(evento, grupo_todos, grupo_enemigos, grupo_powerups, jugador)

        if not game_over:
            # Actualizar
            grupo_jugador.update()
            grupo_disparos.update()
            grupo_powerups.update()
            
            # Mover enemigos solo si no están congelados
            if not enemigos_congelados:
                mover_enemigos(grupo_enemigos, jugador)
            
            # Verificar si hay un jefe presente
            jefe_presente = any(enemigo.es_jefe for enemigo in grupo_enemigos)
            
            # Crear nuevos enemigos solo si no hay jefe presente y no están congelados
            if not jefe_presente and not enemigos_congelados and tiempo_actual - ultimo_enemigo > intervalo_enemigo:
                crear_nuevo_enemigo(grupo_todos, grupo_enemigos)
                ultimo_enemigo = tiempo_actual

            # Crear jefe al alcanzar 500 puntos, solo si no ha sido derrotado antes
            if puntuacion >= 500 and not jefe_aparecido and not jefe_presente and not jefe_derrotado:
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
                            puntuacion += 10 if not enemigo.es_jefe else 50
                            print(f"Puntuación actual: {puntuacion}")
                            if random.random() < 0.1:
                                crear_powerup(grupo_todos, grupo_powerups)
                            # Si era un jefe, marcar como derrotado
                            if enemigo.es_jefe:
                                jefe_derrotado = True
                                jefe_aparecido = False
            else:
                # Rayo con enemigos
                colisiones_rayo = pygame.sprite.groupcollide(grupo_disparos, grupo_enemigos, False, False)
                for disparo, enemigos in colisiones_rayo.items():
                    for enemigo in enemigos:
                        if enemigo.recibir_daño(1):  # Daño fijo de 1 para el rayo
                            enemigo.kill()
                            puntuacion += 10 if not enemigo.es_jefe else 50
                            print(f"Puntuación actual: {puntuacion}")
                            if random.random() < 0.1:
                                crear_powerup(grupo_todos, grupo_powerups)
                            # Si era un jefe, marcar como derrotado
                            if enemigo.es_jefe:
                                jefe_derrotado = True
                                jefe_aparecido = False

            # Disparos con powerups (se activa el powerup)
            colisiones_powerup = pygame.sprite.groupcollide(grupo_disparos, grupo_powerups, True, True)
            for disparo, powerups in colisiones_powerup.items():
                for powerup in powerups:
                    if not powerup_infinito:  # Solo activar power-up si no está en modo infinito
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
                if not powerup_infinito:  # Solo activar power-up si no está en modo infinito
                    powerup_activo = True
                    tiempo_powerup = tiempo_actual
                    aplicar_powerup(jugador, powerup.tipo)

            # Actualizar powerup activo
            if powerup_activo and not powerup_infinito and tiempo_actual - tiempo_powerup > duracion_powerup:
                powerup_activo = False
                jugador.velocidad_disparo = 1
                jugador.ancho_rayo = 5

        # Dibujar
        pantalla.fill(NEGRO)
        grupo_todos.draw(pantalla)
        
        # Dibujar barras de vida de los enemigos
        for enemigo in grupo_enemigos:
            enemigo.dibujar_vida(pantalla)
            
        mostrar_vidas(pantalla, vidas)
        mostrar_puntuacion(pantalla, puntuacion)
        
        # Mostrar tiempo restante del power-up
        if powerup_activo and not powerup_infinito:
            tiempo_restante = (duracion_powerup - (tiempo_actual - tiempo_powerup)) / 1000
            if tiempo_restante > 0:
                fuente = pygame.font.Font(None, 36)
                texto = fuente.render(f"Power-up: {tiempo_restante:.1f}s", True, BLANCO)
                pantalla.blit(texto, (10, ALTO - 40))
        elif powerup_infinito:
            fuente = pygame.font.Font(None, 36)
            texto = fuente.render("Power-up: INFINITO", True, BLANCO)
            pantalla.blit(texto, (10, ALTO - 40))
        
        if game_over:
            if not mostrar_game_over(pantalla, puntuacion):
                ejecutando = False
            else:
                # Reiniciar juego
                vidas = 3
                puntuacion = 0
                game_over = False
                jefe_aparecido = False
                jefe_derrotado = False  # Reiniciar el estado del jefe
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