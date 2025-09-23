import pygame
import config

class Maze:
    def __init__(self, layout):
        self.layout = layout
        self.walls = []
        self.dots = [] # Nueva lista para los puntos
        self.wall_color = (0, 0, 255)

        # Recorremos el mapa para crear paredes y puntos
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * config.TILE_SIZE
                y = row_index * config.TILE_SIZE
                
                if cell == 1: # Si es una pared
                    wall_rect = pygame.Rect(x, y, config.TILE_SIZE, config.TILE_SIZE)
                    self.walls.append(wall_rect)
                elif cell == 0: # Si es un camino, creamos un punto
                    # Hacemos el punto más pequeño que la celda y lo centramos
                    dot_rect = pygame.Rect(x + config.TILE_SIZE // 2 - 2, 
                                          y + config.TILE_SIZE // 2 - 2, 
                                          4, 4) # Un punto de 4x4 píxeles
                    self.dots.append(dot_rect)

    def draw(self, surface):
        # Dibujamos las paredes
        for wall in self.walls:
            pygame.draw.rect(surface, self.wall_color, wall)
        # Dibujamos los puntos
        for dot in self.dots:
            pygame.draw.rect(surface, config.DOT_COLOR, dot)