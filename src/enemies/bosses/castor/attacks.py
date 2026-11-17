class CastorAttackPattern:
    """Patrones del Castor aislados para poder añadir ataques nuevos."""

    def update(self, boss, player):
        boss.rect.x += boss.horizontal_speed * boss.direction
        boss.keep_inside_screen()
        boss.rect.y += boss.vertical_speed
        if boss.rect.top > player.rect.bottom:
            player.vidas -= 1
            boss.kill()
