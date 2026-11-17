from src.constants import ANCHO
from src.enemies.base import Enemy


class Boss(Enemy):
    """Base para bosses con vida y patrones de comportamiento propios."""

    is_boss = True

    def __init__(self, x, y, image_name, size, health):
        super().__init__(x, y, image_name, size, health)
        self.direction = 1

    def keep_inside_screen(self):
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
            self.direction = -1
        elif self.rect.left < 0:
            self.rect.left = 0
            self.direction = 1
