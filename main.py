import pygame, sys, os
from menu import main_menu
from level import load_level
from camera import Camera
from entities import Player, COIN_POP_EFFECTS
from Items import FIREBALLS

WIDTH, HEIGHT = 960, 540
FPS = 60
color_fondo = (135, 206, 235)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Mario Bros")

    if not pygame.mixer.get_init():
        os.environ["SDL_AUDIODRIVER"] = "dummy"

    try:
        pygame.mixer.init()
        pygame.mixer.music.load("assets/musica/12. Overworld.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    except Exception as e:
        print(f"No se pudo iniciar el audio. Continuando sin sonido. Error: {e}")

    player, solids, coins, enemies, plants, clouds, grasses = load_level()
    camera = Camera()
    font = pygame.font.SysFont(None, 32)

    running = True
    while running:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        player.update(keys)
        for enemy in enemies:
            enemy.update()
        camera.update(player)

        if not player.alive:
            player, solids, coins, enemies, plants, clouds, grasses = load_level()

        screen.fill(color_fondo)

        for sprite_list in [solids, grasses, coins, enemies, plants, clouds]:
            for sprite in sprite_list:
                screen.blit(sprite.image, camera.apply(sprite.rect))
        screen.blit(player.image, camera.apply(player.rect))

        
        for fireball in FIREBALLS[:]:
            if not fireball.update():
                FIREBALLS.remove(fireball)
            else:
                screen.blit(fireball.image, camera.apply(fireball.rect))
        
        for effect in COIN_POP_EFFECTS[:]:
            if not effect.update():
                COIN_POP_EFFECTS.remove(effect)
            else:
                screen.blit(effect.image, camera.apply(effect.rect))



        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()
    main()
