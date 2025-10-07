import os, sys, pygame
from rng import rand_choice, rand_int
import config, maps
from maze import Maze
from player import Player
from ghost import Ghost
import leaderboard
from collections import deque

pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
pygame.display.set_caption(config.GAME_TITLE)

def draw_text(surf, txt, size, x, y, color):
    font = pygame.font.Font(None, size)
    t = font.render(txt, True, color)
    r = t.get_rect(center=(x, y))
    surf.blit(t, r)

def load_skin_preview(name):
    skin = config.SKINS.get(name, list(config.SKINS.values())[0])
    size = config.TILE_SIZE * 2
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    img_path = skin.get("right")
    try:
        if img_path and os.path.exists(config.asset_path(img_path)):
            img = pygame.image.load(config.asset_path(img_path)).convert_alpha()
            img = pygame.transform.smoothscale(img, (size, size))
            surf.blit(img, (0,0))
        else:
            pygame.draw.circle(surf, skin.get("color", (255,255,0)), (size//2, size//2), size//2 - 2)
    except Exception:
        pygame.draw.circle(surf, skin.get("color", (255,255,0)), (size//2, size//2), size//2 - 2)
    return surf

def make_map_thumbnail(layout, max_w=520, max_h=340):
    rows, cols = len(layout), len(layout[0])
    scale = max(2, int(min(max_w/cols, max_h/rows)))
    w, h = cols*scale, rows*scale
    thumb = pygame.Surface((w, h))
    thumb.fill((20, 20, 40))
    wall = pygame.Surface((scale, scale)); wall.fill((0, 0, 0))
    for r, row in enumerate(layout):
        for c, cell in enumerate(row):
            x, y = c*scale, r*scale
            if cell == 1:
                thumb.blit(wall, (x, y))
            elif cell == 0:
                pygame.draw.rect(thumb, (230,230,230), (x+scale//2-1, y+scale//2-1, 2, 2))
            elif cell in (2, 3):
                pygame.draw.rect(thumb, (255,184,151), (x+scale//2-2, y+scale//2-2, 4, 4))
            elif cell == 4:
                pygame.draw.rect(thumb, (80,170,255), (x+scale//2-2, y+scale//2-2, 4, 4))
    return thumb

def draw_bar(surf, x, y, w, h, pct, bg=(40,40,40), fg=(0,220,255)):
    pygame.draw.rect(surf, bg, (x,y,w,h))
    pygame.draw.rect(surf, fg, (x, y, int(w*max(0,min(1,pct))), h))

def star_rating(elapsed_sec, map_name):
    th = config.STAR_THRESHOLDS_SEC.get(map_name, config.STAR_THRESHOLDS_SEC.get('default', [60,90,140]))
    if elapsed_sec <= th[0]: return 3
    if elapsed_sec <= th[1]: return 2
    if elapsed_sec <= th[2]: return 1
    return 0

DIFFICULTIES = {
    "Fácil":  {"ghost_mult": 0.85, "player_mult": 1.00, "ghost_count": 2},
    "Medio":  {"ghost_mult": 1.00, "player_mult": 1.00, "ghost_count": 4},
    "Difícil":{"ghost_mult": 1.25, "player_mult": 1.05, "ghost_count": 4},
}

def skin_menu(screen):
    names=list(config.SKINS.keys()); i=0
    previews = {n:load_skin_preview(n) for n in names}
    while True:
        screen.fill(config.BG_COLOR)
        draw_text(screen, "Elige Skin ", 56, screen.get_width()/2, 80, (255,255,0))
        draw_text(screen, names[i], 44, screen.get_width()/2, 150, (200,200,200))
        pv=previews[names[i]]; r=pv.get_rect(center=(screen.get_width()/2,280)); screen.blit(pv,r)
        draw_text(screen, "Enter para continuar", 28, screen.get_width()/2, 360, (160,160,160))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_LEFT: i=(i-1)%len(names)
                if e.key==pygame.K_RIGHT: i=(i+1)%len(names)
                if e.key==pygame.K_RETURN: return names[i]

def difficulty_menu(screen):
    names=list(DIFFICULTIES.keys()); i=names.index("Medio")
    while True:
        screen.fill(config.BG_COLOR)
        draw_text(screen,"Dificultad ",56,screen.get_width()/2,100,(255,255,0))
        for k,n in enumerate(names):
            color=(255,255,0) if k==i else (200,200,200)
            opt=DIFFICULTIES[n]; txt=f"{n} | Fantasmas: {opt['ghost_count']} | Vel x{opt['ghost_mult']}"
            draw_text(screen, txt, 32, screen.get_width()/2, 180+k*40, color)
        draw_text(screen,"Enter para continuar",28,screen.get_width()/2, 180+len(names)*40+30,(160,160,160))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_UP: i=(i-1)%len(names)
                if e.key==pygame.K_DOWN: i=(i+1)%len(names)
                if e.key==pygame.K_RETURN: return names[i], DIFFICULTIES[names[i]]

def screen_ranking(screen):
    top = leaderboard.top()
    screen.fill(config.BG_COLOR); draw_text(screen,"TOP 10",64,screen.get_width()/2,120,(0,255,255))
    y=180
    for i,s in enumerate(top,1):
        draw_text(screen,f"{i:2d}. {s['name']:<12} {s['score']:>5}",36,screen.get_width()/2,y,(230,230,230)); y+=34
    draw_text(screen,"ENTER para volver",28,screen.get_width()/2,y+40,(150,150,150))
    pygame.display.flip(); waiting=True
    while waiting:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_RETURN: waiting=False

def screen_victories(screen):
    hist = leaderboard.victories()
    screen.fill(config.BG_COLOR); draw_text(screen,"Historial de victorias",56,screen.get_width()/2,80,(255,255,0))
    y=130
    if not hist:
        draw_text(screen,"(vacío)",36,screen.get_width()/2, y, (220,220,220))
        y+=40
    else:
        for h in hist[-12:]:
            line=f"{h['name']} | {h['map']} | {h['score']} pts | {h['stars']}★ | {h['time']}s"
            draw_text(screen,line,28,screen.get_width()/2,y,(230,230,230)); y+=28
    draw_text(screen,"ENTER para volver",28,screen.get_width()/2,y+30,(150,150,150))
    pygame.display.flip(); waiting=True
    while waiting:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_RETURN: waiting=False

def main_menu(screen):
    names=list(maps.ALL_MAPS.keys()); i=0
    special = ["Ver Ranking", "Historial de victorias"]
    thumbs={}
    for n in names:
        data=maps.ALL_MAPS[n]; layout=data.get('layout', data.get('LAYOUT', data))
        thumbs[n]=make_map_thumbnail(layout)
    while True:
        screen.fill(config.BG_COLOR)
        draw_text(screen,"PUNK-MAN ",64,screen.get_width()/2,60,(255,255,0))
        draw_text(screen,"Selecciona un mapa ",28,screen.get_width()/2,110,(200,200,200))
        base_y=150
        for k,n in enumerate(names + special):
            color=(255,255,0) if k==i else (230,230,230)
            draw_text(screen, n, 28, screen.get_width()*0.25, base_y + k*28, color)
        if i < len(names):
            th=thumbs[names[i]]; r=th.get_rect(center=(screen.get_width()*0.70,screen.get_height()*0.55)); screen.blit(th,r)
        else:
            draw_text(screen,"—",64,screen.get_width()*0.70,screen.get_height()*0.55,(255,255,255))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_UP: i=(i-1)% (len(names)+len(special))
                if e.key==pygame.K_DOWN: i=(i+1)% (len(names)+len(special))
                if e.key==pygame.K_RETURN:
                    if i < len(names):
                        return names[i], maps.ALL_MAPS[names[i]]
                    else:
                        if special[i-len(names)] == "Ver Ranking":
                            screen_ranking(screen)
                        else:
                            screen_victories(screen)

def run_game(screen, map_name, map_data, skin_name, diff, diff_name):
    layout = map_data.get('layout', map_data.get('LAYOUT', map_data))
    spawns = map_data.get('spawns', map_data.get('SPAWNS'))
    def parse_spawns(obj):
        player=(1,1); ghosts=[]
        if isinstance(obj,dict):
            if 'player' in obj: player=tuple(obj['player'])
            elif 'player_start' in obj: player=tuple(obj['player_start'])
            elif 'player_pos' in obj: player=tuple(obj['player_pos'])
            if 'ghosts' in obj: ghosts=[tuple(g) for g in obj['ghosts']]
        elif isinstance(obj,(list,tuple)) and obj and isinstance(obj[0],(list,tuple)):
            player=tuple(obj[0]); ghosts=[tuple(g) for g in obj[1:]]
        return player, ghosts
    player_start, ghost_spawns = parse_spawns(spawns)
    world_w=len(layout[0])*config.TILE_SIZE; world_h=len(layout)*config.TILE_SIZE
    screen=pygame.display.set_mode((max(world_w,640), max(world_h,480)))
    maze=Maze(layout)

    allow_shield = (diff_name != "Difícil")
    if allow_shield and len(maze.shield_orbs) == 0 and maze.free_tiles:
        c,r = rand_choice(maze.free_tiles)
        rect = pygame.Rect(c*config.TILE_SIZE + config.TILE_SIZE//2 - 8, r*config.TILE_SIZE + config.TILE_SIZE//2 - 8, 16,16)
        maze.shield_orbs.append(rect)

    if config.AUDIO_ENABLED and not pygame.mixer.music.get_busy():
        try:
            pygame.mixer.music.load(config.asset_path(config.MUSIC_FILE))
            pygame.mixer.music.set_volume(config.MUSIC_VOLUME)
            pygame.mixer.music.play(-1, fade_ms=300)
        except Exception as e: print('Audio:',e)
    try:
        eat_sfx=pygame.mixer.Sound(config.asset_path(config.EAT_SFX_FILE)); eat_sfx.set_volume(config.SFX_VOLUME)
    except Exception as e:
        eat_sfx=None; print('SFX:',e)

    player_speed=config.PLAYER_BASE_SPEED*diff['player_mult']
    player=Player(player_start[0],player_start[1],player_speed,skin_name)

    def tile_free(c,r):
        try: return layout[r][c] in (0,2,3,4)
        except IndexError: return False
    def nearest_free(c0,r0):
        if tile_free(c0,r0): return c0,r0
        H,W=len(layout),len(layout[0]); dq=deque([(c0,r0)]); seen={(c0,r0)}
        while dq:
            c,r=dq.popleft()
            for dc,dr in [(1,0),(-1,0),(0,1),(0,-1)]:
                nc, nr = c+dc, r+dr
                if 0<=nr<H and 0<=nc<W and (nc,nr) not in seen:
                    if tile_free(nc,nr): return nc,nr
                    seen.add((nc,nr)); dq.append((nc,nr))
        return c0,r0

    names=['blinky','pinky','inky','clyde']
    colors=[(255,0,0),(255,184,222),(0,255,255),(255,184,82)]
    want=min(4, diff['ghost_count'], len(ghost_spawns)); ghosts=[]
    for i in range(want):
        c,r=ghost_spawns[i]; c,r=nearest_free(c,r)
        ghosts.append(Ghost(c,r,names[i%4],colors[i%4], speed_mult=diff['ghost_mult']))

    score=0; eat_chain=0; last_eat_ms=0; EAT_COOLDOWN=90
    power_until=0; frightened=False
    shield_until=0; shield_charges=0
    extra_active=False; extra_rect=None; next_extra_idx=0 if allow_shield else 9999
    extra_thresholds = config.EXTRA_LIFE_THRESHOLDS if allow_shield else []

    start_ticks=pygame.time.get_ticks()
    clock=pygame.time.Clock()

    try:
        extra_icon=pygame.image.load(config.asset_path(config.EXTRA_LIFE_ICON)).convert_alpha()
        extra_icon=pygame.transform.smoothscale(extra_icon,(24,24))
    except Exception:
        extra_icon=pygame.Surface((24,24)); extra_icon.fill((255,0,255))

    def random_item_pos():
        if not maze.free_tiles: return None
        c,r=rand_choice(maze.free_tiles)
        x,y = c*config.TILE_SIZE + config.TILE_SIZE//2 - 12, r*config.TILE_SIZE + config.TILE_SIZE//2 - 12
        return pygame.Rect(x,y,24,24)

    running=True
    while running:
        dt=clock.tick(60)
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE: running=False
                if e.key==pygame.K_LEFT:  player.change_direction((-1,0))
                if e.key==pygame.K_RIGHT: player.change_direction((1,0))
                if e.key==pygame.K_UP:    player.change_direction((0,-1))
                if e.key==pygame.K_DOWN:  player.change_direction((0,1))

        now=pygame.time.get_ticks()
        player.move(maze)

        gained, activated, got_shield = player.eat(maze)
        if gained>0:
            score+=gained
            if eat_sfx and (now-last_eat_ms)>=EAT_COOLDOWN:
                pygame.mixer.find_channel(True).play(eat_sfx); last_eat_ms=now

        if next_extra_idx < len(extra_thresholds) and score >= extra_thresholds[next_extra_idx] and not extra_active:
            extra_rect = random_item_pos(); extra_active = extra_rect is not None; next_extra_idx += 1

        if activated:
            eat_chain=0; frightened=True; power_until = now + config.POWER_DURATION_MS
            for g in ghosts: g.set_frightened(now)

        if got_shield and allow_shield:
            shield_charges = 1
            shield_until = now + config.POWER_DURATION_MS

        if extra_active and extra_rect and player.rect.colliderect(extra_rect):
            extra_active=False; extra_rect=None; player.lives += 1

        for g in ghosts:
            g.move(maze, now)
            if player.rect.colliderect(g.rect):
                from ghost import STATE_FRIGHTENED, STATE_EATEN
                if g.state==STATE_FRIGHTENED:
                    g.state=STATE_EATEN; g.rect.topleft=g.eaten_target
                    eat_chain=min(eat_chain+1,4); score += config.EAT_GHOST_BASE_SCORE*(2**(eat_chain-1))
                else:
                    if shield_charges>0 and now <= shield_until:
                        shield_charges = 0; shield_until = 0
                        for gg in ghosts: gg.rect.topleft=gg.home
                    else:
                        player.lives-=1; eat_chain=0; player.reset_position()
                        for gg in ghosts: gg.rect.topleft=gg.home
                        if player.lives<=0:
                            show_game_over_and_save(screen, score); return

        if frightened and now >= power_until:
            frightened=False
        if shield_until and now >= shield_until:
            shield_until = 0; shield_charges = 0

        if not maze.dots and not maze.power_dots and not maze.shield_orbs:
            elapsed = (pygame.time.get_ticks() - start_ticks)//1000
            stars = star_rating(elapsed, map_name)
            name = ask_name(screen)
            leaderboard.add_score(name or "Player", score)
            leaderboard.add_victory(name or "Player", score, map_name, stars, elapsed)
            screen.fill((0,0,0))
            draw_text(screen, '¡Victoria!', 64, screen.get_width()/2, screen.get_height()/2 - 60, (255,255,0))
            draw_text(screen, f'Tiempo: {elapsed}s  |  Estrellas: ' + '★'*stars + '☆'*(3-stars), 40, screen.get_width()/2, screen.get_height()/2 + 10, (200,200,200))
            pygame.display.flip(); pygame.time.wait(1200)
            return

        screen.fill(config.BG_COLOR)
        maze.draw(screen)
        for g in ghosts: g.draw(screen)
        player.draw(screen)
        draw_text(screen, f"{map_name} | Score: {score} | Lives: {player.lives}", 26, screen.get_width()/2, 16, config.SCORE_COLOR)

        active = None; remaining = 0
        if frightened: active="POWER"; remaining=(power_until-now)/max(1,config.POWER_DURATION_MS)
        if shield_until:
            if not active or (shield_until-now) > (power_until-now):
                active="SHIELD"; remaining=(shield_until-now)/max(1,config.POWER_DURATION_MS)
        if active:
            draw_bar(screen, 20, 30, screen.get_width()-40, 8, remaining, bg=(40,40,40), fg=(0,220,255))
            draw_text(screen, active, 20, 60, 52, (200,255,255))

        if extra_active and extra_rect: screen.blit(extra_icon, extra_rect)

        pygame.display.flip()

def ask_name(screen):
    name=""; entering=True
    while entering:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RETURN: entering=False
                elif e.key==pygame.K_BACKSPACE: name=name[:-1]
                elif e.unicode.isprintable() and len(name)<12: name+=e.unicode
        screen.fill(config.BG_COLOR)
        draw_text(screen,"Ingresa tu nombre:",36,screen.get_width()/2,280,(200,200,200))
        draw_text(screen,name,36,screen.get_width()/2,320,(255,255,255))
        pygame.display.flip()
    return name

def show_game_over_and_save(screen, score):
    draw_text(screen, "GAME OVER", 72, screen.get_width()/2, screen.get_height()/2-40, config.GAMEOVER_COLOR)
    pygame.display.flip(); pygame.time.wait(900)
    name = ask_name(screen)
    leaderboard.add_score(name or "Player", score)
    show_ranking(screen)

def show_ranking(screen):
    top=leaderboard.top()
    screen.fill(config.BG_COLOR); draw_text(screen,"TOP 10",64,screen.get_width()/2,120,(0,255,255))
    y=180
    for i,s in enumerate(top,1):
        draw_text(screen,f"{i:2d}. {s['name']:<12} {s['score']:>5}",36,screen.get_width()/2,y,(230,230,230)); y+=34
    draw_text(screen,"ENTER para volver",28,screen.get_width()/2,y+40,(150,150,150))
    pygame.display.flip(); waiting=True
    while waiting:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_RETURN: waiting=False

def main():
    screen=pygame.display.set_mode((960,720))
    while True:
        skin=skin_menu(screen)
        diff_name,diff=difficulty_menu(screen)
        map_name,map_data=main_menu(screen)
        run_game(screen, map_name, map_data, skin, diff, diff_name)

if __name__=='__main__': main()
