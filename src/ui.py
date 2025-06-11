import pygame
from src.constants import *

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_normal, color_hover):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_actual = color_normal
        self.fuente = FUENTE_NORMAL

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color_actual, self.rect)
        pygame.draw.rect(superficie, BLANCO, self.rect, 2)
        
        texto_surface = self.fuente.render(self.texto, True, BLANCO)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        superficie.blit(texto_surface, texto_rect)

    def actualizar(self, pos_mouse):
        if self.rect.collidepoint(pos_mouse):
            self.color_actual = self.color_hover
        else:
            self.color_actual = self.color_normal

    def esta_sobre(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)

def mostrar_vidas(pantalla, vidas):
    """Muestra el número de vidas restantes"""
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(f"Vidas: {vidas}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

def mostrar_puntuacion(pantalla, puntuacion):
    """Muestra la puntuación actual"""
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(f"Puntos: {puntuacion}", True, BLANCO)
    pantalla.blit(texto, (ANCHO - 150, 10))

def mostrar_game_over(pantalla, puntuacion):
    """Muestra la pantalla de game over con un botón de volver a jugar"""
    # Crear el botón
    boton_rect = pygame.Rect(ANCHO//2 - 100, ALTO//2 + 50, 200, 50)
    boton_color = (0, 255, 0)  # Verde
    boton_color_hover = (0, 200, 0)  # Verde más oscuro
    color_actual = boton_color

    # Bucle de la pantalla de game over
    esperando = True
    while esperando:
        # Obtener posición del mouse
        mouse_pos = pygame.mouse.get_pos()
        
        # Actualizar color del botón
        if boton_rect.collidepoint(mouse_pos):
            color_actual = boton_color_hover
        else:
            color_actual = boton_color

        # Dibujar fondo
        pantalla.fill(NEGRO)
        
        # Dibujar texto de Game Over
        fuente = pygame.font.Font(None, 74)
        texto = fuente.render("GAME OVER", True, ROJO)
        texto_rect = texto.get_rect(center=(ANCHO/2, ALTO/3))
        pantalla.blit(texto, texto_rect)
        
        # Dibujar puntuación
        fuente_puntos = pygame.font.Font(None, 36)
        texto_puntos = fuente_puntos.render(f"Puntuación final: {puntuacion}", True, BLANCO)
        texto_puntos_rect = texto_puntos.get_rect(center=(ANCHO/2, ALTO/3 + 50))
        pantalla.blit(texto_puntos, texto_puntos_rect)
        
        # Dibujar botón
        pygame.draw.rect(pantalla, color_actual, boton_rect)
        pygame.draw.rect(pantalla, BLANCO, boton_rect, 2)  # Borde blanco
        
        # Dibujar texto del botón
        texto_boton = fuente_puntos.render("Volver a Jugar", True, BLANCO)
        texto_boton_rect = texto_boton.get_rect(center=boton_rect.center)
        pantalla.blit(texto_boton, texto_boton_rect)
        
        # Actualizar pantalla
        pygame.display.flip()
        
        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False  # Salir del juego
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(mouse_pos):
                    return True  # Volver a jugar
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True  # Volver a jugar con la tecla R
                elif evento.key == pygame.K_ESCAPE:
                    return False  # Salir con ESC
    
    return False

def mostrar_game_over_con_botones(puntuacion, record):
    # Crear botones
    boton_jugar = Boton(ANCHO//2 - 100, ALTO//2, 200, 50, "Jugar de nuevo", VERDE, (0, 200, 0))
    boton_salir = Boton(ANCHO//2 - 100, ALTO//2 + 70, 200, 50, "Salir", ROJO, (200, 0, 0))
    
    ejecutando = True
    while ejecutando:
        PANTALLA.fill(NEGRO)
        
        # Dibujar título
        texto_game_over = FUENTE_TITULO.render("GAME OVER", True, ROJO)
        texto_rect = texto_game_over.get_rect(center=(ANCHO//2, ALTO//4))
        PANTALLA.blit(texto_game_over, texto_rect)
        
        # Dibujar puntuación
        texto_puntuacion = FUENTE_NORMAL.render(f"Puntuación: {puntuacion}", True, BLANCO)
        texto_record = FUENTE_NORMAL.render(f"Record: {record}", True, AMARILLO)
        PANTALLA.blit(texto_puntuacion, (ANCHO//2 - texto_puntuacion.get_width()//2, ALTO//3))
        PANTALLA.blit(texto_record, (ANCHO//2 - texto_record.get_width()//2, ALTO//3 + 40))
        
        # Actualizar y dibujar botones
        pos_mouse = pygame.mouse.get_pos()
        boton_jugar.actualizar(pos_mouse)
        boton_salir.actualizar(pos_mouse)
        boton_jugar.dibujar(PANTALLA)
        boton_salir.dibujar(PANTALLA)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.esta_sobre(pos_mouse):
                    return "jugar"
                if boton_salir.esta_sobre(pos_mouse):
                    return "salir"
        
        pygame.display.flip()
        RELOJ.tick(FPS) 