import random

from src.constants import ANCHO
from src.enemies import CastorBoss, NormalEnemy


ENEMY_SIZE = 60
ENEMY_COLUMNS = 8


def _column_x(column, width=ENEMY_SIZE):
    column_width = ANCHO // ENEMY_COLUMNS
    return column * column_width + (column_width - width) // 2


def add_enemy(enemy, all_sprites, enemy_group):
    all_sprites.add(enemy)
    enemy_group.add(enemy)
    return enemy


def spawn_initial_enemies(all_sprites, enemy_group, amount=3):
    for column in random.sample(range(ENEMY_COLUMNS), amount):
        add_enemy(
            NormalEnemy(_column_x(column), -ENEMY_SIZE),
            all_sprites,
            enemy_group,
        )


def spawn_enemy(all_sprites, enemy_group):
    column = random.randrange(ENEMY_COLUMNS)
    return add_enemy(
        NormalEnemy(_column_x(column), -ENEMY_SIZE),
        all_sprites,
        enemy_group,
    )


def spawn_boss(all_sprites, enemy_group):
    boss = CastorBoss(ANCHO // 2 - 90, 50)
    return add_enemy(boss, all_sprites, enemy_group)
