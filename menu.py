import pygame
import sys
import os
# Integración del menú de configuración
try:
    from Menu_config import open_config_menu
except Exception:
    # Si por alguna razón no está disponible, definimos un stub para evitar crashes
    def open_config_menu():
        print('No se pudo abrir el menú de configuración (config_menu no disponible)')

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
    button_width, button_height = 180, 96

    # Play button
    play_btn_img = pygame.image.load("assets/menu/boton_play_menu.png").convert_alpha()
    play_btn_hover = pygame.image.load("assets/menu/boton_play_menu_2.png").convert_alpha()
    play_btn_img = pygame.transform.scale(play_btn_img, (button_width, button_height))
    play_btn_hover = pygame.transform.scale(play_btn_hover, (button_width, button_height))
    play_btn_rect = play_btn_img.get_rect(center=(WIDTH // 2 , HEIGHT // 2))

    # Quit button
    quit_btn_img = pygame.image.load("assets/menu/boton_quit_menu.png").convert_alpha()
    quit_btn_hover = pygame.image.load("assets/menu/boton_quit_menu_2.png").convert_alpha()
    quit_btn_img = pygame.transform.scale(quit_btn_img, (button_width, button_height))
    quit_btn_hover = pygame.transform.scale(quit_btn_hover, (button_width, button_height))
    quit_btn_rect = quit_btn_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 240))

    # Top button
    top_btn_img = pygame.image.load("assets/menu/boton_top_menu.png").convert_alpha()
    top_btn_hover = pygame.image.load("assets/menu/boton_top_menu_2.png").convert_alpha()
    top_btn_img = pygame.transform.scale(top_btn_img, (button_width, button_height))
    top_btn_hover = pygame.transform.scale(top_btn_hover, (button_width, button_height))
    top_btn_rect = top_btn_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
     # Options button (integración del menú de configuración)
    # Ahora más pequeño y ubicado arriba a la derecha
    options_img = None
    options_hover = None
    try:
        options_w, options_h = 120, 64
        opt_path = "assets/menu/boton_options_menu.png"
        opt_hover_path = "assets/menu/boton_options_menu_2.png"
        if os.path.exists(opt_path) and os.path.exists(opt_hover_path):
            options_img = pygame.image.load(opt_path).convert_alpha()
            options_hover = pygame.image.load(opt_hover_path).convert_alpha()
            options_img = pygame.transform.scale(options_img, (options_w, options_h))
            options_hover = pygame.transform.scale(options_hover, (options_w, options_h))
            options_btn_rect = options_img.get_rect(topright=(WIDTH - 40, 40))
        else:
            options_img = None
            options_hover = None
            # rect for drawn button in top-right
            options_btn_rect = pygame.Rect(0, 0, options_w, options_h)
            options_btn_rect.topright = (WIDTH - 40, 40)
    except Exception:
        options_img = None
        options_hover = None
        options_btn_rect = pygame.Rect(0, 0, 120, 64)
        options_btn_rect.topright = (WIDTH - 40, 40)

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
        
        # Top
        if top_btn_rect.collidepoint(mouse_pos):
            screen.blit(top_btn_hover, top_btn_rect)
        else:
            screen.blit(top_btn_img, top_btn_rect)
        # Options (pequeño, arriba a la derecha)
        if options_img is not None:
            if options_btn_rect.collidepoint(mouse_pos):
                screen.blit(options_hover, options_btn_rect)
            else:
                screen.blit(options_img, options_btn_rect)
        else:
            # Mostrar el logo 'logohuergo.png' si está disponible en assets/menu
            logo_path = "assets/menu/logohuergo.png"
            try:
                logo_img = pygame.image.load(logo_path).convert_alpha()
                # escalar el logo al tamaño del botón manteniendo aspecto
                logo_w, logo_h = options_btn_rect.width, options_btn_rect.height
                logo_img = pygame.transform.smoothscale(logo_img, (logo_w, logo_h))
                screen.blit(logo_img, options_btn_rect)
                # dibujar un borde al pasar el mouse
                if options_btn_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (56, 217, 222), options_btn_rect, 3, border_radius=8)
            except Exception:
                # Si no se encuentra el logo, volver al fallback con texto 'Opciones'
                opt_color = (150, 150, 170) if not options_btn_rect.collidepoint(mouse_pos) else (56, 217, 222)
                pygame.draw.rect(screen, (30, 30, 40), options_btn_rect, border_radius=8)
                pygame.draw.rect(screen, opt_color, options_btn_rect, 2, border_radius=8)
                font = pygame.font.SysFont('dejavusansmono', 20)
                txt = font.render('Opciones', True, (220, 230, 240))
                trect = txt.get_rect(center=options_btn_rect.center)
                screen.blit(txt, trect)
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
                    elif options_btn_rect.collidepoint(event.pos):
                        # Abrir menú de configuración
                        try:
                            open_config_menu()
                        except Exception as e:
                            print(f'Error al abrir menú de configuración: {e}')

            elif event.type == pygame.KEYDOWN:
                # Atajo para abrir opciones con la tecla O o C
                if event.key in (pygame.K_o, pygame.K_c):
                    try:
                        open_config_menu()
                    except Exception as e:
                        print(f'Error al abrir menú de configuración: {e}')
                        try:
                            open_config_menu()
                        except Exception as e:
                            print(f'Error al abrir menú de configuración: {e}')

            elif event.type == pygame.KEYDOWN:
                # Atajo para abrir opciones con la tecla O o C
                if event.key in (pygame.K_o, pygame.K_c):
                    try:
                        open_config_menu()
                    except Exception as e:
                        print(f'Error al abrir menú de configuración: {e}')
        pygame.display.flip()
        clock.tick(60)
