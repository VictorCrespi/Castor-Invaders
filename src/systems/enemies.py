def update_enemies(enemy_group, player):
    for enemy in enemy_group:
        enemy.update(player)
