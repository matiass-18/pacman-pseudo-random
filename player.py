import pygame
import config

class Player:
    def __init__(self, x_tile, y_tile, speed):
        self.size = config.TILE_SIZE
        self.rect = pygame.Rect(x_tile * self.size, y_tile * self.size, self.size, self.size)
        
        # --- CARGA DE IMÁGENES DIRECCIONALES ---
        self.images = self.load_images()
        self.image = self.images[(1, 0)] # Imagen inicial (mirando a la derecha)
        
        self.start_pos = (self.rect.x, self.rect.y)
        self.lives = config.PLAYER_LIVES
        self.speed = speed
        
        self.direction = (0, 0)
        self.next_direction = (0, 0)

    def load_images(self):
        """ Carga todas las imágenes del jugador y las guarda en un diccionario. """
        images = {}
        # Cargamos las cuatro imágenes direccionales
        base_path = 'assets/images/'
        right = pygame.image.load(f'{base_path}punkman-right.png').convert_alpha()
        left = pygame.image.load(f'{base_path}punkman-left.png').convert_alpha()
        up = pygame.image.load(f'{base_path}punkman-up.png').convert_alpha()
        down = pygame.image.load(f'{base_path}punkman-down.png').convert_alpha()
        
        # Las escalamos y asignamos a su dirección correspondiente
        images[(1, 0)] = pygame.transform.scale(right, (self.size, self.size))   # Derecha
        images[(-1, 0)] = pygame.transform.scale(left, (self.size, self.size))   # Izquierda
        images[(0, -1)] = pygame.transform.scale(up, (self.size, self.size))     # Arriba
        images[(0, 1)] = pygame.transform.scale(down, (self.size, self.size))   # Abajo
        
        return images

    def update_image(self):
        """ Actualiza la imagen del jugador según su dirección actual. """
        if self.direction != (0, 0):
            self.image = self.images[self.direction]

    def reset_position(self):
        self.rect.topleft = self.start_pos
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.image = self.images[(1, 0)] # Reinicia a la imagen por defecto

    def change_direction(self, new_direction):
        self.next_direction = new_direction

    def move(self, maze):
        # --- MODIFICADO PARA ACTUALIZAR LA IMAGEN ---
        if (self.rect.x % config.TILE_SIZE == 0 and self.rect.y % config.TILE_SIZE == 0):
            # Reversa instantánea
            if self.next_direction == (-self.direction[0], -self.direction[1]):
                self.direction = self.next_direction
                self.update_image() # Actualizamos la imagen
            # Giro pendiente
            elif self.next_direction != (0,0):
                test_rect = self.rect.copy()
                test_rect.x += self.next_direction[0]
                test_rect.y += self.next_direction[1]
                if not any(wall.colliderect(test_rect) for wall in maze.walls):
                    self.direction = self.next_direction
                    self.update_image() # Actualizamos la imagen
        
        if self.direction == (0, 0): return

        next_rect = self.rect.copy()
        next_rect.x += self.direction[0] * self.speed
        next_rect.y += self.direction[1] * self.speed
        
        if not any(wall.colliderect(next_rect) for wall in maze.walls):
            self.rect = next_rect

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def eat_dots(self, maze):
        # ... (sin cambios)
        score_added = 0
        collided_indices = self.rect.collidelistall(maze.dots)
        if collided_indices:
            for index in sorted(collided_indices, reverse=True):
                del maze.dots[index]
                score_added += 10
        return score_added