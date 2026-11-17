import pygame

from src.enemies.bosses.base import Boss
from .attacks import CastorAttackPattern


class CastorBoss(Boss):
    """Boss Castor; sus ataques viven en el paquete castor."""

    def __init__(self, x, y):
        super().__init__(x, y, "Castor.png", (180, 180), health=20)
        self.vertical_speed = 0.3
        self.horizontal_speed = 2
        self.attack_pattern = CastorAttackPattern()

    def update(self, player):
        self.attack_pattern.update(self, player)
