# entities.py 
import pygame
import os


TILE = 48  # Resolución de cada entidad
COIN_POP_EFFECTS = []  # Efectos de monedas


def load_img(path, scale=TILE):
    """Carga una imagen con manejo de errores y fallback."""
    full_path = os.path.join(os.path.dirname(__file__), path)
   
    if not os.path.isfile(full_path):
        print(f"[WARNING] No se encontró el archivo: {full_path}")
        # Crear placeholder para que no falle
        img = pygame.Surface((scale, scale), pygame.SRCALPHA)
        img.fill((255, 0, 0, 128))  # Rojo semitransparente
        return img
   
    try:
        img = pygame.image.load(full_path).convert_alpha()
        img = pygame.transform.scale(img, (scale, scale))
        return img
    except pygame.error as e:
        print(f"[ERROR] Error loading image: {full_path} - {e}")
        # Fallback
        img = pygame.Surface((scale, scale), pygame.SRCALPHA)
        img.fill((255, 0, 0, 128))
        return img


class Player(pygame.sprite.Sprite):
    """Jugador con sistema de vidas y hits mejorado."""
    def __init__(self, pos, solids, coins, enemies, plants, clouds, grasses, flags):
        super().__init__()
       
        # Sistema de vidas mejorado
        self.total_lives = 3      # Vidas totales (se manejan en main)
        self.current_hits = 1     # Hits que puede aguantar actualmente (1 o 2 con power-up)
       
        # Sprites y animaciones
        self.images = {
            "idle": [load_img("assets/player/idle.png")],
            "walk": [load_img("assets/player/walk1.png"), load_img("assets/player/walk2.png")],
            "jump": [load_img("assets/player/jump.png")]
        }
        self.anim_state = "idle"
        self.anim_frame = 0
        self.image = self.images["idle"][0]
       
        # Física y posición
        self.rect = self.image.get_rect(topleft=pos)
        self.vx = 0  # Velocidad X
        self.vy = 0  # Velocidad Y
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
        self.level_completed = False  # NUEVO: para detectar si completó el nivel
       
        # Sistema de invencibilidad temporal
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 120  # 2 segundos a 60 FPS
       
    def update(self, keys):
        """Actualiza el jugador con física y controles."""
        # Constantes de física
        SPEED = 5
        GRAVITY = 0.5
        JUMP_VEL = -15.5
       
        # Actualizar invulnerabilidad
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
       
        # Controles de movimiento
        self.vx = ((keys[pygame.K_RIGHT] or keys[pygame.K_d]) -
                  (keys[pygame.K_LEFT] or keys[pygame.K_a])) * SPEED
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
                if dy > 0:  # Cayendo
                    self.rect.bottom = tile.rect.top
                    self.on_ground = True
                    self.vy = 0
                elif dy < 0:  # Golpeando desde abajo
                    self.rect.top = tile.rect.bottom
                    self.vy = 0
                    if hasattr(tile, "hit"):
                        tile.hit(self)
       
        # Colisión con monedas
        for coin in self.coins.copy():
            if self.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.score += 1
       
        # CORREGIDO: Colisión con enemigos - mejor detección de salto
        if not self.invulnerable:
            for enemy in self.enemies.copy():
                if self.rect.colliderect(enemy.rect):
                    # CORREGIDO: Mejor detección de saltar encima del enemigo
                    player_bottom = self.rect.bottom
                    enemy_top = enemy.rect.top
                    
                    # Si el jugador está cayendo Y su parte inferior está cerca de la parte superior del enemigo
                    if self.vy > 0 and player_bottom - self.vy <= enemy_top + 10:
                        # Eliminar enemigo saltando encima
                        self.enemies.remove(enemy)
                        self.vy = JUMP_VEL * 0.7  # Rebote al eliminar enemigo
                        print("¡Enemigo eliminado!")
                    else:
                        # Recibir daño
                        self.take_hit()

        # CORREGIDO: Colisión con banderas
        for flag in self.flags:
            if self.rect.colliderect(flag.rect):
                self.level_completed = True  # Marcar nivel como completado
                print("¡Nivel completado!")
   
    def take_hit(self):
        """Sistema de hits: puede sobrevivir con power-up."""
        if self.current_hits > 1:
            # Tiene power-up: lo pierde pero sobrevive
            self.current_hits = 1
            self.activate_invulnerability()
            print("¡Perdiste el power-up!")
        else:
            # Sin power-up: muere
            self.alive = False
            print("¡Mario murió!")
   
    def activate_invulnerability(self):
        """Activa invulnerabilidad temporal tras recibir daño."""
        self.invulnerable = True
        self.invulnerable_timer = self.invulnerable_duration
        # Empuje hacia atrás y arriba
        self.rect.y -= 30
        self.vy = -8
   
    def give_powerup(self):
        """Otorga power-up al jugador."""
        if self.current_hits < 2:
            self.current_hits = 2
            print("¡Power-up obtenido! Ahora puedes aguantar 2 hits.")
   
    def animate(self):
        """Maneja las animaciones del jugador."""
        frames = self.images[self.anim_state]
        self.anim_frame += 0.15
        if self.anim_frame >= len(frames):
            self.anim_frame = 0
       
        # Efecto de parpadeo durante invulnerabilidad
        if self.invulnerable and self.invulnerable_timer % 10 < 5:
            temp_image = frames[int(self.anim_frame)].copy()
            temp_image.set_alpha(128)  # Semitransparente
            self.image = temp_image
        else:
            self.image = frames[int(self.anim_frame)]


