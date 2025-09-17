#importamos todos los archivos
import pygame, sys, os
from puntaje import guardar_record
from menu import main_menu
from level import load_level       # nivel 1
from level2 import load_level_2    # nivel 2
from camera import Camera
from entities import Player, COIN_POP_EFFECTS
from puntaje_nivel import main_puntaje, perdiste

#establecemos los fps y el color de fondo (celeste)
FPS = 60
color_fondo = (135, 206, 235)

# -------- MAIN --------
def main():
    pygame.init()

    # Ventana pantalla completa
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Mario Bros")

    # Ejecutamos nivel 1
    vidas, monedas = ejecutar_nivel(screen, WIDTH, HEIGHT, clock, 1)

    if vidas > 0:  # Si completaste nivel 1
        # Ejecutamos nivel 2
        vidas, monedas = ejecutar_nivel(screen, WIDTH, HEIGHT, clock, 2, vidas, monedas)

        if vidas > 0:  # Si completaste nivel 2
            guardar_record(monedas)
            main_puntaje(monedas)

    pygame.quit()
    sys.exit()

# -------- FUNCION EJECUTAR NIVEL --------
def ejecutar_nivel(screen, WIDTH, HEIGHT, clock, nivel, vidas_iniciales=3, monedas_iniciales=0):
    # Cargar el nivel correspondiente
    if nivel == 1:
        color_fondo = (135, 206, 235)
        player, solids, coins, enemies, plants, clouds, grasses, flags = load_level()
    else:
        color_fondo = (10, 15, 40)
        player, solids, coins, enemies, plants, clouds, grasses, flags = load_level_2()

    camera = Camera()
    font = pygame.font.SysFont(None, 32)

    # Configurar jugador con datos acumulados
    player.score = monedas_iniciales
    vidas = vidas_iniciales

    # Cargar imágenes de corazones
    heart_full = pygame.image.load("assets/items/corazon.png").convert_alpha()
    heart_full = pygame.transform.scale(heart_full, (40, 40))
    heart_broken = pygame.image.load("assets/items/corazon_roto.png").convert_alpha()
    heart_broken = pygame.transform.scale(heart_broken, (40, 40))

    running = True
    while running:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                guardar_record(player.score)  # guardar si se sale con X
                return 0, player.score
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                guardar_record(player.score)  # guardar si se sale con ESC
                return 0, player.score

        keys = pygame.key.get_pressed()
        player.update(keys)
        for enemy in enemies:
            enemy.update()
        camera.update(player)

        # Si el jugador muere
        if not player.alive:
            vidas -= 1
            if vidas > 0:
                if nivel == 1:
                    player, solids, coins, enemies, plants, clouds, grasses, flags = load_level()
                else:
                    player, solids, coins, enemies, plants, clouds, grasses, flags = load_level_2()
                player.score = monedas_iniciales  # mantiene monedas acumuladas
            else:
                perdiste()
                return 0, player.score

        # Si toca la bandera (nivel completado)
        for flag in flags:
            if player.rect.colliderect(flag.rect):
                return vidas, player.score

        # Pintar fondo
        screen.fill(color_fondo)

        # Dibujar entidades
        for sprite_list in [solids, grasses, coins, enemies, plants, clouds, flags]:
            for sprite in sprite_list:
                screen.blit(sprite.image, camera.apply(sprite.rect))
        screen.blit(player.image, camera.apply(player.rect))

        # Efecto monedas
        for effect in COIN_POP_EFFECTS[:]:
            if not effect.update():
                COIN_POP_EFFECTS.remove(effect)
            else:
                screen.blit(effect.image, camera.apply(effect.rect))

        # Mostrar HUD
        score_txt = font.render(f"Monedas: {player.score}", True, (255, 255, 255))
        nivel_txt = font.render(f"Nivel: {nivel}", True, (255, 255, 255))
        screen.blit(score_txt, (20, 20))
        screen.blit(nivel_txt, (20, 50))

        # Dibujar vidas
        for i in range(3):
            if i < vidas:
                screen.blit(heart_full, (20 + i * 50, 90))
            else:
                screen.blit(heart_broken, (20 + i * 50, 90))

        pygame.display.flip()

    return vidas, player.score

# -------- EJECUCION --------
if __name__ == "__main__":
    main_menu()
    main()
