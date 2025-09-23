import pygame
import sys
import time
import config
import maps  # Importamos nuestro archivo de mapas
from player import Player
from maze import Maze
from ghost import Ghost
from motor_aleatorio import MotorAleatorio, crear_seed_desde_imagen

# --- FUNCIÓN PARA DIBUJAR TEXTO ---
def draw_text(surface, text, size, x, y, color):
    """
    Función auxiliar para dibujar texto centrado en la pantalla.
    """
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# --- FUNCIÓN DEL BUCLE DEL JUEGO ---
def run_game(map_data):
    """ Función que contiene la lógica del juego para un mapa específico. """
    map_layout = map_data["layout"]
    spawn_points = map_data["spawns"]
    map_name = map_data["name"] # Obtenemos el nombre del mapa

    # --- CONFIGURACIÓN DE PANTALLA DINÁMICA ---
    map_height = len(map_layout)
    map_width = len(map_layout[0])
    screen_width = map_width * config.TILE_SIZE
    screen_height = map_height * config.TILE_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))

    # --- CREACIÓN DE OBJETOS PARA EL NIVEL ---
    maze = Maze(map_layout)
    player = Player(1, 1) # Inicia en la celda (1, 1)
    
    ghosts = []
    ghost_colors = list(config.GHOST_COLORS.values())
    for i, pos in enumerate(spawn_points):
        color = ghost_colors[i % len(ghost_colors)]
        ghosts.append(Ghost(pos[0], pos[1], color))

    score = 0
    game_over = False

    seed_base = crear_seed_desde_imagen(config.SEED_IMAGE_PATH)
    motor_del_juego = MotorAleatorio(seed=seed_base ^ time.time_ns())
    
    # --- BUCLE DEL JUEGO ---
    running = True
    while running:
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

        # --- LÓGICA Y ACTUALIZACIONES ---
        if not game_over:
            player.move(maze)

            # Lógica del Túnel
            if map_name == "El Tunel":
                # Asumiendo que el túnel está en la fila 5 del mapa original
                # y en las filas 10 y 11 del mapa duplicado
                tunnel_y_start = 10 * config.TILE_SIZE
                if player.rect.y >= tunnel_y_start and player.rect.y < tunnel_y_start + (2 * config.TILE_SIZE):
                    if player.rect.right < 0:
                        player.x = screen_width
                    elif player.rect.left > screen_width:
                        player.x = -player.size
            
            score += player.eat_dots(maze)
            for ghost in ghosts:
                ghost.move(maze, motor_del_juego)
                if player.rect.colliderect(ghost.rect):
                    player.lives -= 1
                    player.reset_position()
                    if player.lives <= 0:
                        game_over = True
            if not maze.dots:
                running = False

        # --- DIBUJADO ---
        screen.fill(config.BG_COLOR)
        maze.draw(screen)
        player.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen)
        
        draw_text(screen, f"Score: {score}", 36, 70, 10, config.SCORE_COLOR)
        draw_text(screen, f"Lives: {player.lives}", 36, screen_width - 70, 10, config.SCORE_COLOR)

        if game_over:
            draw_text(screen, "GAME OVER", 64, screen_width / 2, screen_height / 2 - 50, config.GAMEOVER_COLOR)
            draw_text(screen, "Presiona ESC para volver al menu", 30, screen_width / 2, screen_height / 2 + 20, config.SCORE_COLOR)

        pygame.display.flip()

# --- FUNCIÓN PRINCIPAL QUE MANEJA EL MENÚ ---
def main():
    pygame.init()
    
    menu_screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(config.GAME_TITLE)

    map_names = list(maps.ALL_MAPS.keys())
    selected_option = 0

    while True:
        menu_screen.fill(config.BG_COLOR)
        draw_text(menu_screen, "PAC-MAN", 96, 400, 50, (255, 255, 0))
        draw_text(menu_screen, "Selecciona un Mapa", 50, 400, 160, config.SCORE_COLOR)

        for i, name in enumerate(map_names):
            color = (255, 255, 0) if i == selected_option else config.SCORE_COLOR
            draw_text(menu_screen, name, 35, 400, 250 + i * 45, color)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(map_names)
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(map_names)
                if event.key == pygame.K_RETURN:
                    chosen_map_name = map_names[selected_option]
                    chosen_map_data = maps.ALL_MAPS[chosen_map_name]
                    # Añadimos el nombre al diccionario para poder identificar el mapa
                    chosen_map_data['name'] = chosen_map_name
                    
                    run_game(chosen_map_data)
                    
                    pygame.display.set_mode((800, 600))

if __name__ == '__main__':
    main()