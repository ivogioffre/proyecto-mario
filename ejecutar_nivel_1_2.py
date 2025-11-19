import pygame
from level import load_level
from level2 import load_level_2
from level3 import load_level_3  #  Nuevo nivel 3
from camera import Camera
from entities import Player, COIN_POP_EFFECTS, load_img
# Para recargar keymap dinámicamente
try:
    from Menu_config import load_config
except Exception:
    def load_config():
        return {}
from camera import Camera
from entities import Player, COIN_POP_EFFECTS, load_img
import puntaje_nivel
from puntaje import guardar_record
import time


def ejecutar_nivel(screen, WIDTH, HEIGHT, clock, nivel, vidas_iniciales=3, monedas_iniciales=0):
    FPS = 60
    fondo_img = None
    luna_img = None
    luna_rect = None
    parallax_factor = 0.2

    # ==========================
    # CARGA DE NIVELES
    # ==========================
    if nivel == 1:
        color_fondo = (135, 206, 235)
        player, solids, coins, enemies, plants, clouds, grasses, flags, hearts, fire_powers = load_level()

    elif nivel == 2:
        try:
            fondo_img = pygame.image.load("assets/fondo.png").convert()
            fondo_img = pygame.transform.scale(fondo_img, (WIDTH, HEIGHT))
        except:
            print("No se pudo cargar fondo.png se usará negro")
            fondo_img = None

        try:
            luna_img = load_img("assets/Tiles/luna_nivel2.png", 150)
            luna_rect = luna_img.get_rect()
            luna_rect.center = (WIDTH // 2, 150)
        except:
            print("No se pudo cargar luna_nivel.png")

        player, solids, coins, enemies, plants, clouds, grasses, flags, hearts, fire_powers = load_level_2()

    else:
        #  Nivel 3 
        try:
            fondo_img = pygame.image.load("assets/ciudad.png").convert()
            fondo_img = pygame.transform.scale(fondo_img, (WIDTH, HEIGHT))
        except:
            print("No se pudo cargar ciudad.png se usará color de fondo")
            fondo_img = None

        color_fondo = (255, 200, 150)
        player, solids, coins, enemies, plants, clouds, grasses, flags, hearts, fire_powers = load_level_3()

    # ==========================
    # VARIABLES DE NIVEL
    # ==========================
    camera = Camera()
    tiempo_inicio = time.time()
    player.score = monedas_iniciales
    player.total_lives = vidas_iniciales
    player.current_hits = 1
    vidas = vidas_iniciales
    font = pygame.font.SysFont(None, 32)
    max_vidas = 3

    # ==========================
    # CARGAR IMÁGENES DE HUD
    # ==========================
    heart_full = pygame.transform.scale(load_img("assets/items/corazon.png"), (30, 30))
    heart_broken = pygame.transform.scale(load_img("assets/items/corazon_roto.png"), (30, 30))
    heart_powerup = pygame.transform.scale(load_img("assets/items/corazon_dorado.png"), (40, 40))

    # ==========================
    # BUCLE PRINCIPAL
    # ==========================
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
              # Recargar configuración cada frame (ligero JSON). Si cambió en el menú, lo aplicamos al player.
        try:
            cfg = load_config() or {}
            new_keys = cfg.get('keys') if isinstance(cfg, dict) else None
            if new_keys and hasattr(player, 'keymap'):
                # Convertir valores a int por si vienen como strings
                for k, v in list(new_keys.items()):
                    try:
                        new_keys[k] = int(v)
                    except Exception:
                        pass
                # actualizar in-place conservando defaults si faltan
                player.keymap.update(new_keys)
        except Exception:
            pass
        player.update(keys)

        for enemy in enemies:
            enemy.update()

        camera.update(player)

        # --------------------------
        # VIDAS Y REINICIO
        # --------------------------
        if not player.alive:
            vidas -= 1
            if vidas > 0:
                if nivel == 1:
                    player, solids, coins, enemies, plants, clouds, grasses, flags, hearts, fire_powers = load_level()
                elif nivel == 2:
                    player, solids, coins, enemies, plants, clouds, grasses, flags, hearts, fire_powers = load_level_2()
                else:
                    player, solids, coins, enemies, plants, clouds, grasses, flags, hearts, fire_powers = load_level_3()

                player.score = monedas_iniciales
                player.total_lives = vidas
                player.current_hits = 1
            else:
                guardar_record(player.score)
                resultado = puntaje_nivel.perdiste()
                if resultado == "menu":
                    return 0, player.score, "menu"
                return 0, player.score

        # --------------------------
        # POWER-UPS
        # --------------------------
        for heart in hearts[:]:
            if player.rect.colliderect(heart.rect):
                heart.apply(player)
                hearts.remove(heart)

        for fire_power in fire_powers[:]:
            if player.rect.colliderect(fire_power.rect):
                fire_power.apply(player)
                fire_powers.remove(fire_power)

        # --------------------------
        # NIVEL COMPLETADO
        # --------------------------
        if player.level_completed:
            tiempo_total = time.time() - tiempo_inicio
            puntaje_tiempo = calcular_bonus_tiempo(tiempo_total)

            try:
                puntaje_nivel.guardar_puntaje_nivel(
                    nivel,
                    player.puntos_nivel,
                    player.puntos_por_monedas,
                    player.puntos_por_enemigos,
                    puntaje_tiempo,
                    tiempo_total,
                    getattr(player, 'monedas', player.score),
                )
            except Exception:
                pass

            print(f"Nivel {nivel} completado. Puntos nivel: {player.puntos_nivel}, bonus tiempo: {puntaje_tiempo}")
            return vidas, player.score

        # ==========================
        # DIBUJADO
        # ==========================
        if nivel == 3:
            # Color del cielo de la imagen (para que no haya diferencia)
            cielo_color = (173, 216, 255)

            # Relleno del cielo arriba
            screen.fill(cielo_color)

            # Fondo bajado un poco
            if fondo_img:
                screen.blit(fondo_img, (0, 80))
        else:
            # Otros niveles funcionan igual que antes
            if fondo_img:
                screen.blit(fondo_img, (0, 0))
            else:
                screen.fill((0, 0, 0) if nivel == 2 else color_fondo)


                if luna_img:
                    screen.blit(luna_img, (luna_rect.x - camera.offset.x * 0.05, luna_rect.y))

        for sprite_list in [solids, grasses, coins, enemies, plants, clouds, flags]:
            for sprite in sprite_list:
                screen.blit(sprite.image, camera.apply(sprite.rect))

        for heart in hearts:
            screen.blit(heart.image, camera.apply(heart.rect))

        for fire_power in fire_powers:
            screen.blit(fire_power.image, camera.apply(fire_power.rect))

        screen.blit(player.image, camera.apply(player.rect))

        for fireball in player.fireballs:
            screen.blit(fireball.image, camera.apply(fireball.rect))

        for effect in COIN_POP_EFFECTS[:]:
            if not effect.update():
                COIN_POP_EFFECTS.remove(effect)
            else:
                screen.blit(effect.image, camera.apply(effect.rect))

        # --------------------------
        # HUD (PUNTAJES, VIDAS, ETC)
        # --------------------------
        tiempo_actual = time.time() - tiempo_inicio
        minutos = int(tiempo_actual // 60)
        segundos = int(tiempo_actual % 60)
        tiempo_txt = font.render(f"Tiempo: {minutos}:{segundos:02d}", True, (255, 255, 255))

        puntos_actual_nivel = getattr(player, 'puntos_nivel', 0)
        puntos_previos = 0
        try:
            for k, v in puntaje_nivel.puntajes_acumulados.items():
                puntos_previos += v.get('puntos_nivel', 0) + v.get('bonus_tiempo', 0)
        except Exception:
            puntos_previos = 0

        puntaje_total_actual = puntos_previos + puntos_actual_nivel
        puntos_nivel_txt = font.render(f"Puntos Nivel: {puntos_actual_nivel}", True, (255, 255, 255))
        puntaje_total_txt = font.render(f"Puntaje Total: {puntaje_total_actual}", True, (255, 215, 0))
        monedas_txt = font.render(f"Monedas: {player.score}", True, (255, 215, 0))
        nivel_txt = font.render(f"Nivel: {nivel}", True, (255, 255, 255))

        screen.blit(puntos_nivel_txt, (20, 20))
        screen.blit(puntaje_total_txt, (20, 50))
        screen.blit(monedas_txt, (20, 80))
        screen.blit(nivel_txt, (20, 110))
        screen.blit(tiempo_txt, (20, 140))

        hearts_y = HEIGHT - 90
        for i in range(max_vidas):
            x_pos = 20 + i * 35
            if i < vidas:
                screen.blit(heart_full, (x_pos, hearts_y))
            else:
                screen.blit(heart_broken, (x_pos, hearts_y))

        if player.current_hits >= 2:
            heart_small = pygame.transform.scale(heart_powerup, (30, 30))
            extra_x = 20 + max_vidas * 35
            screen.blit(heart_small, (extra_x, hearts_y))
            extra_txt = font.render("x1", True, (255, 255, 0))
            screen.blit(extra_txt, (extra_x + 5, hearts_y + 35))

        if player.has_fire_power:
            fire_icon = pygame.transform.scale(load_img("assets/items/Morron.png"), (30, 30))
            screen.blit(fire_icon, (WIDTH - 70, 20))
            fire_txt = font.render("FIRE!", True, (255, 100, 0))
            screen.blit(fire_txt, (WIDTH - 130, 25))

        pygame.display.flip()

    return vidas, player.score


def calcular_bonus_tiempo(tiempo_segundos):
    """Calcula bonificación por tiempo según: <1 min: +100, 1-2 min: +50, 2-3 min: +25, >3 min: 0"""
    if tiempo_segundos < 60:
        return 100
    elif tiempo_segundos < 120:
        return 50
    elif tiempo_segundos < 180:
        return 25
    else:
        return 0
