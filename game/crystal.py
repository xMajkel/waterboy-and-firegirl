import pygame

RED = "red"
BLUE = "blue"

class Crystal(pygame.sprite.Sprite):
    def __init__(self, x, y, color, type):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.color = type

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
