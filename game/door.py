import pygame


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height,image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class WaterDoor(Door):
    def __init__(self, x, y, width, height,image):
        super().__init__(x, y, width, height,image)

class LavaDoor(Door):
    def __init__(self, x, y, width, height,image):
        super().__init__(x, y, width, height,image)
