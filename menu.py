import pygame, sys, os

WIDTH, HEIGHT = 960, 540

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menú Principal")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)

    fondo = pygame.image.load("assets/universo.png").convert()
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

    if not pygame.mixer.get_init():
        musica = False
        os.environ["SDL_AUDIODRIVER"] = "dummy"
    if musica == False:
        pass
    else:
        try:
            pygame.mixer.music.load("assets/musica/10 Shop.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
        except Exception as e:
            print(f"No se pudo iniciar el audio en el menú. Continuando sin sonido. Error: {e}")

    while True:
        screen.blit(fondo, (0, 0))
        titulo = font.render("Mariano Bros", True, (255, 255, 255))
        play = small_font.render("Presiona ENTER para jugar", True, (255, 255, 255))
        salir = small_font.render("Presiona ESC para salir", True, (255, 255, 255))

        screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, HEIGHT//2 - 100))
        screen.blit(play, (WIDTH//2 - play.get_width()//2, HEIGHT//2))
        screen.blit(salir, (WIDTH//2 - salir.get_width()//2, HEIGHT//2 + 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)
