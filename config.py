import os

GAME_TITLE = "Punk-Man v3+"
TILE_SIZE = 32
PLAYER_LIVES = 3

BG_COLOR        = (0, 50, 180)
WALL_COLOR      = (0, 0, 0)
DOT_COLOR       = (235, 235, 235)
POWER_DOT_COLOR = (255, 184, 151)
SHIELD_ORB_COLOR= (80, 170, 255)
SCORE_COLOR     = (255, 255, 255)
GAMEOVER_COLOR  = (255, 0, 0)

AUDIO_ENABLED = True
MUSIC_FILE    = "assets/audio/music.wav"
EAT_SFX_FILE  = "assets/audio/eat.wav"
MUSIC_VOLUME  = 0.4
SFX_VOLUME    = 0.6

GHOST_BASE_SPEED       = 2.3
GHOST_FRIGHTENED_SPEED = 1.6
GHOST_EATEN_SPEED      = 3.2
PLAYER_BASE_SPEED      = 2.8

POWER_DURATION_MS = 7000
EAT_GHOST_BASE_SCORE = 200

SKINS = {
    "Classic": {
        "color": (255, 255, 0),
        "right": "assets/images/pacman_default_right.png",
        "left":  "assets/images/pacman_default_left.png",
        "up":    "assets/images/pacman_default_up.png",
        "down":  "assets/images/pacman_default_down.png"
    },
    "Rojo": {
        "color": (255, 70, 70),
        "right": "assets/images/pacman_red_right.png",
        "left":  "assets/images/pacman_red_left.png",
        "up":    "assets/images/pacman_red_up.png",
        "down":  "assets/images/pacman_red_down.png"
    },
    "Verde": {
        "color": (90, 220, 120),
        "right": "assets/images/pacman_green_right.png",
        "left":  "assets/images/pacman_green_left.png",
        "up":    "assets/images/pacman_green_up.png",
        "down":  "assets/images/pacman_green_down.png"
    },
}
DEFAULT_SKIN_NAME = "Classic"

EXTRA_LIFE_THRESHOLDS = [300, 700]
EXTRA_LIFE_ICON = "assets/images/extra_life.png"
SHIELD_TILE_ICON = "assets/images/shield_orb.png"

STAR_THRESHOLDS_SEC = { "default": [60, 90, 140] }

def asset_path(rel): return os.path.join(os.path.dirname(os.path.abspath(__file__)), rel)

SEED_IMAGE_PATH = "assets/images/image_seed.png"