import pygame
from entities import load_img, TILE

FIREBALLS = []  # lista global de bolas activas

class FireFlower(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_img("assets/Items/fire_flower.png")
        self.rect = self.image.get_rect(center=(pos[0] + TILE // 2, pos[1] + TILE // 2))

    def give_power(self, player):
        player.has_fire = True  # le damos la habilidad al jugador


class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, solids, enemies):
        super().__init__()
        self.image = load_img("assets/Items/fireball.png", TILE // 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = 8 * direction  # dirección (izquierda o derecha)
        self.vy = -5
        self.gravity = 0.5
        self.solids = solids
        self.enemies = enemies
        self.alive = True

    def update(self):
        # movimiento
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.vy += self.gravity

        # rebote contra el suelo
        for tile in self.solids:
            if self.rect.colliderect(tile.rect):
                if self.vy > 0:  # cayendo
                    self.rect.bottom = tile.rect.top
                    self.vy = -8  # rebota
                else:
                    self.rect.top = tile.rect.bottom
                    self.vy = 0

        # colisión con enemigos
        for enemy in self.enemies.copy():
            if self.rect.colliderect(enemy.rect):
                self.enemies.remove(enemy)
                self.alive = False
                break

        # eliminar si se va de pantalla
        if self.rect.top > 2000 or self.rect.right < 0 or self.rect.left > 2000:
            self.alive = False

        return self.alive