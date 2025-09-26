import pygame
import sys
import time
import config
import maps
from player import Player
from maze import Maze
from ghost import Ghost
from motor_aleatorio import MotorAleatorio, crear_seed_desde_imagen

# --- FUNCIÓN PRINCIPAL DEL PROGRAMA ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption(config.GAME_TITLE)

    while True:
        # 1. Mostrar menú de mapas y obtener la selección
        selected_map_data = main_menu(screen)
        if not selected_map_data:
            break # Si se sale del menú de mapas, se cierra el juego

        # 2. Mostrar menú de dificultad y obtener la selección
        difficulty_settings = difficulty_menu(screen)
        if not difficulty_settings:
            continue # Si se sale del menú de dificultad, vuelve al de mapas

        # 3. Iniciar el juego con el mapa y la dificultad seleccionados
        run_game(screen, selected_map_data, difficulty_settings)

    pygame.quit()
    sys.exit()

# --- FUNCIÓN DEL MENÚ DE MAPAS ---
def main_menu(screen):
    map_names = list(maps.ALL_MAPS.keys())
    selected_option = 0
    
    while True:
        # Dibujado del Menú
        screen.fill(config.BG_COLOR)
        draw_text(screen, "PUNK-MAN", 96, screen.get_width() / 2, 50, (255, 255, 0))
        draw_text(screen, "Selecciona un Mapa", 50, screen.get_width() / 2, 160, config.SCORE_COLOR)

        for i, name in enumerate(map_names):
            color = (255, 255, 0) if i == selected_option else config.SCORE_COLOR
            draw_text(screen, name, 35, screen.get_width() / 2, 250 + i * 45, color)
        
        pygame.display.flip()

        # Manejo de Eventos del Menú
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None # Devuelve None para indicar que se quiere salir
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(map_names)
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(map_names)
                if event.key == pygame.K_ESCAPE:
                    return None # Devuelve None para salir
                if event.key == pygame.K_RETURN:
                    chosen_map_name = map_names[selected_option]
                    chosen_map_data = maps.ALL_MAPS[chosen_map_name]
                    chosen_map_data['name'] = chosen_map_name
                    return chosen_map_data

# --- FUNCIÓN DEL MENÚ DE DIFICULTAD ---
def difficulty_menu(screen):
    difficulties = {
        "Facil": {"speed": 2, "ghost_count": 3},
        "Medio": {"speed": 3, "ghost_count": 4},
        "Dificil": {"speed": 6, "ghost_count": 5}
    }
    difficulty_names = list(difficulties.keys())
    selected_option = 0

    while True:
        screen.fill(config.BG_COLOR)
        draw_text(screen, "Selecciona Dificultad", 50, screen.get_width() / 2, 160, config.SCORE_COLOR)
        
        for i, name in enumerate(difficulty_names):
            color = (255, 255, 0) if i == selected_option else config.SCORE_COLOR
            draw_text(screen, name, 35, screen.get_width() / 2, 250 + i * 45, color)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(difficulty_names)
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(difficulty_names)
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key == pygame.K_RETURN:
                    chosen_difficulty_name = difficulty_names[selected_option]
                    return difficulties[chosen_difficulty_name]

# --- FUNCIÓN DEL BUCLE DEL JUEGO ---
def run_game(screen, map_data, difficulty):
    map_layout = map_data["layout"]
    spawn_points = map_data["spawns"]
    map_name = map_data["name"]
    
    ghost_speed = difficulty["speed"]
    ghost_count = difficulty["ghost_count"]

    total_map_width = len(map_layout[0]) * config.TILE_SIZE
    total_map_height = len(map_layout) * config.TILE_SIZE
    world_surface = pygame.Surface((total_map_width, total_map_height))

    maze = Maze(map_layout)
    player = Player(1, 1, ghost_speed)
    
    ghosts = []
    ghost_colors = list(config.GHOST_COLORS.values())
    for i, (color_name, color_rgb) in enumerate(config.GHOST_COLORS.items()):
        # Creamos fantasmas según la dificultad y los spawns disponibles
        if i < ghost_count and i < len(spawn_points):
            pos = spawn_points[i]
            # Le pasamos el 'color_name' (ej: "blinky") al fantasma
            ghosts.append(Ghost(pos[0], pos[1], color_name, ghost_speed))

    score = 0
    game_over = False
    seed_base = crear_seed_desde_imagen(config.SEED_IMAGE_PATH)
    motor_del_juego = MotorAleatorio(seed=seed_base ^ time.time_ns())
    
    running = True
    while running:
        SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT: player.change_direction((-1, 0))
                    if event.key == pygame.K_RIGHT: player.change_direction((1, 0))
                    if event.key == pygame.K_UP: player.change_direction((0, -1))
                    if event.key == pygame.K_DOWN: player.change_direction((0, 1))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        if not game_over:
            player.move(maze)
            score += player.eat_dots(maze)
            for ghost in ghosts:
                ghost.move(maze, motor_del_juego)
                if player.rect.colliderect(ghost.rect):
                    player.lives -= 1
                    player.reset_position()
                    
                    for g in ghosts: # 'g' para no confundir con el 'ghost' del bucle exterior
                        g.reset_position()
                    
                    if player.lives <= 0:
                        game_over = True
            if not maze.dots:
                running = False

        world_surface.fill(config.BG_COLOR)
        maze.draw(world_surface)
        player.draw(world_surface)
        for ghost in ghosts:
            ghost.draw(world_surface)
        
        font = pygame.font.Font(None, 36)
        draw_text(world_surface, f"Score: {score}", 36, 70, 10, config.SCORE_COLOR)
        draw_text(world_surface, f"Lives: {player.lives}", 36, total_map_width - 70, 10, config.SCORE_COLOR)

        if game_over:
            draw_text(world_surface, "GAME OVER", 64, total_map_width / 2, total_map_height / 2 - 50, config.GAMEOVER_COLOR)
            draw_text(world_surface, "Presiona ESC", 30, total_map_width / 2, total_map_height / 2 + 20, config.SCORE_COLOR)

        map_ratio = total_map_width / total_map_height
        screen_ratio = SCREEN_WIDTH / SCREEN_HEIGHT
        
        if map_ratio > screen_ratio:
            scaled_width = SCREEN_WIDTH
            scaled_height = int(scaled_width / map_ratio)
        else:
            scaled_height = SCREEN_HEIGHT
            scaled_width = int(scaled_height * map_ratio)

        scaled_surface = pygame.transform.scale(world_surface, (scaled_width, scaled_height))
        
        pos_x = (SCREEN_WIDTH - scaled_width) / 2
        pos_y = (SCREEN_HEIGHT - scaled_height) / 2
        
        screen.fill(config.BG_COLOR)
        screen.blit(scaled_surface, (pos_x, pos_y))

        pygame.display.flip()

# --- FUNCIÓN PARA DIBUJAR TEXTO ---
def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(midtop=(x, y))
    surface.blit(text_surface, text_rect)

# Inicia la función principal
if __name__ == '__main__':
    main()