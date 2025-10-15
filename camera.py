import pygame
WIDTH, HEIGHT = 960, 540 #dimension de la camara


class Camera:
    def __init__(self):
        self.offset = pygame.Vector2()#cuanto se movio la camara, en funcion a un vector
        self.max_y = 0#limite macimo vertical


    def apply(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)
    #la camara sigue al jugador
    def update(self, target):
        self.offset.x = target.rect.centerx - WIDTH // 2
        if self.offset.x < 0:
            self.offset.x = 0





