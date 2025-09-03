import pygame

TILE = 48 #resolucion de cada entidad
COIN_POP_EFFECTS = [] # Efectos de monedas

#importamos las imagenes y la ponemos en escala (48x48)
def load_img(path, scale=TILE):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (scale, scale))

class Player(pygame.sprite.Sprite):#configurar sprite, colisiones y movimiento del jugador
    def __init__(self, pos, solids, coins, enemies, plants, clouds, grasses, flags):
        super().__init__()
        self.images = {
            "idle": [load_img("assets/player/idle.png")],
            "walk": [load_img("assets/player/walk1.png"), load_img("assets/player/walk2.png")],
            "jump": [load_img("assets/player/jump.png")]
        }
        #sprite para cada movimiento
        self.anim_state = "idle"
        self.anim_frame = 0
        self.image = self.images["idle"][0]
        #fisica y colisiones
        self.rect = self.image.get_rect(topleft=pos)
        self.vx = 0 #x jugador
        self.vy = 0 #y jugador
        self.on_ground = False #si el jugador esta en el suelo
        #interaccion con los objetos
        self.solids = solids
        self.grasses = grasses
        self.coins = coins
        self.enemies = enemies
        self.score = 0
        self.plants = plants
        self.clouds = clouds
        self.flags = flags
        self.alive = True
        
    def update(self, keys):
        # velocidad, gravedad y salto
        SPEED = 5
        GRAVITY = 0.5
        JUMP_VEL = -15.5
        
        #detecta las teclas que se presionan
        self.vx = ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])) * SPEED
        want_jump = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
        if want_jump and self.on_ground:
            self.vy = JUMP_VEL
            self.on_ground = False

        #cambia la animacion
        if not self.on_ground:
            self.anim_state = "jump"
        elif self.vx != 0:
            self.anim_state = "walk"
        else:
            self.anim_state = "idle"

        #se aplica la gravedad
        self.vy += GRAVITY
        if self.vy > 20: self.vy = 20

        self.move_and_collide(self.vx, self.vy)
        if self.rect.top > 2000: #si el jugador cae muy bajo muere
            self.alive = False
        self.animate()

    #detecta colisiones y evita que quede atrapado dentro de bloques
    def move_and_collide(self, dx, dy):
        JUMP_VEL = -15.5
        for axis in ["x", "y"]:
            if axis == "x":
                self.rect.x += dx
                tiles = self.solids + self.grasses
                for tile in tiles:
                    if self.rect.colliderect(tile.rect):
                        if dx > 0:
                            self.rect.right = tile.rect.left
                        elif dx < 0:
                            self.rect.left = tile.rect.right
            else:
                self.rect.y += dy
                self.on_ground = False
                tiles = self.solids + self.grasses
                for tile in tiles:
                    if self.rect.colliderect(tile.rect):
                        if dy > 0:
                            self.rect.bottom = tile.rect.top
                            self.on_ground = True
                            self.vy = 0
                        elif dy < 0:
                            self.rect.top = tile.rect.bottom
                            self.vy = 0
                            if hasattr(tile, "hit"):
                                tile.hit(self)

        #suma puntos si agarra una moneda
        for coin in self.coins.copy():
            if self.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.score += 1

        #si cae encima de un enemigo lo mata
        for enemy in self.enemies.copy():
            if self.rect.colliderect(enemy.rect):
                if self.vy > 0:
                    self.enemies.remove(enemy)
                    self.vy = JUMP_VEL * 0.7
                else:
                    self.alive = False
    #actualiza la animacion
    def animate(self):
        frames = self.images[self.anim_state]
        self.anim_frame += 0.15
        if self.anim_frame >= len(frames):
            self.anim_frame = 0
        self.image = frames[int(self.anim_frame)]

#armamos todas las entidades (bloques, enemigos monedas, etc.)
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

class Flag(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/Items/flagBlue.png")
        self.rect = self.image.get_rect(topleft=pos)

class LuckyBlock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.full_img = load_img("assets/tiles/boxItem.png")
        self.empty_img = load_img("assets/tiles/boxItem_disabled.png")
        self.image = self.full_img
        self.rect = self.image.get_rect(topleft=pos)
        self.used = False

    def hit(self, player):
        if self.used: return
        self.used = True
        self.image = self.empty_img
        player.score += 1
        COIN_POP_EFFECTS.append(CoinPopEffect(self.rect.centerx, self.rect.top - 4))

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/items/coinGold.png", TILE//2)
        self.rect = self.image.get_rect(center=(pos[0]+TILE//2, pos[1]+TILE//2))

class CoinPopEffect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_img("assets/items/coinGold.png", TILE//2)
        self.rect = self.image.get_rect(center=(x, y))
        self.vy = -6
        self.life = 22

    def update(self):
        self.rect.y += self.vy
        self.vy += 0.5
        self.life -= 1
        return self.life > 0

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
    def __init__(self, pos, solids, grasses, enemies_group=None):
        super().__init__()
        self.images_right = [load_img(f"assets/enemies/{i}.png") for i in range(1, 5)]  # Animación mirando derecha
        self.images_left = [pygame.transform.flip(img, True, False) for img in self.images_right]  # Animación mirando izquierda

        self.image = self.images_right[0]
        self.rect = self.image.get_rect(topleft=pos)

        self.vx = -2
        self.solids = solids
        self.grasses = grasses
        self.enemies_group = enemies_group

        self.anim_frame = 0
        self.anim_forward = True

    def update(self):
        self.rect.x += self.vx

        # Animación de ida y vuelta
        if self.anim_forward:
            self.anim_frame += 0.15
            if self.anim_frame >= len(self.images_right) - 1:
                self.anim_forward = False
        else:
            self.anim_frame -= 0.15
            if self.anim_frame <= 0:
                self.anim_forward = True

        # Seleccionar imágenes según dirección
        if self.vx > 0:
            self.image = self.images_right[int(self.anim_frame)]
        else:
            self.image = self.images_left[int(self.anim_frame)]

        # Colisiones con bloques
        for tile in self.solids + self.grasses:
            if self.rect.colliderect(tile.rect):
                self.vx *= -1
                break

        # Colisiones con otros enemigos
        if self.enemies_group:
            for other in self.enemies_group:
                if other != self and self.rect.colliderect(other.rect):
                    self.vx *= -1
                    break
class VerticalEnemy(pygame.sprite.Sprite):
    #si llega a los limite cambia de direccion
    def __init__(self, pos, min_y, max_y, speed=4):
        super().__init__()
        self.image = load_img("assets/enemies/Dp.png")
        self.rect = self.image.get_rect(topleft=pos)
        self.vy = speed
        self.min_y = min_y
        self.max_y = max_y
    def update(self):
        self.rect.y += self.vy
        if self.rect.top <= self.min_y or self.rect.bottom >= self.max_y:
            self.vy *= -1
