import pygame  
import os


TILE = 48  # Resolución de cada entidad
COIN_POP_EFFECTS = []  # Efectos de monedas


def load_img(path, scale=TILE): # Carga una imagen con manejo de errores
    full_path = os.path.join(os.path.dirname(__file__), path)
   
    if not os.path.isfile(full_path):
        print(f" No se encontró el archivo: {full_path}")
        # Crear una imagen X para que no tire error
        img = pygame.Surface((scale, scale), pygame.SRCALPHA)
        img.fill((255, 0, 0, 128))  # imagen de Rojo semitransparente
        return img
   
    try:
        img = pygame.image.load(full_path).convert_alpha()
        img = pygame.transform.scale(img, (scale, scale))
        return img
    except pygame.error as e:
        print(f"ERROR en cargar imagen: {full_path} - {e}")
       
        img = pygame.Surface((scale, scale), pygame.SRCALPHA)
        img.fill((255, 0, 0, 128))
        return img


class Player(pygame.sprite.Sprite):
   
    def __init__(self, pos, solids, coins, enemies, plants, clouds, grasses, flags):
        super().__init__()
       
        # Sistema de vidas
        self.total_lives = 3
        self.current_hits = 1
       
        # Sistema de poder de fuego
        self.has_fire_power = False
        self.fireballs = []
        self.fire_shots_remaining = 0
        self.fire_cooldown = 0
        self.fire_cooldown_max = 60 
       
        # Sprites y animaciones del personaje
        self.images = {
            "idle": [load_img("assets/player/idle.png")],
            "walk": [load_img("assets/player/walk1.png"), load_img("assets/player/walk2.png")],
            "jump": [load_img("assets/player/jump.png")]
        }
        self.anim_state = "idle"
        self.anim_frame = 0
        self.image = self.images["idle"][0]
       
        # Nueva variable para controlar la dirección
        self.facing_right = True
       
        # Física y posicion
        self.rect = self.image.get_rect(topleft=pos)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
       
        # Interacciones con objetos
        self.solids = solids
        self.grasses = grasses
        self.coins = coins
        self.enemies = enemies
        self.plants = plants
        self.clouds = clouds
        self.flags = flags
       
        # Estado del jugador
        self.score = 0
        self.alive = True
        self.level_completed = False
       
        # Sistema de invencibilidad temporal
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 120
       
    def update(self, keys):
        SPEED = 5
        GRAVITY = 0.5
        JUMP_VEL = -15.5
       
        # Actualizar invulnerabilidad
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
       
        # Actualizar cooldown de disparo
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1
       
        # Controles de movimiento
        self.vx = ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) -
                  (keys[pygame.K_LEFT] or keys[pygame.K_a])) * SPEED
       
        # Actualizar dirección del personaje
        if self.vx > 0:
            self.facing_right = True
        elif self.vx < 0:
            self.facing_right = False
       
        # Disparo de bolas de fuego (Ctrl o X)
        if (keys[pygame.K_LCTRL] or keys[pygame.K_r]) and self.has_fire_power:
            if self.fire_cooldown == 0: 
                self.shoot_fireball()
                self.fire_cooldown = self.fire_cooldown_max
           
        want_jump = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
       
        # Salto
        if want_jump and self.on_ground:
            self.vy = JUMP_VEL
            self.on_ground = False
       
        # Estados de animación
        if not self.on_ground:
            self.anim_state = "jump"
        elif self.vx != 0:
            self.anim_state = "walk"
        else:
            self.anim_state = "idle"
       
        # Aplicar gravedad
        self.vy += GRAVITY
        if self.vy > 20:
            self.vy = 20
       
        # Movimiento y colisiones
        self.move_and_collide(self.vx, self.vy)
       
        # Muerte por caída
        if self.rect.top > 2000:
            self.alive = False
       
        # Actualizar bolas de fuego
        for fireball in self.fireballs[:]:
            fireball.update()
            if not fireball.alive:
                self.fireballs.remove(fireball)
           
        self.animate()
   
    def move_and_collide(self, dx, dy):
        JUMP_VEL = -15.5
       
        # Movimiento horizontal
        self.rect.x += dx
        tiles = self.solids + self.grasses
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if dx > 0:
                    self.rect.right = tile.rect.left
                elif dx < 0:
                    self.rect.left = tile.rect.right
       
        # Movimiento vertical
        self.rect.y += dy
        self.on_ground = False
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
       
        # Colision con monedas
        for coin in self.coins.copy():
            if self.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.score += 1
       
        # Colisión con enemigos
        if not self.invulnerable:
            for enemy in self.enemies.copy():
                if self.rect.colliderect(enemy.rect):
                    player_bottom = self.rect.bottom
                    enemy_top = enemy.rect.top
                   
                    if self.vy > 0 and player_bottom - self.vy <= enemy_top + 10:
                        self.enemies.remove(enemy)
                        self.vy = JUMP_VEL * 0.7
                    else:
                        self.take_hit()


        # Colisión con banderas
        for flag in self.flags:
            if self.rect.colliderect(flag.rect):
                self.level_completed = True
   
    def take_hit(self):
        if self.current_hits > 1:
            self.current_hits = 1
            self.activate_invulnerability()
        else:
            self.alive = False


   
    def activate_invulnerability(self):
        self.invulnerable = True
        self.invulnerable_timer = self.invulnerable_duration
        self.rect.y -= 30
        self.vy = -8
   
    def give_powerup(self):
        if self.current_hits < 2:
            self.current_hits = 2
   
    def give_fire_power(self):
        """Otorga el poder de fuego al jugador"""
        self.has_fire_power = True
        self.fire_shots_remaining = 3  

 
        print("¡Poder de fuego obtenido!")
   
    def shoot_fireball(self):
        """Dispara una bola de fuego en la dirección que mira el jugador"""
        # Verificar si aún tiene disparos disponibles
        if self.fire_shots_remaining <= 0:
            return
        
        direction = 1 if self.facing_right else -1
        fireball = Fireball(self.rect.centerx, self.rect.centery, direction,
                           self.solids, self.grasses, self.enemies)
        self.fireballs.append(fireball)
        
        # Reducir disparos disponibles
        self.fire_shots_remaining -= 1
        print(f"Disparos restantes: {self.fire_shots_remaining}")
        
        # Si se acabaron los disparos, remover el poder
        if self.fire_shots_remaining <= 0:
            self.has_fire_power = False
            print("¡Poder de fuego agotado!")
    def animate(self):
        frames = self.images[self.anim_state]
        self.anim_frame += 0.15
        if self.anim_frame >= len(frames):
            self.anim_frame = 0
       
        # Obtener la imagen base
        base_image = frames[int(self.anim_frame)]
       
        # Voltear la imagen si mira a la izquierda
        if not self.facing_right:
            base_image = pygame.transform.flip(base_image, True, False)
       
        # Efecto de parpadeo durante invulnerabilidad
        if self.invulnerable and self.invulnerable_timer % 10 < 5:
            temp_image = base_image.copy()
            temp_image.set_alpha(128)
            self.image = temp_image
        else:
            self.image = base_image


