import pygame, os, config

DIRS = {(1, 0): 'right', (-1, 0): 'left', (0, -1): 'up', (0, 1): 'down'}

class Player:
    def __init__(self, col, row, speed, skin_name):
        self.size = config.TILE_SIZE
        self.rect = pygame.Rect(col * self.size, row * self.size, self.size, self.size)
        
        self.start_pos = self.rect.topleft
        self.lives = config.PLAYER_LIVES
        self.speed = speed
        
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        
        # ...existing code...
        self.skin = config.SKINS.get(skin_name, config.SKINS[config.DEFAULT_SKIN_NAME])
        self.images = self._load_images_or_fallback()
        self.image = self.images[(1, 0)]  # Cambiado de 'right' a (1, 0)
# ...existing code...

    def _load_images_or_fallback(self):
        imgs = {}
        for dname in ['right', 'left', 'up', 'down']:
            path = self.skin.get(dname)
            if path and os.path.exists(config.asset_path(path)):
                surf = pygame.image.load(config.asset_path(path)).convert_alpha()
                vec = [k for k, v in DIRS.items() if v == dname][0]
                imgs[vec] = pygame.transform.smoothscale(surf, (self.size, self.size))
            else:
                s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                pygame.draw.circle(s, self.skin['color'], (self.size // 2, self.size // 2), self.size // 2 - 2)
                vec = [k for k, v in DIRS.items() if v == dname][0]
                imgs[vec] = s
        return imgs

    def reset_position(self):
        self.rect.topleft = self.start_pos
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.image = self.images[(1, 0)]

    def change_direction(self, d):
        self.next_direction = d

    def move(self, maze):
        # Permitir un margen de error de alineación (por ejemplo, 2 píxeles)
        align_margin = 2
        x_aligned = abs(self.rect.x % config.TILE_SIZE) <= align_margin
        y_aligned = abs(self.rect.y % config.TILE_SIZE) <= align_margin
        aligned = x_aligned and y_aligned

        # Si estamos casi alineados, forzamos alineación exacta
        if x_aligned:
            self.rect.x = round(self.rect.x / config.TILE_SIZE) * config.TILE_SIZE
        if y_aligned:
            self.rect.y = round(self.rect.y / config.TILE_SIZE) * config.TILE_SIZE

        # 1. Si estamos alineados, intentamos cambiar a la dirección deseada si es posible
        if aligned:
            # Reversa instantánea
            if self.next_direction == (-self.direction[0], -self.direction[1]):
                self.direction = self.next_direction
            # Giro o arranque si la celda está libre
            elif self.next_direction != (0, 0):
                test_rect = self.rect.copy()
                test_rect.x += self.next_direction[0]
                test_rect.y += self.next_direction[1]
                if not any(wall.colliderect(test_rect) for wall in maze.walls):
                    self.direction = self.next_direction

        # 2. Si estamos quietos, intentamos arrancar en cualquier frame si estamos alineados para esa dirección
        if self.direction == (0, 0) and self.next_direction != (0, 0):
            can_start = True
            if self.next_direction[0] != 0 and not y_aligned:
                can_start = False
            if self.next_direction[1] != 0 and not x_aligned:
                can_start = False
            if can_start:
                test_rect = self.rect.copy()
                test_rect.x += self.next_direction[0]
                test_rect.y += self.next_direction[1]
                if not any(wall.colliderect(test_rect) for wall in maze.walls):
                    self.direction = self.next_direction

        # 3. Si no hay dirección, no nos movemos
        if self.direction == (0, 0):
            return

        # 4. Intentamos avanzar en la dirección actual
        next_rect = self.rect.copy()
        next_rect.x += self.direction[0] * self.speed
        next_rect.y += self.direction[1] * self.speed

        # 5. Si hay pared, nos detenemos
        if any(wall.colliderect(next_rect) for wall in maze.walls):
            # Forzar alineación a la grilla al detenerse
            self.rect.x = round(self.rect.x / config.TILE_SIZE) * config.TILE_SIZE
            self.rect.y = round(self.rect.y / config.TILE_SIZE) * config.TILE_SIZE
            self.direction = (0, 0)
        else:
            self.rect = next_rect

        # 6. Actualizamos la imagen si corresponde
        if self.direction in self.images:
            self.image = self.images[self.direction]
            
    def _can_move_in_direction(self, direction, maze):
        if direction == (0, 0):
            return False

        # Solo permitir giro si está alineado en la grilla para esa dirección
        if direction[0] != 0 and self.rect.y % config.TILE_SIZE != 0:
            return False
        if direction[1] != 0 and self.rect.x % config.TILE_SIZE != 0:
            return False

        test_rect = self.rect.copy()
        test_rect.x += direction[0]
        test_rect.y += direction[1]

        return not any(wall.colliderect(test_rect) for wall in maze.walls)

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def eat(self, maze):
        # (Este método de tu amigo está perfecto, no se toca)
        points = 0; activated = False; got_shield = False
        idxs = self.rect.collidelistall(maze.dots)
        for i in sorted(idxs, reverse=True): del maze.dots[i]; points += 10
        pidxs = self.rect.collidelistall(maze.power_dots)
        for i in sorted(pidxs, reverse=True): del maze.power_dots[i]; points += 50; activated = True
        sidxs = self.rect.collidelistall(maze.shield_orbs)
        for i in sorted(sidxs, reverse=True): del maze.shield_orbs[i]; got_shield = True
        return points, activated, got_shield