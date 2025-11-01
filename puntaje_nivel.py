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
        screen.blit(fondo, (0,0))

        # Mensaje central
        titulo = font.render("¡GANASTE!", True, (255, 215, 0))
        screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, HEIGHT//2 - 100))

        instru = small_font.render("Presiona ESC para salir", True, (255,255,255))
        screen.blit(instru, (WIDTH//2 - instru.get_width()//2, HEIGHT//2 + 50))

        # Totales arriba a la derecha
        txt_puntos = small_font.render(f"Puntaje: {total_puntos}", True, (255, 255, 0))
        txt_monedas = small_font.render(f"Monedas: {total_monedas}", True, (255, 215, 0))
        txt_tiempo = small_font.render(f"Tiempo: {minutos}:{segundos:02d}", True, (255, 255, 255))

        screen.blit(txt_puntos, (WIDTH - txt_puntos.get_width() - 20, 20))
        screen.blit(txt_monedas, (WIDTH - txt_monedas.get_width() - 20, 50))
        screen.blit(txt_tiempo, (WIDTH - txt_tiempo.get_width() - 20, 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

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
    while True:
        screen.fill((0,0,0))
        txt = font.render("PERDISTE", True, (255,0,0))
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 50))
        instru = small_font.render("Presiona ESC para salir", True, (255,255,255))
        screen.blit(instru, (WIDTH//2 - instru.get_width()//2, HEIGHT//2 + 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

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
