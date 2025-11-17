import pygame, os, sys

def podio():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Podio - Top 10")
    clock = pygame.time.Clock()

    try:
        fondo = pygame.image.load("assets/menu/fondo.png").convert()
        fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
    except:
        fondo = pygame.Surface((WIDTH, HEIGHT))
        fondo.fill((20, 20, 40))
    
    # Fuentes
    title_font = pygame.font.SysFont(None, 90)
    ranking_font = pygame.font.SysFont(None, 42)
    detail_font = pygame.font.SysFont(None, 34)
    small_font = pygame.font.SysFont(None, 36)
    
    # Botones
    button_width, button_height = 220, 65
    back_btn_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT - 100, button_width, button_height)
    
    # Cargar y parsear puntajes desde Puntaje.txt
    records = []
    try:
        if os.path.exists("Puntaje.txt"):
            with open("Puntaje.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and "Monedas Obtenidas:" in line:
                        try:
                            # Formato: Fecha y hora: YYYY-MM-DD HH:MM:SS - Monedas Obtenidas: X/84 - Puntos Totales: Y - Tiempo: M:SS - Puntos por Enemigos: Z
                            parts = line.split(" - ")
                            
                            # Extraer fecha
                            fecha_str = parts[0].replace("Fecha y hora:", "").strip()
                            
                            # Extraer monedas
                            monedas_part = [p for p in parts if "Monedas Obtenidas:" in p][0]
                            monedas = int(monedas_part.split(":")[1].split("/")[0].strip())
                            
                            # Extraer puntos totales
                            puntos_part = [p for p in parts if "Puntos Totales:" in p]
                            puntos = int(puntos_part[0].split(":")[1].strip()) if puntos_part else monedas * 10
                            
                            # Extraer tiempo (formato M:SS o MM:SS)
                            tiempo_part = [p for p in parts if "Tiempo:" in p]
                            tiempo_str = "0:00"
                            tiempo_total_segundos = 0
                            
                            if tiempo_part:
                                tiempo_str = tiempo_part[0].split("Tiempo:")[1].strip()
                                # Convertir tiempo a segundos totales para ordenar
                                try:
                                    tiempo_parts = tiempo_str.split(":")
                                    minutos = int(tiempo_parts[0])
                                    segundos = int(tiempo_parts[1])
                                    tiempo_total_segundos = minutos * 60 + segundos
                                except:
                                    tiempo_total_segundos = 0
                            
                            # Extraer puntos por enemigos
                            enemigos_part = [p for p in parts if "Puntos por Enemigos:" in p]
                            puntos_enemigos = int(enemigos_part[0].split(":")[1].strip()) if enemigos_part else 0
                            
                            records.append({
                                "fecha": fecha_str,
                                "monedas": monedas,
                                "puntos": puntos,
                                "tiempo": tiempo_str,
                                "tiempo_total": tiempo_total_segundos,
                                "puntos_enemigos": puntos_enemigos
                            })
                        except Exception as e:
                            print(f"Error parseando línea: {e}")
                            pass
    except Exception as e:
        print(f"Error al cargar puntajes: {e}")
    
    # Ordenar por puntos (descendente), y si empatan, por tiempo (ascendente = menos tiempo es mejor)
    records.sort(key=lambda x: (-x["puntos"], x["tiempo_total"]))
    
    # Limitar a top 10
    top_records = records[:10]
    
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
            print(f"No se pudo iniciar el audio. Continuando sin sonido. Error: {e}")
    
    # Scroll para ver más detalles
    scroll_y = 0
    max_scroll = max(0, len(top_records) * 120 - (HEIGHT - 350))
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(fondo, (0, 0))
        
        # Título con efecto de sombra
        shadow_title = title_font.render("PODIO - TOP 10", True, (100, 80, 0))
        screen.blit(shadow_title, (WIDTH // 2 - shadow_title.get_width() // 2 + 3, 33))
        titulo = title_font.render("PODIO - TOP 10", True, (255, 215, 0))
        screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 30))
        
        # Subtítulo
        subtitle = small_font.render("Los mejores puntajes del juego", True, (200, 200, 200))
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 110))
        
        # Línea decorativa
        pygame.draw.line(screen, (255, 215, 0), (WIDTH // 2 - 400, 145), (WIDTH // 2 + 400, 145), 4)
        
        # Mostrar ranking
        y_pos = 180 - scroll_y
        if top_records:
            for idx, record in enumerate(top_records, 1):
                # Verificar si está visible en pantalla
                if y_pos > -120 and y_pos < HEIGHT - 80:
                    # Cambiar color según posición
                    if idx == 1:
                        bg_color = (60, 50, 0)
                        text_color = (255, 215, 0)  # Oro
                        medal = "ORO"
                        border_width = 3
                    elif idx == 2:
                        bg_color = (40, 40, 40)
                        text_color = (192, 192, 192)  # Plata
                        medal = "PLATA"
                        border_width = 3
                    elif idx == 3:
                        bg_color = (50, 35, 20)
                        text_color = (205, 127, 50)  # Bronce
                        medal = "BRONCE"
                        border_width = 3
                    else:
                        bg_color = (30, 30, 50)
                        text_color = (255, 255, 255)
                        medal = f"#{idx}"
                        border_width = 2
                    
                    # Dibujar fondo del récord
                    record_rect = pygame.Rect(WIDTH // 2 - 420, y_pos - 5, 840, 110)
                    pygame.draw.rect(screen, bg_color, record_rect, border_radius=10)
                    pygame.draw.rect(screen, text_color, record_rect, border_width, border_radius=10)
                    
                    # Mostrar entrada del ranking - Línea principal
                    ranking_text = f"{medal} - {record['puntos']} PUNTOS"
                    txt = ranking_font.render(ranking_text, True, text_color)
                    screen.blit(txt, (WIDTH // 2 - 400, y_pos + 5))
                    
                    # Detalles en línea secundaria - Primera fila
                    detail_text1 = f"     Monedas: {record['monedas']}/84  |  Tiempo Total: {record['tiempo']}  |  Enemigos: {record['puntos_enemigos']} pts"
                    detail_txt1 = detail_font.render(detail_text1, True, (220, 220, 220))
                    screen.blit(detail_txt1, (WIDTH // 2 - 400, y_pos + 45))
                    
                    # Fecha - Segunda fila
                    fecha_txt = detail_font.render(f"     Fecha: {record['fecha']}", True, (180, 180, 180))
                    screen.blit(fecha_txt, (WIDTH // 2 - 400, y_pos + 75))
                    
                y_pos += 120
        else:
            # Mensaje cuando no hay récords
            no_records_bg = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 80, 600, 160)
            pygame.draw.rect(screen, (40, 40, 60), no_records_bg, border_radius=15)
            pygame.draw.rect(screen, (100, 100, 150), no_records_bg, 3, border_radius=15)
            
            no_records = ranking_font.render("No hay récords aún", True, (255, 100, 100))
            subtitle = detail_font.render("¡Juega y establece el primer récord!", True, (200, 200, 200))
            screen.blit(no_records, (WIDTH // 2 - no_records.get_width() // 2, HEIGHT // 2 - 40))
            screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 2 + 10))
        
        # Indicadores de scroll si hay más contenido
        if scroll_y > 0:
            arrow_up = small_font.render("^ Arriba", True, (200, 200, 200))
            arrow_up_bg = pygame.Rect(WIDTH - arrow_up.get_width() - 40, 155, arrow_up.get_width() + 20, 40)
            pygame.draw.rect(screen, (50, 50, 70), arrow_up_bg, border_radius=8)
            screen.blit(arrow_up, (WIDTH - arrow_up.get_width() - 30, 160))
            
        if scroll_y < max_scroll:
            arrow_down = small_font.render("v Abajo", True, (200, 200, 200))
            arrow_down_bg = pygame.Rect(WIDTH - arrow_down.get_width() - 40, HEIGHT - 180, arrow_down.get_width() + 20, 40)
            pygame.draw.rect(screen, (50, 50, 70), arrow_down_bg, border_radius=8)
            screen.blit(arrow_down, (WIDTH - arrow_down.get_width() - 30, HEIGHT - 175))
        
        # Botón Volver con efecto hover mejorado
        back_color = (120, 220, 120) if back_btn_rect.collidepoint(mouse_pos) else (80, 160, 80)
        pygame.draw.rect(screen, back_color, back_btn_rect, border_radius=10)
        pygame.draw.rect(screen, (200, 255, 200), back_btn_rect, 4, border_radius=10)
        back_txt = small_font.render("Volver", True, (255, 255, 255))
        screen.blit(back_txt, (back_btn_rect.centerx - back_txt.get_width() // 2,
                               back_btn_rect.centery - back_txt.get_height() // 2))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_btn_rect.collidepoint(event.pos):
                        running = False
                        return
                # Scroll con rueda del mouse
                elif event.button == 4:  # Scroll arriba
                    scroll_y = max(0, scroll_y - 40)
                elif event.button == 5:  # Scroll abajo
                    scroll_y = min(max_scroll, scroll_y + 40)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return
                # Scroll con flechas
                elif event.key == pygame.K_UP:
                    scroll_y = max(0, scroll_y - 60)
                elif event.key == pygame.K_DOWN:
                    scroll_y = min(max_scroll, scroll_y + 60)
                # Scroll con Page Up/Down
                elif event.key == pygame.K_PAGEUP:
                    scroll_y = max(0, scroll_y - 200)
                elif event.key == pygame.K_PAGEDOWN:
                    scroll_y = min(max_scroll, scroll_y + 200)
                # Ir al inicio/final
                elif event.key == pygame.K_HOME:
                    scroll_y = 0
                elif event.key == pygame.K_END:
                    scroll_y = max_scroll
        
        pygame.display.flip()
        clock.tick(60)