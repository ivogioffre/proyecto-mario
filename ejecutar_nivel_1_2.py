import pygame
from level import load_level
from level2 import load_level_2
from camera import Camera
from entities import Player, COIN_POP_EFFECTS, load_img
from puntaje_nivel import perdiste, main_puntaje
from puntaje import guardar_record
import time

def ejecutar_nivel(screen, WIDTH, HEIGHT, clock, nivel, vidas_iniciales=3, monedas_iniciales=0):
    FPS = 60
    fondo_img = None
    luna_img = None
    luna_rect = None

    tiempo_inicio = time.time()

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
    player.score = 0
    player.monedas = monedas_iniciales
    player.total_lives = vidas_iniciales
    player.current_hits = 1
    vidas = vidas_iniciales

    font = pygame.font.SysFont(None, 32)
    max_vidas = 3

    heart_full = pygame.transform.scale(load_img("assets/items/corazon.png"), (30, 30))
    heart_broken = pygame.transform.scale(load_img("assets/items/corazon_roto.png"), (30, 30))

    running = True
    while running:
        clock.tick(FPS)

        tiempo_actual = time.time() - tiempo_inicio
        minutos = int(tiempo_actual // 60)
        segundos = int(tiempo_actual % 60)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return 0, player.score, player.monedas, 0, 0
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return 0, player.score, player.monedas, 0, 0

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
                player.monedas = monedas_iniciales
                player.total_lives = vidas
                player.current_hits = 1
            else:
                perdiste()
                return 0, player.score, player.monedas, 0, 0

        # Detectar objetos especiales
        for heart in hearts[:]:
            if player.rect.colliderect(heart.rect):
                heart.apply(player)
                hearts.remove(heart)

        for fire_power in fire_powers[:]:
            if player.rect.colliderect(fire_power.rect):
                fire_power.apply(player)
                fire_powers.remove(fire_power)

        if player.level_completed:
            tiempo_total = time.time() - tiempo_inicio
            bonus_tiempo = calcular_bonus_tiempo(tiempo_total, nivel)

            puntaje_total, tiempo_final, monedas = main_puntaje(
                player.score, bonus_tiempo, tiempo_total, nivel, player.monedas
            )
            guardar_record(monedas, tiempo_final, puntaje_total)

            if nivel == 1:
                guardar_record(monedas, tiempo_final, puntaje_total)
                return ejecutar_nivel(screen, WIDTH, HEIGHT, clock, 2, vidas, player.monedas)
            else:
                guardar_record(monedas, tiempo_final, puntaje_total)
                # Devolver el tiempo final correcto (tiempo_final) en lugar de la variable inexistente 'tiempo'
                return vidas, puntaje_total, bonus_tiempo, tiempo_final, monedas

        # Dibujado
        if fondo_img:
            screen.blit(fondo_img, (0, 0))
        else:
            screen.fill((0, 0, 0) if nivel == 2 else color_fondo)

        if luna_img:
            screen.blit(luna_img, (luna_rect.x - camera.offset.x * 0.05, luna_rect.y))

        for group in [solids, grasses, coins, enemies, plants, clouds, flags]:
            for sprite in group:
                screen.blit(sprite.image, camera.apply(sprite.rect))

        for heart in hearts:
            screen.blit(heart.image, camera.apply(heart.rect))
        for fire_power in fire_powers:
            screen.blit(fire_power.image, camera.apply(fire_power.rect))

        screen.blit(player.image, camera.apply(player.rect))

        
        for effect in COIN_POP_EFFECTS[:]:
            
            alive = effect.update()
            if not alive:
                COIN_POP_EFFECTS.remove(effect)
            else:
                try:
                    screen.blit(effect.image, camera.apply(effect.rect))
                except Exception:
                    screen.blit(effect.image, effect.rect)

        # UI
        score_txt = font.render(f"Puntos: {player.score}", True, (255, 255, 255))
        monedas_txt = font.render(f"Monedas: {player.monedas}", True, (255, 215, 0))
        nivel_txt = font.render(f"Nivel: {nivel}", True, (255, 255, 255))
        tiempo_txt = font.render(f"Tiempo: {minutos}:{segundos:02d}", True, (255, 255, 255))
        
        screen.blit(score_txt, (20, 20))
        screen.blit(monedas_txt, (20, 50))
        screen.blit(nivel_txt, (20, 80))
        screen.blit(tiempo_txt, (20, 110))

        for i in range(max_vidas):
<<<<<<< Updated upstream
            if i < vidas:
                screen.blit(heart_full, (20 + i * 35, 90))
            else:
                screen.blit(heart_broken, (20 + i * 35, 90))

        # Mostrar vida extra
        if player.current_hits >= 2:
            heart_small = pygame.transform.scale(heart_powerup,(30, 30))
            screen.blit(heart_small, (20 + max_vidas * 35, 90))
            extra_txt = font.render("x1", True, (255, 255, 0))
            screen.blit(extra_txt, (25 + (max_vidas + 1) * 35, 95))

        # Indicador de poder de fuego
        if player.has_fire_power:
            fire_icon = pygame.transform.scale(load_img("assets/items/Morron.png"), (30, 30))
            screen.blit(fire_icon, (WIDTH - 70, 20))
            fire_txt = font.render("FIRE!", True, (255, 100, 0))
            screen.blit(fire_txt, (WIDTH - 130, 25))
=======
            heart = heart_full if i < vidas else heart_broken
            screen.blit(heart, (20 + i * 35, 150))
>>>>>>> Stashed changes

        pygame.display.flip()

    return vidas, player.score, player.monedas, 0, 0


def calcular_bonus_tiempo(tiempo_segundos, nivel):
    tiempos = [(60, 120, 180), (90, 150, 210)][nivel - 1]
    oro, plata, bronce = tiempos
    if tiempo_segundos <= oro:
        return 500
    elif tiempo_segundos <= plata:
        return 300
    elif tiempo_segundos <= bronce:
        return 150
    elif tiempo_segundos <= bronce * 2:
        return 50
    else:
        return 0
