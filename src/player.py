import pygame
import os
from src.constants import *
from .powerups import RayoEspecial

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Cargar la imagen del jugador
        try:
            self.image = pygame.image.load(os.path.join('img', 'jugador.png'))
            self.image = pygame.transform.scale(self.image, (50, 50))
        except Exception as e:
            print(f"Error al cargar imagen del jugador: {e}")
            # Si no se encuentra la imagen, usar un rectángulo verde
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 255, 0))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.ultimo_disparo = 0
        self.ancho_rayo = 5
        self.powerup_activo = False
        self.rayo_disponible = False
        self.vidas = 3
        self.ultimo_disparo = 0
        self.cadencia_disparo = 333  # 33% más rápido (500 * 0.67 = 333)
        self.tiempo_powerup = 0
        self.puntuacion = 0

    def update(self):
        # Obtener teclas presionadas
        teclas = pygame.key.get_pressed()
        self.velocidad_x = 0
        if teclas[pygame.K_LEFT]:
            self.velocidad_x = -VELOCIDAD_JUGADOR
        if teclas[pygame.K_RIGHT]:
            self.velocidad_x = VELOCIDAD_JUGADOR

        # Movimiento horizontal
        self.rect.x += self.velocidad_x
        
        # Limitar al borde de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO

        # Actualizar estado del power-up
        if self.powerup_activo:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_powerup > DURACION_POWERUP:
                self.powerup_activo = False
                self.rayo_disponible = False

    def disparar(self, grupo_todos, grupo_disparos):
        """Crea un nuevo disparo"""
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_disparo > self.cadencia_disparo:
            self.ultimo_disparo = ahora
            if self.powerup_activo and self.rayo_disponible:
                rayo = RayoEspecial(self.rect.centerx, self.rect.top, self.ancho_rayo)
                grupo_todos.add(rayo)
                grupo_disparos.add(rayo)
                self.rayo_disponible = False
                self.powerup_activo = False  # Desactivar el power-up después de usarlo
                self.vidas -= 1  # Quitar una vida al usar el rayo
            else:
                disparo = Disparo(self.rect.centerx, self.rect.top, self.ancho_rayo)
                grupo_todos.add(disparo)
                grupo_disparos.add(disparo)

    def activar_powerup(self):
        """Activa el power-up"""
        self.powerup_activo = True
        self.tiempo_powerup = pygame.time.get_ticks()
        self.rayo_disponible = True

class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho):
        super().__init__()
        self.image = pygame.Surface((ancho, 20))
        self.image.fill(AMARILLO)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidad_y = -10
        self.daño = 1  # Daño base del disparo normal

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom < 0:
            self.kill()

class RayoEspecial(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((ANCHO_DISPARO * 3, ALTO_DISPARO * 2))
        self.image.fill(AMARILLO)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidad_y = -VELOCIDAD_DISPARO * 2
        self.daño = 3  # El rayo hace más daño

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom < 0:
            self.kill() 