class Tile(pygame.sprite.Sprite):# Bloque solido basico
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/tiles/grassCenter.png")
        self.rect = self.image.get_rect(topleft=pos)


class Grass(pygame.sprite.Sprite): #Bloque solido de pasto
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/tiles/grassMid.png")
        self.rect = self.image.get_rect(topleft=pos)


class TileLevel2(pygame.sprite.Sprite):#bloque solido para el nivel 2
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/Tiles/piedra.png")
        self.rect = self.image.get_rect(topleft=pos)


class GrassLevel2(pygame.sprite.Sprite):# vendria siendo como el pasto pero en el nivel 2
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/Tiles/piedra2.png")
        self.rect = self.image.get_rect(topleft=pos)


class Flag(pygame.sprite.Sprite):# bandera donde finaliza el nivel
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/Items/flagBlue.png")
        self.rect = self.image.get_rect(topleft=pos)


class LuckyBlock(pygame.sprite.Sprite): #luckyblock que suelta monedas si le pegas de abajo
    def __init__(self, pos):
        super().__init__()
        self.full_img = load_img("assets/tiles/boxItem.png")
        self.empty_img = load_img("assets/tiles/boxItem_disabled.png")
        self.image = self.full_img
        self.rect = self.image.get_rect(topleft=pos)
        self.used = False
   
    def hit(self, player):# se activa cuando el jugador le pega de abajo
       
        if self.used:
            return
        self.used = True
        self.image = self.empty_img
        player.score += 1
        COIN_POP_EFFECTS.append(CoinPopEffect(self.rect.centerx, self.rect.top - 4))


