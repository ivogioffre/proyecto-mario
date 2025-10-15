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




def main():# Es la función principal del juego, la que se encarga de iniciar todo y controlar el flujo general
    #Inicializa Pygame y la ventana del juego
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
    vidas, monedas = ejecutar_nivel(screen, WIDTH, HEIGHT, clock, 1)
<<<<<<< HEAD


=======
>>>>>>> 9bc5d7d5b45e131af0f4f84fd3d96fb21c5632d7


    #Si aun quedan vidas al terminar nivel 1 pasamos al 2
    if vidas > 0:  
        # Ejecutamos nivel 2
        vidas, monedas = ejecutar_nivel(screen, WIDTH, HEIGHT, clock, 2, vidas, monedas)




        if vidas > 0:  # Si completaste nivel 2
            guardar_record(monedas)
            main_puntaje(monedas)




    pygame.quit()
    sys.exit()




















if __name__ == "__main__":
    main_menu()
    main()




<<<<<<< HEAD


=======
>>>>>>> 9bc5d7d5b45e131af0f4f84fd3d96fb21c5632d7
