import pygame
import config

class Maze:
    def __init__(self, layout):
        self.layout = layout
        self.walls = []
        self.dots = []
        
        # Creamos las superficies para las paredes y puntos (mejora visual)
        self.wall_surface = pygame.Surface((config.TILE_SIZE, config.TILE_SIZE))
        self.wall_surface.fill((0, 0, 255)) # Color azul
        
        self.dot_surface = pygame.Surface((4, 4))
        self.dot_surface.fill(config.DOT_COLOR)

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * config.TILE_SIZE
                y = row_index * config.TILE_SIZE
                
                if cell == 1:
                    wall_rect = pygame.Rect(x, y, config.TILE_SIZE, config.TILE_SIZE)
                    self.walls.append(wall_rect)
                elif cell == 0:
                    dot_rect = pygame.Rect(x + config.TILE_SIZE // 2 - 2, 
                                          y + config.TILE_SIZE // 2 - 2, 
                                          4, 4)
                    self.dots.append(dot_rect)

    def draw(self, surface):
        for wall in self.walls:
            surface.blit(self.wall_surface, wall)
        for dot in self.dots:
            surface.blit(self.dot_surface, dot)