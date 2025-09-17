import pygame
import sys
import os

def main_menu():
    pygame.init()

    # Se establece Pantalla completa
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Menú Principal")
    clock = pygame.time.Clock() # Controla los FPS

    # Carga el  fondo
    fondo = pygame.image.load("assets/menu/fondo.png").convert()
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

    # --- Botones ---
    button_width, button_height = 300, 200

    # Play button
    play_btn_img = pygame.image.load("assets/menu/boton_play_menu.png").convert_alpha()
    play_btn_hover = pygame.image.load("assets/menu/boton_play_menu_2.png").convert_alpha()
    play_btn_img = pygame.transform.scale(play_btn_img, (button_width, button_height))
    play_btn_hover = pygame.transform.scale(play_btn_hover, (button_width, button_height))
    play_btn_rect = play_btn_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Quit button
    quit_btn_img = pygame.image.load("assets/menu/boton_quit_menu.png").convert_alpha()
    quit_btn_hover = pygame.image.load("assets/menu/boton_quit_menu_2.png").convert_alpha()
    quit_btn_img = pygame.transform.scale(quit_btn_img, (button_width, button_height))
    quit_btn_hover = pygame.transform.scale(quit_btn_hover, (button_width, button_height))
    quit_btn_rect = quit_btn_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))

    # Cargar y escalar el título
    titulo_img = pygame.image.load("assets/menu/mariano_bros.png").convert_alpha()
    titulo_width, titulo_height = 400, 600
    titulo_img = pygame.transform.scale(titulo_img, (titulo_width, titulo_height))
    titulo_rect = titulo_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200)) 

    # Música
    musica = True
    if not pygame.mixer.get_init():
        musica = False
        os.environ["SDL_AUDIODRIVER"] = "dummy"
    if musica:
        try:
            pygame.mixer.music.load("assets/musica/10 Shop.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
        except Exception as e:
            print(f"No se pudo iniciar el audio en el menú. Continuando sin sonido. Error: {e}")

    # Bucle principal del menú
    while True:
        screen.blit(fondo, (0, 0))
        screen.blit(titulo_img, titulo_rect)

        # --- Chequeo Hover ---
        mouse_pos = pygame.mouse.get_pos()

        # Play
        if play_btn_rect.collidepoint(mouse_pos):
            screen.blit(play_btn_hover, play_btn_rect)
        else:
            screen.blit(play_btn_img, play_btn_rect)

        # Quit
        if quit_btn_rect.collidepoint(mouse_pos):
            screen.blit(quit_btn_hover, quit_btn_rect)
        else:
            screen.blit(quit_btn_img, quit_btn_rect)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN: # Detecta click del mouse
                if event.button == 1:  # Click izquierdo
                    if play_btn_rect.collidepoint(event.pos):
                        return  # Inicia el juego
                    elif quit_btn_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()
        clock.tick(60)
