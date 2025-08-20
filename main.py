import pygame, sys, json, os

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 960, 540
FPS = 60
GRAVITY = 0.6
SPEED = 5
JUMP_VEL = -14
TILE = 48

LEVEL_MAP = [
    "X                                                                              ",
    "X                                                                              ",
    "X                                                                              ",
    "X                           MM                                                 ",
    "X                      G                                          M            ",
    "X                 L                                                            ",
    "X                GGG                    MMM                                    ",
    "X                                                            GG                ",
    "X      P   L                                                L               L  ",
    "XGGGGGGGGGGGGGGGGGGG         GGGGG    GGGGGGG            GGGGGG     GGGGGGGGGGG",
    "XXXXXXXXXXXXXXXXXXXX   GGG   XXXXX  E XXXXXXX   GGG   E  XXXXXX  E  XXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXX         XXXXX    XXXXXXX            XXXXXX     XXXXXXXXXXX",                   
]


# ---------------- UTIL ----------------
def load_img(path, scale=TILE):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (scale, scale))

def load_level():
    solids = []
    grasses = []
    coins = []
    enemies = []
    plants = []
    clouds = []
    player = None

    for j, row in enumerate(LEVEL_MAP):
        for i, ch in enumerate(row):
            x, y = i * TILE, j * TILE
            if ch == "X":
                solids.append(Tile((x, y)))
            elif ch == "G":
                grasses.append(Grass((x, y)))
            elif ch == "P":
                player = Player((x, y), solids, coins, enemies, plants,clouds,grasses)
            elif ch == "M":
                coins.append(Coin((x, y)))
            elif ch == "E":
                enemies.append(Enemy((x, y), solids, grasses))
            elif ch == "L":
                plants.append(Plant((x, y)))
            elif ch == "C":
                clouds.append(cloud((x, y)))

    return player, solids, coins, enemies, plants, clouds, grasses

# ---------------- ENTIDADES ----------------
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, solids, coins, enemies, plants,clouds,grasses):
        super().__init__()
        self.images = {
            "idle": [load_img("assets/player/idle.png")],
            "walk": [load_img("assets/player/walk1.png"),
                     load_img("assets/player/walk2.png")],
            "jump": [load_img("assets/player/jump.png")]
        }
        self.anim_state = "idle"
        self.anim_frame = 0
        self.image = self.images["idle"][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.solids = solids
        self.grasses = grasses 
        self.coins = coins
        self.enemies = enemies
        self.score = 0
        self.plants = plants
        self.alive = True
        self.clouds = clouds


    def update(self, keys):
        # Movimiento
        self.vx = ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])) * SPEED
        want_jump = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
        if want_jump and self.on_ground:
            self.vy = JUMP_VEL
            self.on_ground = False

        # Animación
        if not self.on_ground:
            self.anim_state = "jump"
        elif self.vx != 0:
            self.anim_state = "walk"
        else:
            self.anim_state = "idle"

        self.vy += GRAVITY
        if self.vy > 20: self.vy = 20

        self.move_and_collide(self.vx, self.vy)
        if self.rect.top > 2000:  
            self.alive = False

        self.animate()

    def move_and_collide(self, dx, dy):
        # Mover en X
        self.rect.x += dx
        for tile in self.solids + self.grasses:
            if self.rect.colliderect(tile.rect):
                if dx > 0:
                    self.rect.right = tile.rect.left
                elif dx < 0:
                    self.rect.left = tile.rect.right
        # Mover en Y
        self.rect.y += dy
        self.on_ground = False
        for tile in self.solids + self.grasses:
            if self.rect.colliderect(tile.rect):
                if dy > 0:
                    self.rect.bottom = tile.rect.top
                    self.on_ground = True
                    self.vy = 0
                elif dy < 0:
                    self.rect.top = tile.rect.bottom
                    self.vy = 0
        # Colisión con monedas
        for coin in self.coins.copy():
            if self.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.score += 1

        for plants in self.plants.copy():
            if self.rect.colliderect(plants.rect):
                pass

        for cloud in self.clouds.copy():
            if self.rect.colliderect(cloud.rect):
                pass


        # Colisión con enemigos
        for enemy in self.enemies.copy():
            if self.rect.colliderect(enemy.rect):
                if self.vy > 0:
                    self.enemies.remove(enemy)
                    self.vy = JUMP_VEL * 0.7
                else:
                    self.alive = False

    def animate(self):
        frames = self.images[self.anim_state]
        self.anim_frame += 0.15
        if self.anim_frame >= len(frames):
            self.anim_frame = 0
        self.image = frames[int(self.anim_frame)]

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/tiles/grassCenter.png")
        self.rect = self.image.get_rect(topleft=pos)

