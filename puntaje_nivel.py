import pygame, sys, os
from entities import Player

def main_puntaje(score):
    # Inicializar Pygame
    pygame.init()

    # Abrir ventana en pantalla completa
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()#toma la medida de la pantalla
    pygame.display.set_caption("Mariano bross")#titulo de la ventana
    clock = pygame.time.Clock()

    #fuentes para los titulos
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)

    # Cargar y escalar fondo
    fondo = pygame.image.load("assets/menu/fondo.png").convert()
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

    # Configura la música de fondo
    musica = True
    if not pygame.mixer.get_init():
        musica = False
        os.environ["SDL_AUDIODRIVER"] = "dummy"
    #musica en bucle
    if musica:
        try:
            pygame.mixer.music.load("assets/musica/10 Shop.mp3")
            pygame.mixer.music.play(-1) #infinito
            pygame.mixer.music.set_volume(0.5)
        except Exception as e:
            print(f"No se pudo iniciar el audio en el menú. Continuando sin sonido. Error: {e}")

    #Bucle infinito hasta salir
    while True:
        screen.blit(fondo, (0, 0))
        titulo = font.render("Mariano Bros", True, (255, 255, 255))

        texto_puntaje = f"Tu puntuación: {score}"
        play = small_font.render(texto_puntaje, True, (255, 255, 255))
        salir = small_font.render("Presiona ESC para salir", True, (255, 255, 255))

        #centra el titulo en la pantalla
        screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, HEIGHT//2 - 100))
        screen.blit(play, (WIDTH//2 - play.get_width()//2, HEIGHT//2))
        screen.blit(salir, (WIDTH//2 - salir.get_width()//2, HEIGHT//2 + 40))

        #si sale del juego si se sierra la ventana
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        #actualiza la pantalla todo el tiempo
        pygame.display.flip()
        clock.tick(60)