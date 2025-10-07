import time
from PIL import Image
import config

def crear_seed_desde_imagen(ruta_imagen):

    try:
        with Image.open(ruta_imagen) as img:
            img_gris = img.convert('L')
            ancho, alto = img.size
            valores_pixeles = list(img_gris.getdata())
            semilla_bruta = (sum(valores_pixeles) * ancho * alto) ^ (ancho * alto)
            return semilla_bruta % (2**32)
    except Exception as e:
        print(f"Error al crear la semilla: {e}")
        return None

class MotorAleatorio:

    A = 1664525
    C = 1013904223
    M = 2**32

    def __init__(self, seed):
        
        print(f"DEBUG: El motor se ha creado correctamente con la seed = {seed}")


        self.estado = seed

    def siguiente_numero(self, min_val, max_val):

        self.estado = (self.A * self.estado + self.C) % self.M
        
        rango = max_val - min_val + 1
        bits_altos = self.estado >> 16 
        return min_val + (bits_altos % rango)

if __name__ == "__main__":
    
    print("Inicializando el motor de aleatoriedad del juego...")
    ruta_imagen_nivel = config.SEED_IMAGE_PATH 
    seed_base = crear_seed_desde_imagen(ruta_imagen_nivel)
    
    if seed_base is not None:
        
        seed_final_grande = seed_base ^ time.time_ns()

        seed_final_valida = seed_final_grande % MotorAleatorio.M

        motor_del_juego = MotorAleatorio(seed=seed_final_valida)

        print(f"Motor inicializado con la semilla final: {motor_del_juego.estado}")
        print("-" * 30)

        print("Simulando decisiones de un fantasma en 3 intersecciones:")
        
        decision_1 = motor_del_juego.siguiente_numero(0, 3)
        print(f"   -> Intersección 1: El fantasma decide ir a la dirección {decision_1}")

        decision_2 = motor_del_juego.siguiente_numero(0, 3)
        print(f"   -> Intersección 2: El fantasma decide ir a la dirección {decision_2}")
        
        decision_3 = motor_del_juego.siguiente_numero(0, 3)
        print(f"   -> Intersección 3: El fantasma decide ir a la dirección {decision_3}")