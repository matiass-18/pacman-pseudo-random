import pygame
import config

class Ghost:
    def __init__(self, x_tile, y_tile, color_name, speed): # Añadimos 'speed'
        self.size = config.TILE_SIZE
        self.rect = pygame.Rect(x_tile * self.size, y_tile * self.size, self.size, self.size)
        
        # Cargamos la imagen basándonos en el nombre del color
        image_path = f'assets/images/ghost_{color_name}.png'
        original_image = pygame.image.load(image_path).convert_alpha()
        # La escalamos al tamaño de nuestra celda
        self.image = pygame.transform.scale(original_image, (self.size, self.size))

        # Guardamos el color original para el modo "asustado"
        self.normal_color_image = self.image # Guardamos la imagen original
        # (El resto del código para el modo asustado necesitará usar imágenes también)

        # El resto del método se queda igual
        self.start_pos = (self.rect.x, self.rect.y)
        self.speed = speed
        self.direction = (0, 0)

    def reset_position(self):
        """ Coloca al fantasma de nuevo en su posición inicial. """
        self.rect.topleft = self.start_pos
        self.direction = (0, 0)

    def move(self, maze, motor_aleatorio):
        # --- LÓGICA DE DECISIÓN EN INTERSECCIONES ---
        # Si el fantasma está alineado, es un punto de decisión.
        if self.is_aligned_with_grid():
            # 1. Obtiene todas las direcciones válidas (sin paredes).
            valid_directions = self.get_valid_directions(maze)
            
            # 2. Evita darse la vuelta a menos que no haya otra opción.
            if len(valid_directions) > 1:
                opposite_direction = (-self.direction[0], -self.direction[1])
                if opposite_direction in valid_directions:
                    valid_directions.remove(opposite_direction)
            
            # 3. Usa el motor aleatorio para elegir una de las salidas válidas.
            if valid_directions:
                choice = motor_aleatorio.siguiente_numero(0, len(valid_directions) - 1)
                self.direction = valid_directions[choice]

        # --- LÓGICA DE MOVIMIENTO Y COLISIÓN (similar a la del jugador) ---
        if self.direction == (0, 0):
            return

        # Creamos un rectángulo de prueba para el próximo movimiento
        next_rect = self.rect.copy()
        next_rect.x += self.direction[0] * self.speed
        next_rect.y += self.direction[1] * self.speed
        
        collided = False
        for wall in maze.walls:
            if next_rect.colliderect(wall):
                collided = True
                # Si choca, se detiene en seco en lugar de atravesar la pared
                self.direction = (0, 0)
                break
        
        # Solo nos movemos si el camino está libre
        if not collided:
            self.rect = next_rect

    def is_aligned_with_grid(self):
        """ Verifica si el fantasma está en una celda exacta de la cuadrícula. """
        return (self.rect.x % config.TILE_SIZE == 0) and \
               (self.rect.y % config.TILE_SIZE == 0)

    def get_valid_directions(self, maze):
        """ Revisa los 4 caminos y devuelve una lista de los que están libres. """
        all_directions = [(0, -1), (0, 1), (-1, 0), (1, 0)] # Arriba, Abajo, Izq, Der
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
        surface.blit(self.image, self.rect)