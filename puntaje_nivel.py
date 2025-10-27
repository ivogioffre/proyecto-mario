import pygame, sys, os

# Variable global para acumular tiempos de todos los niveles
tiempos_acumulados = {"nivel_1": 0, "nivel_2": 0}
# Variable global para acumular puntajes de todos los niveles
puntajes_acumulados = {"nivel_1": 0, "nivel_2": 0}

def main_puntaje(score, bonus_tiempo=0, tiempo_total=0, nivel=1, monedas=0):
    global tiempos_acumulados
    pygame.init()
    puntaje_total = score + bonus_tiempo

    # Guardar puntaje y tiempo del nivel actual
    puntajes_acumulados[f"nivel_{nivel}"] = puntaje_total
    tiempos_acumulados[f"nivel_{nivel}"] = tiempo_total

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Mariano bros")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)

    fondo = pygame.image.load("assets/menu/fondo.png").convert()
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

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
            print(f"No se pudo iniciar el audio del menú. Error: {e}")

    while True:
        screen.blit(fondo, (0, 0))
       
        if nivel == 2:
            titulo = font.render("¡JUEGO COMPLETADO!", True, (255, 215, 0))
        else:
            titulo = font.render("¡Nivel Completado!", True, (255, 255, 255))

        minutos = int(tiempo_total // 60)
        segundos = int(tiempo_total % 60)
        texto_nivel = small_font.render(f"Nivel {nivel}", True, (255, 255, 255))
        texto_tiempo = small_font.render(f"Tiempo Nivel {nivel}: {minutos}:{segundos:02d}", True, (255, 255, 255))
        texto_monedas = small_font.render(f"Monedas Recolectadas: {monedas}/84", True, (255, 255, 0))
        texto_puntos = small_font.render(f"Puntos: {score}", True, (255, 255, 255))
        texto_bonus = small_font.render(f"Bonus Tiempo: {bonus_tiempo}", True, (255, 255, 0))
        texto_total = small_font.render(f"Puntaje Nivel: {puntaje_total}", True, (255, 215, 0))
       
        y_offset = HEIGHT//2 - 220
       
        screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, y_offset))
        screen.blit(texto_nivel, (WIDTH//2 - texto_nivel.get_width()//2, y_offset + 60))
        screen.blit(texto_tiempo, (WIDTH//2 - texto_tiempo.get_width()//2, y_offset + 100))
        screen.blit(texto_monedas, (WIDTH//2 - texto_monedas.get_width()//2, y_offset + 140))
        screen.blit(texto_puntos, (WIDTH//2 - texto_puntos.get_width()//2, y_offset + 180))
        screen.blit(texto_bonus, (WIDTH//2 - texto_bonus.get_width()//2, y_offset + 220))
        screen.blit(texto_total, (WIDTH//2 - texto_total.get_width()//2, y_offset + 260))
       
        if nivel == 2:
            tiempo_total_juego = tiempos_acumulados["nivel_1"] + tiempos_acumulados["nivel_2"]
            min_total = int(tiempo_total_juego // 60)
            seg_total = int(tiempo_total_juego % 60)
           
            texto_tiempo_total = small_font.render(f"Tiempo Total: {min_total}:{seg_total:02d}", True, (255, 255, 0))
            screen.blit(texto_tiempo_total, (WIDTH//2 - texto_tiempo_total.get_width()//2, y_offset + 320))

            # Mostrar puntaje total del juego (suma de ambos niveles)
            puntaje_total_juego = puntajes_acumulados["nivel_1"] + puntajes_acumulados["nivel_2"]
            texto_total_juego = small_font.render(f"Puntaje Total: {puntaje_total_juego}", True, (255, 215, 0))
            screen.blit(texto_total_juego, (WIDTH//2 - texto_total_juego.get_width()//2, y_offset + 360))

            salir = small_font.render("Presiona ENTER o ESC para salir", True, (255, 255, 255))
            screen.blit(salir, (WIDTH//2 - salir.get_width()//2, y_offset + 380))
        else:
            salir = small_font.render("Presiona ENTER para continuar", True, (255, 255, 255))
            screen.blit(salir, (WIDTH//2 - salir.get_width()//2, y_offset + 310))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Cuando se presiona ENTER retornamos el puntaje correspondiente:
                    # - Si estamos en nivel 2, devolver el puntaje total del juego
                    # - Si no, devolver el puntaje del nivel actual
                    if nivel == 2:
                        tiempo_retorno = tiempos_acumulados["nivel_1"] + tiempos_acumulados["nivel_2"]
                        puntaje_retorno = puntajes_acumulados["nivel_1"] + puntajes_acumulados["nivel_2"]
                    else:
                        tiempo_retorno = tiempo_total
                        puntaje_retorno = puntaje_total
                    return (puntaje_retorno, tiempo_retorno, monedas)
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
        salir = small_font.render("Presiona ESC para salir", True, (255, 255, 255))

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
