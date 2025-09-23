import pygame
import config

class Player:
    def __init__(self, x_tile, y_tile):
        self.size = config.TILE_SIZE
        self.rect = pygame.Rect(x_tile * self.size, y_tile * self.size, self.size, self.size)
        
        # Guardamos la posición inicial para el método reset
        self.start_pos = (x_tile * self.size, y_tile * self.size)
        self.lives = config.PLAYER_LIVES
        
        self.color = (255, 255, 0)
        # USA UNA VELOCIDAD QUE SEA DIVISOR DE TILE_SIZE (40)
        self.speed = 2 
        
        self.direction = (0, 0)
        self.next_direction = (0, 0)

    def reset_position(self):
        """ Coloca al jugador de nuevo en su posición inicial. """
        self.rect.topleft = self.start_pos
        self.direction = (0, 0)
        self.next_direction = (0, 0)

    def change_direction(self, new_direction):
        """ Guarda la próxima dirección que el jugador quiere tomar. """
        self.next_direction = new_direction

    def move(self, maze):
        # --- 1. LÓGICA DE GIRO Y REVERSA ---
        # Reversa instantánea
        if self.next_direction == (-self.direction[0], -self.direction[1]):
            self.direction = self.next_direction
            self.next_direction = (0, 0)

        # Intento de giro en intersección
        # Como la velocidad es un divisor, la posición siempre será un múltiplo de TILE_SIZE en las intersecciones
        if (self.rect.x % config.TILE_SIZE == 0) and (self.rect.y % config.TILE_SIZE == 0):
            if self.next_direction != (0, 0) and self.can_turn(self.next_direction, maze):
                self.direction = self.next_direction
                self.next_direction = (0, 0)

        # --- 2. LÓGICA DE MOVIMIENTO Y COLISIÓN ---
        if self.direction == (0, 0):
            return

        # Movemos el rect directamente. Ya no necesitamos x, y flotantes.
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # La lógica de colisión es más simple ahora
        for wall in maze.walls:
            if self.rect.colliderect(wall):
                if self.direction[0] > 0: self.rect.right = wall.left
                elif self.direction[0] < 0: self.rect.left = wall.right
                if self.direction[1] > 0: self.rect.bottom = wall.top
                elif self.direction[1] < 0: self.rect.top = wall.bottom

    def can_turn(self, direction, maze):
        """ Verifica si un giro a una nueva dirección es posible. """
        test_rect = self.rect.copy()
        test_rect.x += direction[0]
        test_rect.y += direction[1]
        
        for wall in maze.walls:
            if test_rect.colliderect(wall):
                return False
        return True

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def eat_dots(self, maze):
        score_added = 0
        collided_indices = self.rect.collidelistall(maze.dots)
        if collided_indices:
            for index in sorted(collided_indices, reverse=True):
                del maze.dots[index]
                score_added += 10
        return score_added