import pygame
import sys
from puntaje import guardar_record
from menu import main_menu
from level import load_level
from level2 import load_level_2
from camera import Camera
from entities import Player, COIN_POP_EFFECTS, load_img
from puntaje_nivel import main_puntaje, perdiste
from ejecutar_nivel_1_2 import ejecutar_nivel

# Frames por segundo (FPS)
FPS = 60

def main():  # Es la función principal del juego, la que se encarga de iniciar todo y controlar el flujo general
    # Inicializa Pygame y la ventana del juego
    # Llama a la función ejecutar_nivel() para jugar nivel 1 y 2
    pygame.init()

    # Ventana pantalla completa
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Mario Bros")

    # Música
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("assets/musica/12. Overworld.mp3")
        pygame.mixer.music.play(-1)  # Loop infinito
        pygame.mixer.music.set_volume(0.5)
    except Exception as e:
        print(f"No se pudo iniciar el audio: {e}")

    # Ejecutamos nivel 1
    resultado = ejecutar_nivel(screen, WIDTH, HEIGHT, clock, 1)
    vidas, monedas = resultado[0], resultado[1]
    
    # Verificar si el usuario pidió volver al menú
    if len(resultado) > 2 and resultado[2] == "menu":
        pygame.quit()
        return "menu"

    # Si aún quedan vidas al terminar nivel 1 pasamos al 2
    if vidas > 0:
        # Mostrar pantalla de transición al segundo nivel
        try:
            from puntaje_nivel import pantalla_transicion_nivel
            pantalla_transicion_nivel(screen, WIDTH, HEIGHT, nivel=2, duracion_ms=1500)
        except Exception:
            pass

        # Ejecutamos nivel 2
        resultado = ejecutar_nivel(screen, WIDTH, HEIGHT, clock, 2, vidas, monedas)
        vidas, monedas = resultado[0], resultado[1]
        
        # Verificar si el usuario pidió volver al menú
        if len(resultado) > 2 and resultado[2] == "menu":
            pygame.quit()
            return "menu"

        if vidas > 0:  # Si completaste nivel 2
            try:
                from puntaje_nivel import pantalla_transicion_nivel
                pantalla_transicion_nivel(screen, WIDTH, HEIGHT, nivel=3, duracion_ms=1500)
            except Exception:
                pass

            # Ejecutamos nivel 3
            resultado = ejecutar_nivel(screen, WIDTH, HEIGHT, clock, 3, vidas, monedas)
            vidas, monedas = resultado[0], resultado[1]
            
            # Verificar si el usuario pidió volver al menú
            if len(resultado) > 2 and resultado[2] == "menu":
                pygame.quit()
                return "menu"

            if vidas > 0:  # Si completaste nivel 3
                guardar_record(monedas)
                resultado = main_puntaje(monedas)
                if isinstance(resultado, tuple) and resultado[0] == "menu":
                    puntaje_final = resultado[1] if len(resultado) > 1 else 0
                    pygame.quit()
                    return "menu"
                elif resultado == "menu":
                    pygame.quit()
                    return "menu"

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    while True:
        main_menu()
        resultado = main()
        if resultado != "menu":
            break
