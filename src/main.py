import json
import random
import sys

import pygame

from src.atajos import manejar_atajos
from src.constants import (
    ALTO,
    ANCHO,
    FPS,
    NEGRO,
    BLANCO,
)
from src.player import Jugador
from src.powerups import aplicar_powerup, crear_powerup
from src.systems.boss import BossLifecycle
from src.systems.enemies import update_enemies
from src.systems.spawning import spawn_boss, spawn_enemy, spawn_initial_enemies
from src.ui import mostrar_game_over, mostrar_puntuacion, mostrar_vidas


class Game:
    """Orquesta el bucle del juego sin contener la lógica de cada entidad."""

    ENEMY_INTERVAL = 750
    POWERUP_INTERVAL = 20000
    PLAYER_SHOT_INTERVAL = 333
    POWERUP_DURATION = 2000

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.shot_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()

        self.running = True
        self.game_over = False
        self.frozen_enemies = False
        self.infinite_powerup = False
        self.score = 0
        self.lives = 3
        self.last_shot = 0
        self.last_powerup = 0
        self.last_enemy = 0
        self.powerup_active = False
        self.powerup_started = 0
        self.boss_spawned = False
        self.boss_defeated = False

        self.player = Jugador()
        self.all_sprites.add(self.player)
        self.player_group.add(self.player)
        spawn_initial_enemies(self.all_sprites, self.enemy_group)

    def run(self):
        while self.running:
            now = pygame.time.get_ticks()
            self.handle_events(now)
            if not self.game_over:
                self.update(now)
            self.draw(now)
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def handle_events(self, now):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_key(event.key, now)
            manejar_atajos(
                event,
                self.all_sprites,
                self.enemy_group,
                self.powerup_group,
                self.player,
            )

    def handle_key(self, key, now):
        if key == pygame.K_SPACE and now - self.last_shot > self.PLAYER_SHOT_INTERVAL:
            self.player.disparar(self.all_sprites, self.shot_group)
            self.last_shot = now
        elif key == pygame.K_r and self.game_over:
            self.reset()
        elif key == pygame.K_F11:
            self.frozen_enemies = not self.frozen_enemies
        elif key == pygame.K_F2:
            self.infinite_powerup = not self.infinite_powerup
            if self.infinite_powerup:
                self.powerup_active = True
                self.player.velocidad_disparo = 3
                self.player.ancho_rayo = ANCHO // 2
            else:
                self.deactivate_powerups()

    def update(self, now):
        self.player_group.update()
        self.shot_group.update()
        self.powerup_group.update()
        self.update_boss_state()

        if not self.frozen_enemies:
            update_enemies(self.enemy_group, self.player)
            self.lives = self.player.vidas

        boss_present = BossLifecycle.is_active(self.enemy_group)
        if not boss_present and now - self.last_enemy > self.ENEMY_INTERVAL:
            spawn_enemy(self.all_sprites, self.enemy_group)
            self.last_enemy = now

        if (
            self.score >= 500
            and not self.boss_spawned
            and not self.boss_defeated
            and not boss_present
        ):
            self.start_boss()
            boss_present = True

        if not boss_present and now - self.last_powerup > self.POWERUP_INTERVAL:
            crear_powerup(self.all_sprites, self.powerup_group)
            self.last_powerup = now

        self.handle_enemy_collisions()
        if not boss_present:
            self.handle_powerup_collisions(now)
        self.handle_player_collisions()
        self.expire_powerup(now)

    def update_boss_state(self):
        if BossLifecycle.is_active(self.enemy_group):
            BossLifecycle.prepare_boss_fight(
                self.enemy_group,
                self.powerup_group,
            )
            self.deactivate_powerups()

    def start_boss(self):
        BossLifecycle.prepare_boss_fight(
            self.enemy_group,
            self.powerup_group,
        )
        self.deactivate_powerups()
        spawn_boss(self.all_sprites, self.enemy_group)
        self.boss_spawned = True

    def handle_enemy_collisions(self):
        if self.powerup_active:
            collisions = pygame.sprite.groupcollide(
                self.shot_group,
                self.enemy_group,
                False,
                False,
            )
            damage = 1
        else:
            collisions = pygame.sprite.groupcollide(
                self.shot_group,
                self.enemy_group,
                True,
                False,
            )
            damage = None

        for shot, enemies in collisions.items():
            for enemy in enemies:
                hit_damage = damage if damage is not None else shot.daño
                if enemy.receive_damage(hit_damage):
                    self.score += 50 if enemy.is_boss else 10
                    if enemy.is_boss:
                        self.boss_defeated = True
                        self.boss_spawned = False
                    elif random.random() < 0.1:
                        crear_powerup(self.all_sprites, self.powerup_group)

    def handle_powerup_collisions(self, now):
        collisions = pygame.sprite.groupcollide(
            self.shot_group,
            self.powerup_group,
            True,
            True,
        )
        for _, powerups in collisions.items():
            for powerup in powerups:
                self.activate_powerup(powerup.tipo, now)

        for powerup in pygame.sprite.spritecollide(
            self.player,
            self.powerup_group,
            True,
        ):
            self.activate_powerup(powerup.tipo, now)

    def activate_powerup(self, powerup_type, now):
        if not self.infinite_powerup:
            self.powerup_active = True
            self.powerup_started = now
            aplicar_powerup(self.player, powerup_type)

    def handle_player_collisions(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_group, True):
            self.player.vidas -= 1
            self.lives = self.player.vidas
            if self.lives <= 0:
                self.game_over = True

    def expire_powerup(self, now):
        if (
            self.powerup_active
            and not self.infinite_powerup
            and now - self.powerup_started > self.POWERUP_DURATION
        ):
            self.deactivate_powerups()

    def deactivate_powerups(self):
        for powerup in list(self.powerup_group):
            powerup.kill()
        self.powerup_active = False
        self.infinite_powerup = False
        self.player.powerup_activo = False
        self.player.rayo_disponible = False
        self.player.velocidad_disparo = 1
        self.player.cadencia_disparo = self.PLAYER_SHOT_INTERVAL
        self.player.ancho_rayo = 5

    def reset(self):
        self.all_sprites.empty()
        self.player_group.empty()
        self.enemy_group.empty()
        self.shot_group.empty()
        self.powerup_group.empty()
        self.player = Jugador()
        self.player.vidas = 3
        self.all_sprites.add(self.player)
        self.player_group.add(self.player)
        spawn_initial_enemies(self.all_sprites, self.enemy_group)
        self.lives = 3
        self.score = 0
        self.game_over = False
        self.boss_spawned = False
        self.boss_defeated = False

    def draw(self, now):
        self.screen.fill(NEGRO)
        self.all_sprites.draw(self.screen)
        for enemy in self.enemy_group:
            enemy.draw_health(self.screen)

        mostrar_vidas(self.screen, self.lives)
        mostrar_puntuacion(self.screen, self.score)
        self.draw_powerup_status(now)

        if self.game_over:
            if mostrar_game_over(self.screen, self.score):
                self.reset()
            else:
                self.running = False
        pygame.display.flip()

    def draw_powerup_status(self, now):
        if self.powerup_active and not self.infinite_powerup:
            remaining = (self.POWERUP_DURATION - (now - self.powerup_started)) / 1000
            if remaining > 0:
                self.draw_text(f"Power-up: {remaining:.1f}s")
        elif self.infinite_powerup:
            self.draw_text("Power-up: INFINITO")

    def draw_text(self, text):
        font = pygame.font.Font(None, 36)
        self.screen.blit(font.render(text, True, BLANCO), (10, ALTO - 40))


def cargar_record():
    try:
        with open("record.json", "r") as record_file:
            return json.load(record_file)["record"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        return 0


def guardar_record(record):
    with open("record.json", "w") as record_file:
        json.dump({"record": record}, record_file)


def main():
    Game().run()


if __name__ == "__main__":
    main()
