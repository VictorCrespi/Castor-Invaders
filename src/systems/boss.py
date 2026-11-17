class BossLifecycle:
    """Gestiona las reglas globales que se aplican mientras hay un boss."""

    @staticmethod
    def is_active(enemy_group):
        return any(enemy.is_boss for enemy in enemy_group)

    @staticmethod
    def prepare_boss_fight(enemy_group, powerup_group):
        for enemy in list(enemy_group):
            if not enemy.is_boss:
                enemy.kill()
        for powerup in list(powerup_group):
            powerup.kill()
