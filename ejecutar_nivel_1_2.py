import pygame
from level import load_level
from level2 import load_level_2
from camera import Camera
from entities import Player, COIN_POP_EFFECTS, load_img
from puntaje_nivel import perdiste
from puntaje import guardar_record

def ejecutar_nivel(screen, WIDTH, HEIGHT, clock, nivel, vidas_iniciales=3, monedas_iniciales=0):
    FPS = 60
    fondo_img = None
    luna_img = None
    luna_rect = None
    parallax_factor = 0.2
    
    if nivel == 1:
        color_fondo = (135, 206, 235)
        player, solids, coins, enemies, plants, clouds, grasses, flags, hearts, fire_powers = load_level()
    else:
        try:
            fondo_img = pygame.image.load("assets/fondo.png").convert()
            fondo_img = pygame.transform.scale(fondo_img, (WIDTH, HEIGHT))
        except:
            print("No se pudo cargar fondo.png, se usará negro")
            fondo_img = None

        try:
            luna_img = load_img("assets/Tiles/luna_nivel2.png", 150)
            luna_rect = luna_img.get_rect()
            luna_rect.center = (WIDTH // 2, 150)
        except:
            print("No se pudo cargar luna_nivel.png")

        player, solids, coins, enemies, plants, clouds, grasses, flags, hearts, fire_powers = load_level_2()

    camera = Camera()
    player.score = monedas_iniciales
    player.total_lives = vidas_iniciales
    player.current_hits = 1
    vidas = vidas_iniciales

    font = pygame.font.SysFont(None, 32)
    max_vidas = 3


    # Cargar imagenes de corazones
    heart_full = pygame.transform.scale(load_img("assets/items/corazon.png"), (30, 30))
    heart_broken = pygame.transform.scale(load_img("assets/items/corazon_roto.png"), (30, 30))
    heart_powerup = pygame.transform.scale(load_img("assets/items/corazon_dorado.png"), (40, 40))

    running = True
    while running:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                guardar_record(player.score)
                return 0, player.score
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                guardar_record(player.score)
                return 0, player.score

        keys = pygame.key.get_pressed()
        player.update(keys)

        for enemy in enemies:
            enemy.update()

        camera.update(player)

        if not player.alive:
            vidas -= 1
            if vidas > 0:
                if nivel == 1:
                    player, solids, coins, enemies, plants, clouds, grasses, flags, hearts, fire_powers = load_level()
                else:
                    player, solids, coins, enemies, plants, clouds, grasses, flags, hearts, fire_powers = load_level_2()
                player.score = monedas_iniciales
                player.total_lives = vidas
                player.current_hits = 1
            else:
                guardar_record(player.score)
                perdiste()
                return 0, player.score

        # Manejar power-ups de corazón
        for heart in hearts[:]:
            if player.rect.colliderect(heart.rect):
                heart.apply(player)
                hearts.remove(heart)

        # Manejar power-ups de fuego
        for fire_power in fire_powers[:]:
            if player.rect.colliderect(fire_power.rect):
                fire_power.apply(player)
                fire_powers.remove(fire_power)

        if player.level_completed:
            print(f"¡Nivel {nivel} completado!")
            return vidas, player.score

        # Renderizado
        if fondo_img:
            screen.blit(fondo_img, (0, 0))
        else:
            screen.fill((0, 0, 0) if nivel == 2 else color_fondo)

        if luna_img:
            screen.blit(luna_img, (luna_rect.x - camera.offset.x * 0.05, luna_rect.y))

        # Dibujar entidades
        for sprite_list in [solids, grasses, coins, enemies, plants, clouds, flags]:
            for sprite in sprite_list:
                screen.blit(sprite.image, camera.apply(sprite.rect))

        # Dibujar corazones en el mapa
        for heart in hearts:
            screen.blit(heart.image, camera.apply(heart.rect))

        # Dibujar power-ups de fuego en el mapa
        for fire_power in fire_powers:
            screen.blit(fire_power.image, camera.apply(fire_power.rect))

        # Dibujar jugador
        screen.blit(player.image, camera.apply(player.rect))

        # Dibujar bolas de fuego
        for fireball in player.fireballs:
            screen.blit(fireball.image, camera.apply(fireball.rect))

        # Actualizar efectos de monedas
        for effect in COIN_POP_EFFECTS[:]:
            if not effect.update():
                COIN_POP_EFFECTS.remove(effect)
            else:
                screen.blit(effect.image, camera.apply(effect.rect))

        # UI
        score_txt = font.render(f"Monedas: {player.score}", True, (255, 255, 255))
        nivel_txt = font.render(f"Nivel: {nivel}", True, (255, 255, 255))
        screen.blit(score_txt, (20, 20))
        screen.blit(nivel_txt, (20, 50))

        # Mostrar vidas
        for i in range(max_vidas):
            if i < vidas:
                screen.blit(heart_full, (20 + i * 35, 90))
            else:
                screen.blit(heart_broken, (20 + i * 35, 90))

        # Mostrar vida extra
        if player.current_hits >= 2:
            extra_player = pygame.transform.scale(player.images["idle"][0], (30, 30))
            screen.blit(extra_player, (20 + max_vidas * 35, 85))
            status_txt = font.render("x1", True, (255, 255, 0))
            screen.blit(status_txt, (25 + (max_vidas + 1) * 35, 95))

        # Indicador de poder de fuego
        if player.has_fire_power:
            fire_icon = pygame.transform.scale(load_img("assets/items/Morron.png"), (30, 30))
            screen.blit(fire_icon, (WIDTH - 70, 20))
            fire_txt = font.render("FIRE!", True, (255, 100, 0))
            screen.blit(fire_txt, (WIDTH - 130, 25))

        pygame.display.flip()

    return vidas, player.score