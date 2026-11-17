import pygame

from src.constants import ALTO_DISPARO, ANCHO_DISPARO, AMARILLO, VELOCIDAD_DISPARO


class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.Surface((width, 20))
        self.image.fill(AMARILLO)
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.velocity_y = -10
        self.daño = 1

    def update(self):
        self.rect.y += self.velocity_y
        if self.rect.bottom < 0:
            self.kill()


class RayoEspecial(pygame.sprite.Sprite):
    def __init__(self, x, y, width=ANCHO_DISPARO * 3):
        super().__init__()
        self.image = pygame.Surface((width, ALTO_DISPARO * 2))
        self.image.fill(AMARILLO)
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.velocity_y = -VELOCIDAD_DISPARO * 2
        self.daño = 3

    def update(self):
        self.rect.y += self.velocity_y
        if self.rect.bottom < 0:
            self.kill()
