
import os, time
import config
from motor_aleatorio import MotorAleatorio, crear_seed_desde_imagen

try:
    seed_img = config.asset_path(config.SEED_IMAGE_PATH)
except Exception:
    seed_img = os.path.join(os.path.dirname(__file__), "assets", "images", "seed.png")

base = crear_seed_desde_imagen(seed_img) or 123456789
MOTOR = MotorAleatorio(seed=(base ^ time.time_ns()) % MotorAleatorio.M)

def rand_int(a, b):
    return MOTOR.siguiente_numero(a, b)

def rand_choice(seq):
    if not seq:
        raise IndexError("rand_choice on empty sequence")
    return seq[rand_int(0, len(seq)-1)]
