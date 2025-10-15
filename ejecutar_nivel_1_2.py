import pygame
from level import load_level
from level2 import load_level_2
from camera import Camera
from entities import Player, COIN_POP_EFFECTS, load_img
from puntaje_nivel import perdiste
from puntaje import guardar_record




def ejecutar_nivel(screen, WIDTH, HEIGHT, clock, nivel, vidas_iniciales=3, monedas_iniciales=0):
    FPS = 60
    # Cargar el nivel correspondiente
    fondo_img = None
    luna_img = None
    luna_rect = None
    parallax_factor = 0.2  # factor de movimiento de la luna
    if nivel == 1:
        color_fondo = (135, 206, 235)  # Celeste
        player, solids, coins, enemies, plants, clouds, grasses, flags, hearts = load_level()
    else:
        # Nivel 2 con imagen de fondo
        try:
            fondo_img = pygame.image.load("assets/fondo.png").convert()
            fondo_img = pygame.transform.scale(fondo_img, (WIDTH, HEIGHT))
        except:
            print("No se pudo cargar fondo.png, se usará negro")
            fondo_img = None


        # Cargar luna estática con parallax
        try:
            luna_img = load_img("assets/Tiles/luna_nivel2.png", 150)  # tamaño ajustable
            luna_rect = luna_img.get_rect()
            luna_rect.center = (WIDTH // 2, 150)  # posición inicial
        except:
            print("No se pudo cargar luna_nivel.png")


        player, solids, coins, enemies, plants, clouds, grasses, flags, hearts = load_level_2()


    # Configurar cámara
    camera = Camera()


    # Configurar jugador con datos acumulados
    player.score = monedas_iniciales
    player.total_lives = vidas_iniciales
    player.current_hits = 1  # Empieza con 1 hit por defecto
    vidas = vidas_iniciales


    # Fuente y cantidad maxima de corazones
    font = pygame.font.SysFont(None, 32)
    max_vidas = 3



    # Cargar imagenes de corazones
    heart_full = pygame.transform.scale(load_img("assets/items/corazon.png"), (30, 30))
    heart_broken = pygame.transform.scale(load_img("assets/items/corazon_roto.png"), (30, 30))
    heart_powerup = pygame.transform.scale(load_img("assets/items/corazon_dorado.png"), (40, 40))


    running = True
    while running:
        clock.tick(FPS) # control de FPS




        # Eventos
        # Si el jugador sale guarda record en puntaje.txt
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                guardar_record(player.score)
                return 0, player.score
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                guardar_record(player.score)
                return 0, player.score


        # Input del jugador
        keys = pygame.key.get_pressed()
        player.update(keys)


        # Actualizar enemigos
        for enemy in enemies:
            enemy.update()


        # Actualizar cámara
        camera.update(player)


        # Si el jugador muere
        if not player.alive:
            vidas -= 1
            if vidas > 0:
                # Reiniciar nivel si aun quedan vidas
                if nivel == 1:
                    player, solids, coins, enemies, plants, clouds, grasses, flags, hearts = load_level()
                else:
                    player, solids, coins, enemies, plants, clouds, grasses, flags, hearts = load_level_2()
                player.score = monedas_iniciales  # Mantener monedas acumuladas
                player.total_lives = vidas
                player.current_hits = 1
            # Si no quedan vidas pasas a la  pantalla de derrota
            else:
                guardar_record(player.score)
                perdiste()
                return 0, player.score




        # Manejar power-ups de corazon
        for heart in hearts[:]:
            if player.rect.colliderect(heart.rect):
                heart.apply(player)
                hearts.remove(heart)




        # Nivel completado
        if player.level_completed:
            print(f"¡Nivel {nivel} completado!")
            return vidas, player.score


        # Renderizado
        if fondo_img:
            screen.blit(fondo_img, (0, 0))
        else:
            screen.fill((0, 0, 0) if nivel == 2 else color_fondo)


        # Dibujar luna fija en el fondo
        if luna_img:
            screen.blit(luna_img, (luna_rect.x - camera.offset.x * 0.05, luna_rect.y))






        # Dibujar entidades
        for sprite_list in [solids, grasses, coins, enemies, plants, clouds, flags]:
            for sprite in sprite_list:
                screen.blit(sprite.image, camera.apply(sprite.rect))




        # Dibujar corazones en el mapa
        for heart in hearts:
            screen.blit(heart.image, camera.apply(heart.rect))


        # Dibujar jugador
        screen.blit(player.image, camera.apply(player.rect))


        # Actualizar efectos de monedas
        for effect in COIN_POP_EFFECTS[:]:
            if not effect.update():
                COIN_POP_EFFECTS.remove(effect)
            else:
                screen.blit(effect.image, camera.apply(effect.rect))


        # UI - Score y nivel
        score_txt = font.render(f"Monedas: {player.score}", True, (255, 255, 255))
        nivel_txt = font.render(f"Nivel: {nivel}", True, (255, 255, 255))
        screen.blit(score_txt, (20, 20))
        screen.blit(nivel_txt, (20, 50))


        # Mostrar vidas como corazones llenos/rotos
        for i in range(max_vidas):
            if i < vidas:
                screen.blit(heart_full, (20 + i * 35, 90))
            else:
                screen.blit(heart_broken, (20 + i * 35, 90))




        # Mostrar vida extra (power-up) como corazon dorado grande
        if player.current_hits >= 2:
            extra_player = pygame.transform.scale(player.images["idle"][0], (30, 30))
            screen.blit(extra_player, (20 + max_vidas * 35, 85))
            status_txt = font.render("x1", True, (255, 255, 0))
            screen.blit(status_txt, (25 + (max_vidas + 1) * 35, 95))


        pygame.display.flip()


    return vidas, player.score


