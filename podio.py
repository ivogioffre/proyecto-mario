import pygame, os, sys

def podio():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Menú Principal")
    clock = pygame.time.Clock() # Controla los FPS

    fondo = pygame.image.load("assets/menu/fondo.png").convert()
    fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
    
    # Fuentes
    title_font = pygame.font.SysFont(None, 80)
    ranking_font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)
    
    # Botones
    button_width, button_height = 200, 60
    back_btn_rect = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT - 100, button_width, button_height)
    
    # Cargar y parsear puntajes desde Puntaje.txt
    records = []
    try:
        if os.path.exists("Puntaje.txt"):
            with open("Puntaje.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if line and "Monedas Obtenidas:" in line:
                        # Formato esperado: " Fecha y hora : YYYY-MM-DD HH:MM:SS - Monedas Obtenidas: X/ 84"
                        parts = line.split("Monedas Obtenidas:")
                        if len(parts) > 1:
                            try:
                                monedas_str = parts[1].split("/")[0].strip()
                                monedas = int(monedas_str)
                                fecha_str = parts[0].replace("Fecha y hora :", "").strip()
                                records.append({
                                    "fecha": fecha_str,
                                    "monedas": monedas,
                                    "puntos": monedas * 10  # Suponiendo 10 puntos por moneda
                                })
                            except:
                                pass
    except Exception as e:
        print(f"Error al cargar puntajes: {e}")
    
    # Ordenar por puntos (descendente)
    records.sort(key=lambda x: x["puntos"], reverse=True)
    
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
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(fondo, (0, 0))
        
        # Título
        titulo = title_font.render("PODIO", True, (255, 215, 0))
        screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 30))
        
        # Mostrar ranking
        y_pos = 150
        if top_records:
            for idx, record in enumerate(top_records, 1):
                # Cambiar color según posición
                if idx == 1:
                    color = (255, 215, 0)  # Oro
                    medal = "🥇"
                elif idx == 2:
                    color = (192, 192, 192)  # Plata
                    medal = "🥈"
                elif idx == 3:
                    color = (205, 127, 50)  # Bronce
                    medal = "🥉"
                else:
                    color = (255, 255, 255)
                    medal = f"{idx}."
                
                # Mostrar entrada del ranking
                ranking_text = f"{medal} Monedas: {record['monedas']}/84 | Puntos: {record['puntos']}"
                txt = ranking_font.render(ranking_text, True, color)
                screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, y_pos))
                y_pos += 60
        else:
            no_records = ranking_font.render("No hay récords aún", True, (255, 100, 100))
            screen.blit(no_records, (WIDTH // 2 - no_records.get_width() // 2, HEIGHT // 2))
        
        # Botón Volver
        back_color = (100, 200, 100) if back_btn_rect.collidepoint(mouse_pos) else (80, 160, 80)
        pygame.draw.rect(screen, back_color, back_btn_rect, border_radius=8)
        pygame.draw.rect(screen, (200, 255, 200), back_btn_rect, 3, border_radius=8)
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
                        return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        
        pygame.display.flip()
        clock.tick(60)