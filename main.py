#importamos todos los archivos
import pygame, sys, os
from menu import main_menu
from level import load_level
from camera import Camera
from entities import Player, COIN_POP_EFFECTS
from puntaje_nivel import main_puntaje

#establecemos los fps y el color de fondo (celeste)
FPS = 60
color_fondo = (135, 206, 235)

#ejecutamos el main
def main():
    # Cargamos la música
    musica = load_level()
    pygame.init()

    # Ventana pantalla completa
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size() # Obtener dimensiones de la pantalla
    clock = pygame.time.Clock()
    pygame.display.set_caption("Mario Bros") # Título de la ventana

    # ponemos musica de foindo
    if musica == False:
        pass
    else:
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("assets/musica/12. Overworld.mp3") #establecemos la musica
            pygame.mixer.music.play(-1) #bucle
            pygame.mixer.music.set_volume(0.5) #ajuste volumen
        except Exception as e:
            print(f"No se pudo iniciar el audio. Continuando sin sonido. Error: {e}")

    #carga del nivel
    player, solids, coins, enemies, plants, clouds, grasses, flags = load_level()
    camera = Camera() #ponemos la camara
    font = pygame.font.SysFont(None, 32)

    
    running = True #indica que el juego esta corriendo
    while running:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False #salir si se aprieta escape

        keys = pygame.key.get_pressed() # reconoce las teclas que se presionan
        player.update(keys) # actualizamos al jugador
        for enemy in enemies:
            enemy.update()#los enemigos se mueven con animaciones
        camera.update(player) #la camara se mueve con el jugador

        #si el jugador muere se reinicia el nivel
        if not player.alive:
            player, solids, coins, enemies, plants, clouds, grasses , flags  = load_level()
        
        for flag in flags:
            if player.rect.colliderect(flag.rect):
                main_puntaje(player.score)  # le pasamos el puntaje
                return  # salir del juego

        #todo el fondo celeste
        screen.fill(color_fondo)

        #agrega todos los sprites y se acomodan
        for sprite_list in [solids, grasses, coins, enemies, plants, clouds , flags]:
            for sprite in sprite_list:
                screen.blit(sprite.image, camera.apply(sprite.rect))
        screen.blit(player.image, camera.apply(player.rect))

        # el efecto de las monedas
        for effect in COIN_POP_EFFECTS[:]:
            if not effect.update():
                COIN_POP_EFFECTS.remove(effect)
            else:
                screen.blit(effect.image, camera.apply(effect.rect))

        #muestra la puntuacion de las monedas
        score_txt = font.render(f"Monedas: {player.score}", True, (255, 255, 255))
        screen.blit(score_txt, (20, 20))

        # se actualiza la pantalla
        pygame.display.flip()
    #se cierra pygame y el programa
    pygame.quit()
    sys.exit()
#se ejecuta main, primero el menu y despues el juego
if __name__ == "__main__":
    main_menu()
    main()
