import pygame
import random
import os
from src.constants import *

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Cargar la imagen de Pereira
        try:
            self.image = pygame.image.load(os.path.join('img', 'Pereira.png'))
            self.image = pygame.transform.scale(self.image, (60, 60))  # Enemigos más grandes
        except:
            # Si no se encuentra la imagen, usar un rectángulo rojo
            self.image = pygame.Surface((60, 60))
            self.image.fill(ROJO)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 1.2  # Velocidad de descenso ajustada
        self.vida = 1  # Vida inicial del enemigo
        self.es_jefe = False  # Para identificar si es un enemigo normal o jefe

    def recibir_daño(self, daño, es_rayo=False):
        """Reduce la vida del enemigo y retorna True si muere"""
        if es_rayo:
            self.vida -= 1  # El rayo quita 1 de vida a todos los enemigos
        else:
            self.vida -= daño
            
        if self.vida <= 0:
            self.kill()
            return True
        return False

    def dibujar_vida(self, pantalla):
        """Dibuja la barra de vida del enemigo (solo para jefes)"""
        if self.es_jefe:
            # Calcular el ancho de la barra de vida
            ancho_barra = 40
            alto_barra = 5
            x = self.rect.x + (self.rect.width - ancho_barra) // 2
            y = self.rect.y - 10

            # Dibujar fondo de la barra (gris)
            pygame.draw.rect(pantalla, GRIS, (x, y, ancho_barra, alto_barra))
            
            # Dibujar la vida actual (verde)
            vida_actual = (self.vida / self.vida_maxima) * ancho_barra
            pygame.draw.rect(pantalla, VERDE, (x, y, vida_actual, alto_barra))

    def update(self, jugador):
        # Solo movimiento vertical hacia abajo
        self.rect.y += self.velocidad
        
        # Si pasa por debajo del jugador, eliminar y quitar una vida
        if self.rect.top > jugador.rect.bottom:
            jugador.vidas -= 1
            self.kill()

class Jefe(Enemigo):
    def __init__(self, x, y):
        super().__init__(x, y)
        # Cargar la imagen del castor
        try:
            self.image = pygame.image.load(os.path.join('img', 'Castor.png'))
            self.image = pygame.transform.scale(self.image, (180, 180))  # Jefe mucho más grande
        except Exception as e:
            print(f"Error al cargar imagen del jefe: {e}")
            # Si no se encuentra la imagen, usar un rectángulo rojo brillante
            self.image = pygame.Surface((180, 180))
            self.image.fill((255, 0, 0))  # Rojo brillante
            # Dibujar una X para hacerlo más visible
            pygame.draw.line(self.image, (255, 255, 255), (0, 0), (180, 180), 5)
            pygame.draw.line(self.image, (255, 255, 255), (0, 180), (180, 0), 5)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 0.3  # Velocidad más lenta
        self.vida = 20  # Vida inicial del jefe
        self.vida_maxima = 20  # Vida máxima para la barra de vida
        self.es_jefe = True
        self.velocidad_x = 2  # Velocidad horizontal
        self.direccion = 1  # 1 para derecha, -1 para izquierda

    def update(self, jugador):
        # Movimiento horizontal
        self.rect.x += self.velocidad_x * self.direccion
        
        # Cambiar dirección al llegar a los bordes
        if self.rect.right > ANCHO:
            self.direccion = -1
        elif self.rect.left < 0:
            self.direccion = 1
            
        # Movimiento vertical más lento
        self.rect.y += self.velocidad
        
        # Si pasa por debajo del jugador, eliminar y quitar una vida
        if self.rect.top > jugador.rect.bottom:
            jugador.vidas -= 1
            self.kill()

def crear_enemigos(grupo_todos, grupo_enemigos):
    # Crear solo 3 enemigos iniciales en columnas aleatorias
    espacio_horizontal = ANCHO // 8
    columnas_usadas = random.sample(range(8), 3)  # Seleccionar 3 columnas aleatorias
    for columna in columnas_usadas:
        x = columna * espacio_horizontal + (espacio_horizontal - 60) // 2  # Centrar en la columna
        enemigo = Enemigo(x, -60)  # Empezar arriba de la pantalla
        grupo_todos.add(enemigo)
        grupo_enemigos.add(enemigo)

def crear_jefe(grupo_todos, grupo_enemigos):
    """Crea un jefe en la parte superior de la pantalla"""
    print("Intentando crear jefe...")
    x = ANCHO // 2 - 90  # Centrar horizontalmente (ajustado para el nuevo tamaño)
    print(f"Posición X del jefe: {x}")
    jefe = Jefe(x, 50)  # Empezar más abajo
    print("Jefe creado, añadiendo a grupos...")
    grupo_todos.add(jefe)
    grupo_enemigos.add(jefe)
    print("Jefe añadido a los grupos correctamente")

def mover_enemigos(grupo_enemigos, jugador):
    # Actualizar posición de todos los enemigos
    for enemigo in grupo_enemigos:
        enemigo.update(jugador)

def crear_nuevo_enemigo(grupo_todos, grupo_enemigos):
    # Crear un nuevo enemigo en una columna aleatoria
    espacio_horizontal = ANCHO // 8
    columna = random.randint(0, 7)
    x = columna * espacio_horizontal + (espacio_horizontal - 60) // 2  # Centrar en la columna
    enemigo = Enemigo(x, -60)  # Empezar arriba de la pantalla
    grupo_todos.add(enemigo)
    grupo_enemigos.add(enemigo) 