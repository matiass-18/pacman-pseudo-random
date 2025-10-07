import pygame, os, config
from rng import rand_choice

STATE_NORMAL=0; STATE_FRIGHTENED=1; STATE_EATEN=2

class Ghost:
    def __init__(self, col, row, name, color=(255,0,0), speed_mult=1.0):
        self.size = config.TILE_SIZE
        self.home = (col * config.TILE_SIZE, row * config.TILE_SIZE)
        self.rect = pygame.Rect(self.home[0], self.home[1], self.size, self.size)
        self.state = STATE_NORMAL
        self.direction = (0, 0)
        self.name = name
        self.color = color
        self.speed_mult = speed_mult
        self.frightened_until = 0
        self.eaten_target = self.home
        self.image = self._load_image_or_rect()

    def _load_image_or_rect(self):
        path = config.asset_path(f'assets/images/ghost_{self.name}.png')
        if os.path.exists(path):
            surf = pygame.image.load(path).convert_alpha()
            return pygame.transform.smoothscale(surf, (self.size, self.size))
        s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(s, self.color, (0, 0, self.size, self.size), border_radius=6)
        return s

    def speed(self):
        if self.state == STATE_EATEN:
            return config.GHOST_EATEN_SPEED * self.speed_mult
        if self.state == STATE_FRIGHTENED:
            return config.GHOST_FRIGHTENED_SPEED * self.speed_mult
        return config.GHOST_BASE_SPEED * self.speed_mult

    def set_frightened(self, now):
        self.state = STATE_FRIGHTENED
        self.frightened_until = max(self.frightened_until, now) + config.POWER_DURATION_MS

    def update_state(self, now):
        if self.state == STATE_FRIGHTENED and now >= self.frightened_until:
            self.state = STATE_NORMAL
        if self.state == STATE_EATEN and self.rect.topleft == self.eaten_target:
            self.state = STATE_NORMAL

    def is_aligned_with_grid(self):
        return (self.rect.x % config.TILE_SIZE == 0) and (self.rect.y % config.TILE_SIZE == 0)

    def get_valid_directions(self, maze):
        all_directions = [(1,0), (-1,0), (0,1), (0,-1)]
        valid = []
        for d in all_directions:
            test_rect = self.rect.copy()
            test_rect.x += d[0]
            test_rect.y += d[1]
            if not any(w.colliderect(test_rect) for w in maze.walls):
                valid.append(d)
        return valid

    def move(self, maze, now):
        self.update_state(now)
        step = self.speed()

        # Si está alineado, decide dirección normalmente
        if self.is_aligned_with_grid():
            valid_dirs = self.get_valid_directions(maze)
            if len(valid_dirs) > 1 and self.direction in valid_dirs:
                opp = (-self.direction[0], -self.direction[1])
                if opp in valid_dirs:
                    valid_dirs.remove(opp)
            if valid_dirs:
                self.direction = rand_choice(valid_dirs)
            else:
                self.direction = (0, 0)

        # Si está detenido, intenta buscar dirección aunque no esté alineado
        if self.direction == (0, 0):
            # Forzar alineación a la grilla más cercana
            self.rect.x = round(self.rect.x / config.TILE_SIZE) * config.TILE_SIZE
            self.rect.y = round(self.rect.y / config.TILE_SIZE) * config.TILE_SIZE
            valid_dirs = self.get_valid_directions(maze)
            if valid_dirs:
                self.direction = rand_choice(valid_dirs)
            else:
                return  # Sigue sin poder moverse

        # Intentar moverse
        next_rect = self.rect.copy()
        next_rect.x += int(self.direction[0] * step)
        next_rect.y += int(self.direction[1] * step)
        if not any(w.colliderect(next_rect) for w in maze.walls):
            self.rect = next_rect
        else:
            # Si choca, se detiene y decidirá nueva dirección en el próximo frame
            self.direction = (0, 0)

    def draw(self, surf):
        if self.state == STATE_FRIGHTENED:
            base = self.image.copy()
            s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            s.fill((0, 0, 255, 120))
            surf.blit(base, self.rect)
            surf.blit(s, self.rect)
        elif self.state == STATE_EATEN:
            pygame.draw.rect(surf, (160, 160, 160), self.rect, border_radius=6)
        else:
            surf.blit(self.image, self.rect)