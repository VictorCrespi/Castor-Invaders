import pygame
from src.systems.spawning import spawn_boss
from src.powerups import crear_powerup

def manejar_atajos(evento, grupo_todos, grupo_enemigos, grupo_powerups, jugador):
    """Maneja los atajos de teclado del juego"""
    if evento.type == pygame.KEYDOWN:
        # F12: Aparece el jefe
        if evento.key == pygame.K_F12:
            print("Atajo: Aparece el jefe")
            spawn_boss(grupo_todos, grupo_enemigos)
            
        # F1: Aparece el power-up rayo
        elif evento.key == pygame.K_F1:
            print("Atajo: Aparece el power-up rayo")
            crear_powerup(grupo_todos, grupo_powerups)
            
        # F2: Activa el power-up rayo directamente
        elif evento.key == pygame.K_F2:
            print("Atajo: Activar power-up rayo")
            jugador.activar_powerup()
            jugador.rayo_disponible = True 