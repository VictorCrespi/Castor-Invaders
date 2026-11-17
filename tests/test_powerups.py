import unittest

import pygame

from src.player import Jugador
from src.powerups import aplicar_powerup, crear_powerup
from src.projectiles import RayoEspecial


class PowerUpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_powerup_creation_does_not_fail(self):
        all_sprites = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        crear_powerup(all_sprites, powerups)

        self.assertEqual(len(powerups), 1)

    def test_beam_keeps_its_powerup_state_after_firing(self):
        player = Jugador()
        player.ancho_rayo = 400
        aplicar_powerup(player, "rayo")
        player.ultimo_disparo = pygame.time.get_ticks() - 1000
        all_sprites = pygame.sprite.Group()
        shots = pygame.sprite.Group()

        player.disparar(all_sprites, shots)

        beam = next(iter(shots))
        self.assertIsInstance(beam, RayoEspecial)
        self.assertEqual(beam.rect.width, 400)
        self.assertLess(beam.visual_width, beam.rect.width)
        self.assertTrue(player.powerup_activo)
        self.assertTrue(player.rayo_disponible)
        self.assertEqual(player.cadencia_disparo, 500)
        self.assertEqual(player.vidas, 3)


if __name__ == "__main__":
    unittest.main()