class Tile(pygame.sprite.Sprite):
    """Bloque sólido básico."""
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/tiles/grassCenter.png")
        self.rect = self.image.get_rect(topleft=pos)


class Grass(pygame.sprite.Sprite):
    """Bloque de pasto."""
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/tiles/grassMid.png")
        self.rect = self.image.get_rect(topleft=pos)


class Flag(pygame.sprite.Sprite):
    """Bandera de meta del nivel."""
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/Items/flagBlue.png")
        self.rect = self.image.get_rect(topleft=pos)


class LuckyBlock(pygame.sprite.Sprite):
    """Bloque de pregunta que da monedas."""
    def __init__(self, pos):
        super().__init__()
        self.full_img = load_img("assets/tiles/boxItem.png")
        self.empty_img = load_img("assets/tiles/boxItem_disabled.png")
        self.image = self.full_img
        self.rect = self.image.get_rect(topleft=pos)
        self.used = False
   
    def hit(self, player):
        """Se activa cuando el jugador golpea el bloque."""
        if self.used:
            return
        self.used = True
        self.image = self.empty_img
        player.score += 1
        COIN_POP_EFFECTS.append(CoinPopEffect(self.rect.centerx, self.rect.top - 4))


class HeartPowerUp(pygame.sprite.Sprite):
    """Power-up que permite aguantar 2 hits."""
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/items/Broco3.webp", TILE)
        self.rect = self.image.get_rect(center=(pos[0] + TILE // 2, pos[1] + TILE // 2))
   
    def apply(self, player):
        """Aplica el power-up al jugador."""
        player.give_powerup()


class Coin(pygame.sprite.Sprite):
    """Moneda coleccionable."""
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/items/coinGold.png", TILE//2)
        self.rect = self.image.get_rect(center=(pos[0]+TILE//2, pos[1]+TILE//2))


class CoinPopEffect(pygame.sprite.Sprite):
    """Efecto visual cuando aparece una moneda del bloque."""
    def __init__(self, x, y):
        super().__init__()
        self.image = load_img("assets/items/coinGold.png", TILE//2)
        self.rect = self.image.get_rect(center=(x, y))
        self.vy = -6
        self.life = 22
   
    def update(self):
        """Actualiza el efecto de la moneda."""
        self.rect.y += self.vy
        self.vy += 0.5
        self.life -= 1
        return self.life > 0


class Plant(pygame.sprite.Sprite):
    """Decoración de planta."""
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/items/plant.png")
        self.rect = self.image.get_rect(center=(pos[0]+TILE//2, pos[1]+TILE//2))


class cloud(pygame.sprite.Sprite):
    """Decoración de nube."""
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/items/cloud1.png")
        self.rect = self.image.get_rect(center=(pos[0]+TILE//2, pos[1]+TILE//2))


class cloud_level2(pygame.sprite.Sprite):
    """Nube para nivel 2."""
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/items/nube_violeta.png")
        self.rect = self.image.get_rect(center=(pos[0]+TILE//2, pos[1]+TILE//2))


class Enemy(pygame.sprite.Sprite):
    """Enemigo básico que se mueve horizontalmente."""
    def __init__(self, pos, solids, grasses, enemies_group=None):
        super().__init__()
        # Cargar sprites de animación
        self.images_right = [load_img(f"assets/enemies/{i}.png") for i in range(1, 5)]
        self.images_left = [pygame.transform.flip(img, True, False) for img in self.images_right]
       
        self.image = self.images_right[0]
        self.rect = self.image.get_rect(topleft=pos)
       
        # Movimiento
        self.vx = -3  # Velocidad reducida para mejor jugabilidad
        self.solids = solids
        self.grasses = grasses
        self.enemies_group = enemies_group
       
        # Animación
        self.anim_frame = 0
        self.anim_forward = True
   
    def update(self):
        """Actualiza movimiento y animación del enemigo."""
        # Verificar si hay suelo adelante
        next_x = self.rect.x + self.vx
        ground_check = pygame.Rect(
            next_x + (self.rect.width // 2),
            self.rect.bottom,
            1,
            48
        )
       
        has_ground = False
        for tile in self.solids + self.grasses:
            if ground_check.colliderect(tile.rect):
                has_ground = True
                break
       
        # Cambiar dirección si no hay suelo adelante
        if not has_ground:
            self.vx *= -1
        else:
            self.rect.x += self.vx
       
        # Animación suave
        if self.anim_forward:
            self.anim_frame += 0.1
            if self.anim_frame >= len(self.images_right) - 1:
                self.anim_forward = False
        else:
            self.anim_frame -= 0.1
            if self.anim_frame <= 0:
                self.anim_forward = True
       
        # Seleccionar sprite según dirección
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
    """Enemigo que se mueve verticalmente entre límites."""
    def __init__(self, pos, min_y, max_y, speed=3):  # CORREGIDO: speed=3 (igual al horizontal)
        super().__init__()
        self.image = load_img("assets/enemies/Dp.png")
        self.rect = self.image.get_rect(topleft=pos)
        self.vy = speed  # CORREGIDO: Ahora speed=3
        self.min_y = min_y
        self.max_y = max_y
   
    def update(self):
        """Actualiza movimiento vertical."""
        self.rect.y += self.vy
        if self.rect.top <= self.min_y or self.rect.bottom >= self.max_y:
            self.vy *= -1