class HeartPowerUp(pygame.sprite.Sprite):# power - up que permite al personaje principal aguantar dos hits de enemigos
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/items/Broco3.png", TILE)
        self.rect = self.image.get_rect(center=(pos[0] + TILE // 2, pos[1] + TILE // 2))
   
    def apply(self, player): # aplica power - up al personaje
        player.give_powerup()


class Coin(pygame.sprite.Sprite): # moneda coleccionable por el personaje
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/items/zanahoria.png", TILE//2)
        self.rect = self.image.get_rect(center=(pos[0]+TILE//2, pos[1]+TILE//2))


class CoinPopEffect(pygame.sprite.Sprite): # effecto visual de la moneda cuando sale del luckyblock
    def __init__(self, x, y):
        super().__init__()
        self.image = load_img("assets/items/zanahoria.png", TILE//2)
        self.rect = self.image.get_rect(center=(x, y))
        self.vy = -6
        self.life = 22
   
    def update(self): # actualiza movimiento de moneda
        self.rect.y += self.vy
        self.vy += 0.5
        self.life -= 1
        return self.life > 0


class Plant(pygame.sprite.Sprite): # decoracion de planta
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/items/plant.png")
        self.rect = self.image.get_rect(center=(pos[0]+TILE//2, pos[1]+TILE//2))


class cloud(pygame.sprite.Sprite):#Decoración de nube
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/items/cloud1.png")
        self.rect = self.image.get_rect(center=(pos[0]+TILE//2, pos[1]+TILE//2))


class cloud_level2(pygame.sprite.Sprite): # decoracion de nube nivel 2
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/items/nube_violeta.png")
        self.rect = self.image.get_rect(center=(pos[0]+TILE//2, pos[1]+TILE//2))


class Enemy(pygame.sprite.Sprite):
    #Enemigo básico que se mueve horizontalmente.
    # si idle salta encima del mismo este muere
   
    def __init__(self, pos, solids, grasses, enemies_group=None, scale_factor=1.3):
        super().__init__()


        #  Cargar imágenes (load_img devuelve por defecto tamaño TILE)
        raw_imgs = [load_img(f"assets/enemies/{i}.png") for i in range(1, 4)] # nombre de imagen 1 - 2 - 3
        # Escaladas para dibujado (visual)
        self.images_right = [
            pygame.transform.scale(img, (int(img.get_width()*scale_factor), int(img.get_height()*scale_factor)))
            for img in raw_imgs
        ]
        self.images_left = [pygame.transform.flip(img, True, False) for img in self.images_right]


        # Hitbox de colisión Fija en tamaño TILE
        # pos viene como topleft de la celda  usamos esa posicion para la hitbox
        self.collision_rect = pygame.Rect(pos[0], pos[1], TILE, TILE)


        # Rect / image para dibujado
        # Alineamos la imagen escalada de modo que su midbottom coincida con la base de la hitbox
        self.image = self.images_right[0]
        self.rect = self.image.get_rect(midbottom=self.collision_rect.midbottom)


        # Movimiento / grupos
        self.vx = -3
        self.solids = solids
        self.grasses = grasses
        self.enemies_group = enemies_group


        # Animación
        self.anim_frame = 0.0
        self.anim_forward = True


    def update(self):
        # Actualiza movimiento y animación del enemigo.
       
        # Calculamos la posicion tentativa (en coordenadas de la hitbox)
        attempted_x = self.collision_rect.x + self.vx


        # ground_check basado en la hitbox (TILE)   asi no depende del tamaño visual
        ground_check = pygame.Rect(
            attempted_x + TILE // 2,       # mirar justo delante (centro de la celda adelantada)
            self.collision_rect.bottom,    # justo debajo de la hitbox
            1,
            6                               # poca profundidad; suficiente para detectar piso
        )


        has_ground = False
        for tile in self.solids + self.grasses:
            if ground_check.colliderect(tile.rect):
                has_ground = True
                break


        # Si no hay suelo  gira (no nos movemos hacia adelante)
        if not has_ground:
            self.vx *= -1
            attempted_x = self.collision_rect.x  # cancelar el intento de avance
        # Si hay suelo attempted_x mantiene el avance


        # Comprobacion de colision lateral contra bloques
        new_hitbox = self.collision_rect.copy()
        new_hitbox.x = attempted_x


        collided = False
        for tile in self.solids + self.grasses:
            if new_hitbox.colliderect(tile.rect):
                collided = True
                break


        # Colisión con otros enemigos (usar su collision_rect si existe)
        if self.enemies_group:
            for other in self.enemies_group:
                if other is self:
                    continue
                other_hit = getattr(other, "collision_rect", other.rect)
                if new_hitbox.colliderect(other_hit):
                    collided = True
                    break


        # Si colisiono giramos y no aplicamos movimiento; sino, aplicamos movimiento
        if collided:
            self.vx *= -1
        else:
            # Aplicar movimiento a la hitbox
            self.collision_rect.x = attempted_x


        #  Ajuste visual: bajar un poco la imagen para que parezca tocar el suelo
        self.rect = self.image.get_rect(midbottom=(self.collision_rect.midbottom[0],
                                           self.collision_rect.midbottom[1] + 11))


        # Animación suave
        if self.anim_forward:
            self.anim_frame += 0.1
            if self.anim_frame >= len(self.images_right) - 1:
                self.anim_forward = False
        else:
            self.anim_frame -= 0.1
            if self.anim_frame <= 0:
                self.anim_forward = True


        # Seleccionar sprite segun direccion
        if self.vx > 0:
            self.image = self.images_right[int(self.anim_frame)]
        else:
            self.image = self.images_left[int(self.anim_frame)]


class VerticalEnemy(pygame.sprite.Sprite):# enemigo con movimiento vertical
    def __init__(self, pos, min_y, max_y, speed=3): # speed=3 (igual al horizontal)
        super().__init__()
        self.image = load_img("assets/enemies/Papaenem.png")
        self.rect = self.image.get_rect(topleft=pos)
        self.vy = speed  # Ahora speed=3
        self.min_y = min_y
        self.max_y = max_y
   
    def update(self):# actualiza el movimiento vertical dl enemigo
        self.rect.y += self.vy
        if self.rect.top <= self.min_y or self.rect.bottom >= self.max_y:
            self.vy *= -1


class TuboArriba(pygame.sprite.Sprite):#parte de arriba del tubo
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/items/tubos/tubo1.png")
        self.rect = self.image.get_rect(topleft=pos)


class TuboAbajo(pygame.sprite.Sprite):#parte de abajo del tubo
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/items/tubos/tubo2.png")
        self.rect = self.image.get_rect(topleft=pos)


class FirePowerUp(pygame.sprite.Sprite):
    """Power-up que otorga el poder de disparar bolas de fuego"""
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/items/Morron.png", TILE)
        self.rect = self.image.get_rect(center=(pos[0] + TILE // 2, pos[1] + TILE // 2))

    def apply(self, player):
        """Aplica el poder de fuego al jugador"""
        player.give_fire_power()



class Fireball(pygame.sprite.Sprite):


    def __init__(self, x, y, direction, solids, grasses, enemies):
        super().__init__()
        self.image = load_img("assets/items/Jalapeño.png", TILE // 2)
        self.rect = self.image.get_rect(center=(x, y))
       
        # Física
        self.vx = 8 * direction  # Velocidad horizontal
        self.vy = -3  # Velocidad inicial hacia arriba
        self.gravity = 0.3
        self.direction = direction
       
        # Referencias
        self.solids = solids
        self.grasses = grasses
        self.enemies = enemies
       
        # Estado
        self.alive = True
        self.bounces = 0
        self.max_bounces = 3
       
        # Animación de rotación
        self.rotation = 0
   
    def update(self):
        """Actualiza movimiento, colisiones y animación de la bola de fuego"""
        if not self.alive:
            return
       
        # Aplicar gravedad
        self.vy += self.gravity
       
        # Movimiento horizontal
        self.rect.x += self.vx
       
        # Movimiento vertical
        self.rect.y += self.vy
       
        # Rotación visual
        self.rotation += 15 * self.direction
        self.image = pygame.transform.rotate(
            load_img("assets/items/Jalapeño.png", TILE // 2),
            self.rotation
        )
       
        # Colisión con bloques (rebote)
        tiles = self.solids + self.grasses
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                # Rebote en el suelo
                if self.vy > 0:
                    self.rect.bottom = tile.rect.top
                    self.vy = -6  # Rebote
                    self.bounces += 1
                    if self.bounces >= self.max_bounces:
                        self.alive = False
                        return
                # Choque con pared lateral
                elif self.vx > 0:
                    self.rect.right = tile.rect.left
                    self.alive = False
                    return
                elif self.vx < 0:
                    self.rect.left = tile.rect.right
                    self.alive = False
                    return
       
        # Colisión con enemigos
        for enemy in self.enemies[:]:
            if self.rect.colliderect(enemy.rect):
                self.enemies.remove(enemy)
                self.alive = False
                return