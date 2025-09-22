import time
from PIL import Image

# --- FUNCIÓN UTILITARIA (Se mantiene igual) ---
def crear_seed_desde_imagen(ruta_imagen):
    """
    Genera una semilla (seed) única y determinista a partir de una imagen.
    """
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

# --- CLASE PRINCIPAL DEL MOTOR DE ALEATORIEDAD ---
class MotorAleatorio:
    """
    Un generador de números pseudoaleatorios (PRNG) basado en LCG.
    Mantiene el estado internamente para generar números bajo demanda.
    """
    # Constantes del algoritmo LCG
    A = 1664525
    C = 1013904223
    M = 2**32

    def __init__(self, seed):
        
        print(f"DEBUG: El motor se ha creado correctamente con la seed = {seed}")

        """
        Inicializa el motor con una semilla.
        """
        self.estado = seed

    def siguiente_numero(self, min_val, max_val):
        """
        Genera y devuelve el siguiente número aleatorio en la secuencia.
        """
        # 1. Actualiza el estado interno usando la fórmula LCG
        self.estado = (self.A * self.estado + self.C) % self.M
        
        # 2. Usa los bits altos (más aleatorios) para el cálculo
        rango = max_val - min_val + 1
        bits_altos = self.estado >> 16 # Descartamos los 16 bits menos aleatorios
        return min_val + (bits_altos % rango)

# --- BLOQUE PRINCIPAL: CÓMO SE USARÍA EN UN JUEGO ---
if __name__ == "__main__":
    
    # 1. INICIALIZACIÓN (Esto se haría una vez al empezar el juego o nivel)
    print("Inicializando el motor de aleatoriedad del juego...")
    ruta_imagen_nivel = 'image_seed.png' 
    seed_base = crear_seed_desde_imagen(ruta_imagen_nivel)
    
    if seed_base is not None:
        
        seed_final_grande = seed_base ^ time.time_ns()

        # AJUSTE CLAVE: Reducimos la semilla al rango válido del motor ANTES de usarla.
        seed_final_valida = seed_final_grande % MotorAleatorio.M

        motor_del_juego = MotorAleatorio(seed=seed_final_valida)

        print(f"Motor inicializado con la semilla final: {motor_del_juego.estado}")
        print("-" * 30)

        # 2. DURANTE EL JUEGO (Esto se llamaría en el bucle principal del juego)
        print("Simulando decisiones de un fantasma en 3 intersecciones:")
        
        # El fantasma llega a una intersección y necesita decidir una dirección (0=Arriba, 1=Abajo, 2=Izq, 3=Der)
        decision_1 = motor_del_juego.siguiente_numero(0, 3)
        print(f"   -> Intersección 1: El fantasma decide ir a la dirección {decision_1}")

        # Más tarde, llega a otra intersección
        decision_2 = motor_del_juego.siguiente_numero(0, 3)
        print(f"   -> Intersección 2: El fantasma decide ir a la dirección {decision_2}")
        
        # Y a una tercera
        decision_3 = motor_del_juego.siguiente_numero(0, 3)
        print(f"   -> Intersección 3: El fantasma decide ir a la dirección {decision_3}")