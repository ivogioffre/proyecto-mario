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

        #centra la camara vertical
        desired_y = target.rect.centery - HEIGHT // 2
        if desired_y < self.max_y:
            self.max_y = desired_y
        self.offset.y = self.max_y
        if self.offset.y < 0:
            self.offset.y = 0
