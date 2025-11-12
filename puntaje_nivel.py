import pygame, sys, os
from entities import Player

puntajes_acumulados = {}

def guardar_puntaje_nivel(nivel, puntos_nivel, puntos_por_monedas, puntos_por_enemigos, bonus_tiempo, tiempo_total, monedas):
    """Guardar el desglose de puntaje para un nivel concreto."""
    puntajes_acumulados[f"nivel_{nivel}"] = {
        "puntos_nivel": int(puntos_nivel),
        "puntos_por_monedas": int(puntos_por_monedas),
        "puntos_por_enemigos": int(puntos_por_enemigos),
        "bonus_tiempo": int(bonus_tiempo),
        "tiempo_total": float(tiempo_total),
        "monedas": int(monedas),
    }


def main_puntaje(score):
    """Pantalla final al completar el juego."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("¡Ganaste!")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)
    button_font = pygame.font.SysFont(None, 48)

    try:
        fondo = pygame.image.load("assets/menu/fondo.png").convert()
        fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
    except:
        fondo = pygame.Surface((WIDTH, HEIGHT))
        fondo.fill((20, 20, 40))

    # Calcular totales
    total_puntos = sum(v.get("puntos_nivel",0)+v.get("bonus_tiempo",0) for v in puntajes_acumulados.values())
    total_monedas = sum(v.get("monedas",0) for v in puntajes_acumulados.values())
    total_tiempo = sum(v.get("tiempo_total",0) for v in puntajes_acumulados.values())
    minutos = int(total_tiempo // 60)
    segundos = int(total_tiempo % 60)

    # Botones
    button_width, button_height = 250, 60
    menu_btn_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 150, button_width, button_height)
    exit_btn_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 250, button_width, button_height)

    # Música (igual que antes)
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

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(fondo, (0,0))

        # Mensaje central
        titulo = font.render("¡GANASTE!", True, (255, 215, 0))
        screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, HEIGHT//2 - 100))

        # Totales arriba a la derecha
        txt_puntos = small_font.render(f"Puntaje: {total_puntos}", True, (255, 255, 0))
        txt_monedas = small_font.render(f"Monedas: {total_monedas}", True, (255, 215, 0))
        txt_tiempo = small_font.render(f"Tiempo: {minutos}:{segundos:02d}", True, (255, 255, 255))

        screen.blit(txt_puntos, (WIDTH - txt_puntos.get_width() - 20, 20))
        screen.blit(txt_monedas, (WIDTH - txt_monedas.get_width() - 20, 50))
        screen.blit(txt_tiempo, (WIDTH - txt_tiempo.get_width() - 20, 80))

        # Dibujar botones
        # Botón Menú Principal
        menu_color = (100, 200, 100) if menu_btn_rect.collidepoint(mouse_pos) else (80, 160, 80)
        pygame.draw.rect(screen, menu_color, menu_btn_rect, border_radius=8)
        pygame.draw.rect(screen, (200, 255, 200), menu_btn_rect, 3, border_radius=8)
        menu_txt = button_font.render("Menú Principal", True, (255, 255, 255))
        screen.blit(menu_txt, (menu_btn_rect.centerx - menu_txt.get_width() // 2, 
                               menu_btn_rect.centery - menu_txt.get_height() // 2))

        # Botón Salir
        exit_color = (200, 80, 80) if exit_btn_rect.collidepoint(mouse_pos) else (160, 60, 60)
        pygame.draw.rect(screen, exit_color, exit_btn_rect, border_radius=8)
        pygame.draw.rect(screen, (255, 150, 150), exit_btn_rect, 3, border_radius=8)
        exit_txt = button_font.render("Salir", True, (255, 255, 255))
        screen.blit(exit_txt, (exit_btn_rect.centerx - exit_txt.get_width() // 2, 
                               exit_btn_rect.centery - exit_txt.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if menu_btn_rect.collidepoint(event.pos):
                        return "menu"
                    elif exit_btn_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

        pygame.display.flip()
        clock.tick(60)


def perdiste():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Perdiste")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)
    button_font = pygame.font.SysFont(None, 48)
    
    try:
        fondo = pygame.image.load("assets/menu/fondo.png").convert()
        fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
    except:
        fondo = pygame.Surface((WIDTH, HEIGHT))
        fondo.fill((20, 20, 40))
    
    # Botones
    button_width, button_height = 250, 60
    menu_btn_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 100, button_width, button_height)
    exit_btn_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 200, button_width, button_height)

    # Música (igual que antes)
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
            print(f"No se pudo iniciar el audio. Continuando sin sonido. Error: {e}")

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(fondo, (0,0))
        txt = font.render("PERDISTE", True, (255,0,0))
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 100))
        
        # Dibujar botones
        # Botón Menú Principal
        menu_color = (100, 200, 100) if menu_btn_rect.collidepoint(mouse_pos) else (80, 160, 80)
        pygame.draw.rect(screen, menu_color, menu_btn_rect, border_radius=8)
        pygame.draw.rect(screen, (200, 255, 200), menu_btn_rect, 3, border_radius=8)
        menu_txt = button_font.render("Menú Principal", True, (255, 255, 255))
        screen.blit(menu_txt, (menu_btn_rect.centerx - menu_txt.get_width() // 2, 
                               menu_btn_rect.centery - menu_txt.get_height() // 2))

        # Botón Salir
        exit_color = (200, 80, 80) if exit_btn_rect.collidepoint(mouse_pos) else (160, 60, 60)
        pygame.draw.rect(screen, exit_color, exit_btn_rect, border_radius=8)
        pygame.draw.rect(screen, (255, 150, 150), exit_btn_rect, 3, border_radius=8)
        exit_txt = button_font.render("Salir", True, (255, 255, 255))
        screen.blit(exit_txt, (exit_btn_rect.centerx - exit_txt.get_width() // 2, 
                               exit_btn_rect.centery - exit_txt.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if menu_btn_rect.collidepoint(event.pos):
                        return "menu"
                    elif exit_btn_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

        pygame.display.flip()
        clock.tick(60)


def pantalla_transicion_nivel(screen=None, WIDTH=None, HEIGHT=None, nivel=2, duracion_ms=1500):
    """Muestra una pantalla de transición indicando que se pasó al siguiente nivel."""
    creada_local = False
    if screen is None:
        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        WIDTH, HEIGHT = screen.get_size()
        creada_local = True

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 36)

    try:
        fondo = pygame.image.load("assets/menu/fondo.png").convert()
        fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
    except Exception:
        fondo = pygame.Surface((WIDTH, HEIGHT))
        fondo.fill((20, 20, 40))

    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < duracion_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if creada_local:
                    pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if creada_local:
                    pygame.event.clear()
                return

        screen.blit(fondo, (0, 0))
        title = font.render(f"¡Pasaste al Nivel {nivel}!", True, (255, 215, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60))
        instru = small_font.render("Presiona cualquier tecla para continuar...", True, (255, 255, 255))
        screen.blit(instru, (WIDTH // 2 - instru.get_width() // 2, HEIGHT // 2 + 20))

        pygame.display.flip()
        clock.tick(60)
