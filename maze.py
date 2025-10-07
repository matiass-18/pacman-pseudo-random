import pygame, config

class Maze:
    def __init__(self, layout):
        self.layout = layout
        self.walls = []
        self.dots = []
        self.power_dots = []   # 2 o 3
        self.shield_orbs = []  # 4
        self.free_tiles = []
        wall = pygame.Surface((config.TILE_SIZE, config.TILE_SIZE))
        wall.fill(config.WALL_COLOR)
        self.wall_surface = wall
        self.dot_surface = pygame.Surface((4,4), pygame.SRCALPHA)
        pygame.draw.circle(self.dot_surface, config.DOT_COLOR, (2,2), 2)
        self.power_surface = pygame.Surface((16,16), pygame.SRCALPHA)
        pygame.draw.circle(self.power_surface, (255,255,255,110), (8,8), 8)
        pygame.draw.circle(self.power_surface, config.POWER_DOT_COLOR, (8,8), 5)
        self.shield_surface = pygame.Surface((16,16), pygame.SRCALPHA)
        pygame.draw.circle(self.shield_surface, (200,225,255,110), (8,8), 8)
        pygame.draw.circle(self.shield_surface, config.SHIELD_ORB_COLOR, (8,8), 5)

        for r,row in enumerate(layout):
            for c,cell in enumerate(row):
                x,y = c*config.TILE_SIZE, r*config.TILE_SIZE
                if cell == 1:
                    self.walls.append(pygame.Rect(x,y,config.TILE_SIZE,config.TILE_SIZE))
                elif cell == 0:
                    self.dots.append(pygame.Rect(x+config.TILE_SIZE//2-2, y+config.TILE_SIZE//2-2, 4,4))
                    self.free_tiles.append((c,r))
                elif cell in (2,3):
                    self.power_dots.append(pygame.Rect(x+config.TILE_SIZE//2-8, y+config.TILE_SIZE//2-8, 16,16))
                elif cell == 4:
                    self.shield_orbs.append(pygame.Rect(x+config.TILE_SIZE//2-8, y+config.TILE_SIZE//2-8, 16,16))

        if len(self.power_dots)==0 and len(self.dots)>=4:
            corners=[(0,0),(len(layout[0])*config.TILE_SIZE,0),(0,len(layout)*config.TILE_SIZE),(len(layout[0])*config.TILE_SIZE,len(layout)*config.TILE_SIZE)]
            idxs=set()
            for cx,cy in corners:
                best_i=None; best_d=1e18
                for i,d in enumerate(self.dots):
                    if i in idxs: continue
                    dx,dy = d.centerx-cx, d.centery-cy
                    dist = dx*dx+dy*dy
                    if dist < best_d: best_d=dist; best_i=i
                if best_i is not None: idxs.add(best_i)
            for i in sorted(idxs, reverse=True):
                d=self.dots[i]; del self.dots[i]
                self.power_dots.append(pygame.Rect(d.centerx-8, d.centery-8, 16,16))

    def draw(self, surf):
        for w in self.walls: surf.blit(self.wall_surface, w)
        for d in self.dots: surf.blit(self.dot_surface, d)
        for p in self.power_dots: surf.blit(self.power_surface, p)
        for s in self.shield_orbs: surf.blit(self.shield_surface, s)
