import unittest
import random

import pygame

from src.enemies import CastorBoss, NormalEnemy
from src.powerups import PowerUp
from src.systems.boss import BossLifecycle
from src.systems.spawning import spawn_boss, spawn_initial_enemies


class EnemyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_normal_enemy_dies_when_health_reaches_zero(self):
        enemy = NormalEnemy(0, 0)

        self.assertTrue(enemy.receive_damage(1))
        self.assertFalse(enemy.alive())

    def test_initial_spawn_creates_three_normal_enemies(self):
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()

        spawn_initial_enemies(all_sprites, enemies)

        self.assertEqual(len(enemies), 3)
        self.assertTrue(all(not enemy.is_boss for enemy in enemies))

    def test_spawn_positions_do_not_overlap(self):
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()

        random_state = random.getstate()
        random.seed(123)
        try:
            spawn_initial_enemies(all_sprites, enemies, amount=8)
        finally:
            random.setstate(random_state)

        enemies_list = list(enemies)
        for index, enemy in enumerate(enemies_list):
            for other in enemies_list[index + 1:]:
                self.assertFalse(
                    enemy.rect.inflate(16, 16).colliderect(
                        other.rect.inflate(16, 16)
                    )
                )

    def test_boss_cleanup_removes_normal_enemies_and_powerups(self):
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        spawn_initial_enemies(all_sprites, enemies)
        powerup = PowerUp(0, 0)
        all_sprites.add(powerup)
        powerups.add(powerup)
        boss = spawn_boss(all_sprites, enemies)

        BossLifecycle.prepare_boss_fight(enemies, powerups)

        self.assertIsInstance(boss, CastorBoss)
        self.assertEqual(list(enemies), [boss])
        self.assertEqual(len(powerups), 0)
        self.assertNotIn(powerup, all_sprites)


if __name__ == "__main__":
    unittest.main()
