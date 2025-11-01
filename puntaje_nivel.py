import pygame, sys, os

# Guardamos el desglose de puntos por nivel para mostrar el resumen final
puntajes_acumulados = {}

def guardar_puntaje_nivel(nivel, puntos_nivel, puntos_por_monedas, puntos_por_enemigos, bonus_tiempo, tiempo_total, monedas):
    """Guardar el desglose de puntaje para un nivel concreto.

    Se usa luego en la pantalla final para mostrar el resumen.
    """
    puntajes_acumulados[f"nivel_{nivel}"] = {
        "puntos_nivel": int(puntos_nivel),
        "puntos_por_monedas": int(puntos_por_monedas),
        "puntos_por_enemigos": int(puntos_por_enemigos),
        "bonus_tiempo": int(bonus_tiempo),
        "tiempo_total": float(tiempo_total),
        "monedas": int(monedas),
    }


def main_puntaje(monedas_total=0):
    """Muestra el resumen final cuando se completa el juego.

    Si `puntajes_acumulados` contiene datos de niveles, se muestra el detalle
    por nivel (puntos por monedas, enemigos, bonus por tiempo) y el total final.
    """
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Mariano bross - Puntaje Final")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)

    fondo = pygame.image.load("assets/menu/fondo.png").convert()
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

    # Calcular totales
    total_por_niveles = 0
    total_por_monedas = 0
    total_por_enemigos = 0
    total_bonus = 0
    for k, v in puntajes_acumulados.items():
        total_por_niveles += v.get("puntos_nivel", 0)
        total_por_monedas += v.get("puntos_por_monedas", 0)
        total_por_enemigos += v.get("puntos_por_enemigos", 0)
        total_bonus += v.get("bonus_tiempo", 0)

    puntaje_final = total_por_niveles + total_bonus

    while True:
        screen.blit(fondo, (0, 0))

        title = font.render("Resumen Final", True, (255, 215, 0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))

        y = 120
        # Mostrar por nivel
        for nivel in sorted(puntajes_acumulados.keys()):
            v = puntajes_acumulados[nivel]
            line = f"{nivel}: Puntos Nivel={v['puntos_nivel']}  (Monedas={v['puntos_por_monedas']}, Enemigos={v['puntos_por_enemigos']}, Bonus={v['bonus_tiempo']})  Tiempo={int(v['tiempo_total'])}s  MonedasRecolectadas={v['monedas']}"
            txt = small_font.render(line, True, (255, 255, 255))
            screen.blit(txt, (40, y))
            y += 40

        # Totales
        y += 20
        txt_totales = small_font.render(f"Total Puntos por Niveles: {total_por_niveles}", True, (255, 255, 0))
        screen.blit(txt_totales, (40, y)); y += 30
        txt_monedas = small_font.render(f"Total Puntos por Monedas: {total_por_monedas}", True, (255, 255, 0))
        screen.blit(txt_monedas, (40, y)); y += 30
        txt_enemigos = small_font.render(f"Total Puntos por Enemigos: {total_por_enemigos}", True, (255, 255, 0))
        screen.blit(txt_enemigos, (40, y)); y += 30
        txt_bonus = small_font.render(f"Bonificación por Tiempo Total: {total_bonus}", True, (255, 255, 0))
        screen.blit(txt_bonus, (40, y)); y += 30

        txt_final = font.render(f"Puntaje Final: {puntaje_final}", True, (255, 215, 0))
        screen.blit(txt_final, (WIDTH//2 - txt_final.get_width()//2, y + 20))

        instru = small_font.render("Presiona ENTER para salir, ESC para cerrar", True, (255, 255, 255))
        screen.blit(instru, (WIDTH//2 - instru.get_width()//2, HEIGHT - 80))

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


def perdiste():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 72)
    small_font = pygame.font.SysFont(None, 40)

    fondo = pygame.image.load("assets/menu/fondo.png").convert()
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

    while True:
        screen.blit(fondo, (0, 0))
        titulo = font.render("¡PERDISTE!", True, (255, 0, 0))
        salir = small_font.render("Presiona ESC para salir", True, (0, 0, 0))

        screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, HEIGHT//2 - 100))
        screen.blit(salir, (WIDTH//2 - salir.get_width()//2, HEIGHT//2 + 40))

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
    """Muestra una pantalla de transición indicando que se pasó al siguiente nivel.

    Si se pasa una superficie `screen` y sus dimensiones, la usa. Si no, crea
    una pantalla fullscreen temporal (comportamiento similar a otras funciones
    en este módulo).
    """
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
                # salir antes si el jugador presiona una tecla
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

    # Si creamos la pantalla localmente, no la cerramos aquí porque el flujo
    # superior puede querer seguir usando pygame; simplemente retornamos.
    return