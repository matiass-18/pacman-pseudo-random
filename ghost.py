import pygame
import config

class Ghost:
    def __init__(self, x_tile, y_tile, color):
        self.size = config.TILE_SIZE
        self.rect = pygame.Rect(x_tile * self.size, y_tile * self.size, self.size, self.size)
        
        self.start_pos = (x_tile * self.size, y_tile * self.size)
        self.color = color
        
        self.speed = 2
        
        self.direction = (0, 0)
        self.next_direction = (0,0)

    def reset_position(self):
        """ Coloca al fantasma de nuevo en su posición inicial. """
        self.rect.topleft = self.start_pos
        self.direction = (0, 0)

    def move(self, maze, motor_aleatorio):
        # Si el fantasma está alineado, es un punto de decisión.
        if self.is_aligned_with_grid():
            # 1. Obtener todas las direcciones posibles que no son paredes.
            valid_directions = self.get_valid_directions(maze)
            
            # 2. Lógica de decisión
            # Si solo hay una salida (callejón sin salida), la toma.
            if len(valid_directions) == 1:
                self.direction = valid_directions[0]
            # Si hay múltiples salidas, elige una al azar, evitando darse la vuelta.
            elif len(valid_directions) > 1:
                opposite_direction = (-self.direction[0], -self.direction[1])
                if opposite_direction in valid_directions:
                    valid_directions.remove(opposite_direction)
                
                # Usamos el motor aleatorio para elegir
                choice = motor_aleatorio.siguiente_numero(0, len(valid_directions) - 1)
                self.direction = valid_directions[choice]

        # Mueve el fantasma en la dirección determinada
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

    def is_aligned_with_grid(self):
        """ Verifica si el fantasma está en una celda exacta de la cuadrícula. """
        return (self.rect.x % config.TILE_SIZE == 0) and \
               (self.rect.y % config.TILE_SIZE == 0)

    def get_valid_directions(self, maze):
        """ Revisa los 4 caminos y devuelve una lista de los que están libres. """
        all_directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (0,0)] # Arriba, Abajo, Izq, Der
        valid = []
        for direction in all_directions:
            test_rect = self.rect.copy()
            test_rect.x += direction[0]
            test_rect.y += direction[1]
            
            is_wall = False
            for wall in maze.walls:
                if test_rect.colliderect(wall):
                    is_wall = True
                    break
            if not is_wall:
                valid.append(direction)
        return valid

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)