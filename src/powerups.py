import pygame
from src.constants import ALTO, AMARILLO, ANCHO

def crear_powerup(grupo_todos, grupo_powerups):
    """Crea un powerup en una posición aleatoria en la parte superior"""
    espacio_horizontal = ANCHO // 8
    columna = random.randint(0, 7)
    x = columna * espacio_horizontal + (espacio_horizontal - 30) // 2  # Centrar en la columna
    powerup = PowerUp(x, -30)  # Empezar arriba de la pantalla
    grupo_todos.add(powerup)
    grupo_powerups.add(powerup)

def aplicar_powerup(jugador, tipo):
    """Aplica el efecto del powerup al jugador"""
    if tipo == "rayo":
        jugador.velocidad_disparo = 2
        jugador.cadencia_disparo = 250
        jugador.ancho_rayo = ANCHO // 2  # Rayo muy ancho (media pantalla)
        jugador.powerup_activo = True

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(AMARILLO)
        # Dibujar una estrella
        pygame.draw.polygon(self.image, AMARILLO, [
            (10, 0), (13, 7), (20, 7), (15, 12),
            (17, 19), (10, 15), (3, 19), (5, 12),
            (0, 7), (7, 7)
        ])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad_y = 2
        self.tipo = "rayo"  # Por ahora solo tenemos un tipo de powerup

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top > ALTO:
            self.kill()
