import os

import pygame

from src.constants import ALTO, GRIS, ROJO, VERDE


class Enemy(pygame.sprite.Sprite):
    """Base común para todos los enemigos."""

    is_boss = False

    def __init__(self, x, y, image_name="Pereira.png", size=(60, 60), health=1):
        super().__init__()
        self.image = self._load_image(image_name, size)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1.2
        self.health = health
        self.max_health = health

    @staticmethod
    def _load_image(image_name, size, fallback_color=ROJO):
        try:
            image = pygame.image.load(os.path.join("img", image_name))
            return pygame.transform.scale(image, size)
        except (FileNotFoundError, pygame.error):
            image = pygame.Surface(size)
            image.fill(fallback_color)
            return image

    @property
    def es_jefe(self):
        """Compatibilidad con el código antiguo del juego."""
        return self.is_boss

    def receive_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True
        return False

    def recibir_daño(self, daño, es_rayo=False):
        """Compatibilidad con el nombre anterior."""
        return self.receive_damage(1 if es_rayo else daño)

    def update(self, player):
        self.rect.y += self.speed
        if self.rect.top > player.rect.bottom:
            player.vidas -= 1
            self.kill()

    def draw_health(self, surface):
        if not self.is_boss:
            return
        width, height = 40, 5
        x = self.rect.x + (self.rect.width - width) // 2
        y = self.rect.y - 10
        pygame.draw.rect(surface, GRIS, (x, y, width, height))
        health_width = max(0, self.health / self.max_health * width)
        pygame.draw.rect(surface, VERDE, (x, y, health_width, height))

    def dibujar_vida(self, pantalla):
        self.draw_health(pantalla)
