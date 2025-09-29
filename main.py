# main.py - CORRECCIONES
import pygame
import sys
from puntaje import guardar_record
from menu import main_menu
from level import load_level
from level2 import load_level_2
from camera import Camera
from entities import Player, COIN_POP_EFFECTS, load_img
from puntaje_nivel import main_puntaje, perdiste


FPS = 60


def main():
    pygame.init()


    # Ventana pantalla completa
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Mario Bros")


    # Música
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("assets/musica/12. Overworld.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    except Exception as e:
        print(f"No se pudo iniciar el audio: {e}")


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




def ejecutar_nivel(screen, WIDTH, HEIGHT, clock, nivel, vidas_iniciales=3, monedas_iniciales=0):
    # Cargar el nivel correspondiente
    if nivel == 1:
        color_fondo = (135, 206, 235)  # Celeste
        player, solids, coins, enemies, plants, clouds, grasses, flags, hearts = load_level()
    else:
        color_fondo = (10, 15, 40)  # Oscuro para nivel 2
        player, solids, coins, enemies, plants, clouds, grasses, flags, hearts = load_level_2()


    # Configurar cámara
    camera = Camera()


    # Configurar jugador con datos acumulados
    player.score = monedas_iniciales
    player.total_lives = vidas_iniciales
    player.current_hits = 1  # Empieza con 1 hit por defecto
    vidas = vidas_iniciales


    font = pygame.font.SysFont(None, 32)
    max_vidas = 3


    # Cargar imágenes de corazones
    heart_full = pygame.transform.scale(load_img("assets/items/corazon.png"), (30, 30))
    heart_broken = pygame.transform.scale(load_img("assets/items/corazon_roto.png"), (30, 30))
    heart_powerup = pygame.transform.scale(load_img("assets/items/corazon_dorado.png"), (40, 40))


    running = True
    while running:
        clock.tick(FPS)


        # Eventos
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
                # Reiniciar nivel
                if nivel == 1:
                    player, solids, coins, enemies, plants, clouds, grasses, flags, hearts = load_level()
                else:
                    player, solids, coins, enemies, plants, clouds, grasses, flags, hearts = load_level_2()
                player.score = monedas_iniciales  # Mantener monedas acumuladas
                player.total_lives = vidas
                player.current_hits = 1
            else:
                perdiste()
                return 0, player.score


        # Manejar power-ups de corazón
        for heart in hearts[:]:
            if player.rect.colliderect(heart.rect):
                heart.apply(player)
                hearts.remove(heart)


        # CORREGIDO: Si toca la bandera (nivel completado)
        if player.level_completed:
            print(f"¡Nivel {nivel} completado!")
            return vidas, player.score


        # Renderizado
        screen.fill(color_fondo)


        # Dibujar entidades
        for sprite_list in [solids, grasses, coins, enemies, plants, clouds, flags]:
            for sprite in sprite_list:
                screen.blit(sprite.image, camera.apply(sprite.rect))


        # Dibujar corazones de power-up
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


        # Mostrar vida extra (power-up) como corazón dorado grande
        if player.current_hits >= 2:
            extra_player = pygame.transform.scale(player.images["idle"][0], (30, 30))
            screen.blit(extra_player, (20 + max_vidas * 35, 85))
            status_txt = font.render("x1", True, (255, 255, 0))
            screen.blit(status_txt, (25 + (max_vidas + 1) * 35, 95))


       
        pygame.display.flip()


    return vidas, player.score


if __name__ == "__main__":
    main_menu()
    main()