class Grass(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/tiles/grassMid.png")
        self.rect = self.image.get_rect(topleft=pos)

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/items/coinGold.png", TILE//2)
        self.rect = self.image.get_rect(center=(pos[0]+TILE//2, pos[1]+TILE//2))

class Plant(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/items/plant.png")
        self.rect = self.image.get_rect(center=(pos[0]+TILE//2, pos[1]+TILE//2))

class cloud(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/items/cloud1.png")
        self.rect = self.image.get_rect(center=(pos[0]+TILE//2, pos[1]+TILE//2))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, solids, grasses):
        super().__init__()
        self.image = load_img("assets/enemies/slimeWalk1.png")
        self.rect = self.image.get_rect(topleft=pos)
        self.vx = -2
        self.solids = solids
        self.grasses = grasses

    def update(self):
        self.rect.x += self.vx
        for tile in self.solids + self.grasses:
            if self.rect.colliderect(tile.rect):
                self.vx *= -1

# ---------------- CÁMARA ----------------
class Camera:
    def __init__(self):
        self.offset = pygame.Vector2()

    def apply(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)

    def update(self, target):
        self.offset.x = target.rect.centerx - WIDTH//2
        self.offset.y = target.rect.centery - HEIGHT//2
        if self.offset.x < 0: self.offset.x = 0
        if self.offset.y < 0: self.offset.y = 0
#---------------- MENU -------------------
def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menú Principal")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)

    bg = pygame.image.load("assets/universo.png").convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    while True:
        screen.blit(bg, (0, 0))

        title_text = font.render("Mario Bros con Pygame", True, (255, 255, 255))
        play_text = small_font.render("Presiona ENTER para jugar", True, (255, 255, 255))
        quit_text = small_font.render("Presiona ESC para salir", True, (255, 255, 255))

        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 100))
        screen.blit(play_text, (WIDTH//2 - play_text.get_width()//2, HEIGHT//2))
        screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # salir del menú y continuar al juego
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(FPS)

# ---------------- MAIN ----------------
def main():
    pygame.mixer.init() 
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Mario Bross con Pygame (versión rápida)")

    pygame.mixer.music.load("assets/musica/10 Shop.mp3")
    pygame.mixer.music.play(-1)  # -1 = loop infinito
    pygame.mixer.music.set_volume(0.5)  # volumen de 0.0 a 1.0

    player, solids, coins, enemies, plants ,clouds, grasses = load_level()
    camera = Camera()
    font = pygame.font.SysFont(None, 32)
    
    # --- Cargar fondo una sola vez ---
    fondo = pygame.image.load("assets/universo.png").convert()
    fondo = pygame.transform.scale(fondo, (WIDTH*3, HEIGHT*3))  # fondo más grande para mover

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
            player, solids, coins, enemies, plants ,clouds, grasses = load_level()

        # --- Fondo parallax ---
        bg_x = -camera.offset.x * 0.5
        bg_y = -camera.offset.y * 0.5
        screen.blit(fondo, (bg_x, bg_y))

        # --- Dibujar sprites ---
        for tile in solids:
            screen.blit(tile.image, camera.apply(tile.rect))
        for grass in grasses:
            screen.blit(grass.image, camera.apply(grass.rect))
        for coin in coins:
            screen.blit(coin.image, camera.apply(coin.rect))
        for enemy in enemies:
            screen.blit(enemy.image, camera.apply(enemy.rect))
        for plant in plants:
            screen.blit(plant.image, camera.apply(plant.rect))
        for cloud in clouds:
            screen.blit(cloud.image, camera.apply(cloud.rect))
        screen.blit(player.image, camera.apply(player.rect))

        # --- Puntaje ---
        score_txt = font.render(f"Monedas: {player.score}", True, (255, 255, 255))
        screen.blit(score_txt, (20, 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()
    main()
