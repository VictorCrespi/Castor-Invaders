import random

import pygame

from src.constants import ANCHO
from src.enemies import CastorBoss, NormalEnemy


ENEMY_SIZE = 60
SPAWN_Y_RANGE = (-240, -ENEMY_SIZE)
SPAWN_MARGIN = 16
SPAWN_ATTEMPTS = 40


def _candidate_position():
    return (
        random.randint(0, ANCHO - ENEMY_SIZE),
        random.randint(*SPAWN_Y_RANGE),
    )


def _is_position_available(position, enemy_group):
    candidate_area = pygame.Rect(
        position[0],
        position[1],
        ENEMY_SIZE,
        ENEMY_SIZE,
    ).inflate(SPAWN_MARGIN, SPAWN_MARGIN)
    return all(
        not candidate_area.colliderect(enemy.rect.inflate(SPAWN_MARGIN, SPAWN_MARGIN))
        for enemy in enemy_group
    )


def _spawn_position(enemy_group):
    candidates = [_candidate_position() for _ in range(SPAWN_ATTEMPTS)]
    for candidate in candidates:
        if _is_position_available(candidate, enemy_group):
            return candidate

    if not enemy_group:
        return candidates[0]

    def distance_to_closest_enemy(position):
        x, y = position
        return min(
            (x - enemy.rect.x) ** 2 + (y - enemy.rect.y) ** 2
            for enemy in enemy_group
        )

    return max(candidates, key=distance_to_closest_enemy)


def add_enemy(enemy, all_sprites, enemy_group):
    all_sprites.add(enemy)
    enemy_group.add(enemy)
    return enemy


def spawn_initial_enemies(all_sprites, enemy_group, amount=3):
    for _ in range(amount):
        spawn_enemy(all_sprites, enemy_group)


def spawn_enemy(all_sprites, enemy_group):
    position = _spawn_position(enemy_group)
    return add_enemy(
        NormalEnemy(*position),
        all_sprites,
        enemy_group,
    )


def spawn_boss(all_sprites, enemy_group):
    boss = CastorBoss(ANCHO // 2 - 90, 50)
    return add_enemy(boss, all_sprites, enemy_group)
