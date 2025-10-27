import pygame
import sys
from puntaje import guardar_record
from menu import main_menu
from ejecutar_nivel_1_2 import ejecutar_nivel

FPS = 60

def main():
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Mario Bros")

    try:
        pygame.mixer.init()
        pygame.mixer.music.load("assets/musica/12. Overworld.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    except Exception as e:
        print(f"No se pudo iniciar el audio: {e}")

    # Ejecutamos nivel 1
    vidas, puntaje, bonus, tiempo, monedas = ejecutar_nivel(screen, WIDTH, HEIGHT, clock, 1)
    
    # Ya no guardamos aquí porque se guarda al completar cada nivel

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()
    main()