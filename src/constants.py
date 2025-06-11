import pygame

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 600

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
GRIS = (128, 128, 128)

# Configuración del juego
FPS = 60
VIDAS_INICIALES = 3
PUNTOS_ENEMIGO = 100
CADENCIA_DISPARO = 250  # milisegundos entre disparos
RETRASO_DISPARO = 250  # milisegundos entre disparos (alias para compatibilidad)
PROBABILIDAD_POWERUP = 0.1  # 10% de probabilidad de soltar power-up

# Configuración de power-ups
DURACION_POWERUP = 5000  # 5 segundos
DURACION_POWER_UP = 5000  # 5 segundos (alias para compatibilidad)
VELOCIDAD_POWERUP = 3

# Configuración de enemigos
VELOCIDAD_ENEMIGO = 2
ESPACIO_HORIZONTAL = 60
ESPACIO_VERTICAL = 50

# Configuración de disparos
VELOCIDAD_DISPARO = 7
ANCHO_DISPARO = 5
ALTO_DISPARO = 15

# Configuración del jugador
VELOCIDAD_JUGADOR = 5
ANCHO_JUGADOR = 50
ALTO_JUGADOR = 40

# Configuración de la ventana
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders")
RELOJ = pygame.time.Clock()

# Fuentes
FUENTE_NORMAL = pygame.font.Font(None, 36)
FUENTE_TITULO = pygame.font.Font(None, 74)

# Configuración de proyectiles
VELOCIDAD_PROYECTIL = -10
ANCHO_RAYO = 100
DURACION_RAYO = 200  # milisegundos 