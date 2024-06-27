import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((102, 102, 51))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class WaterPlatform(Platform):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill((0, 0, 200))

class LavaPlatform(Platform):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill((200, 0, 0))

class AcidPlatform(Platform):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill((0, 200, 0))

class MovingPlatform(Platform):
    def __init__(self, x, y, width, height, move_x, move_y, range_x, range_y, speed):
        super().__init__(x, y, width, height)
        self.start_x = x
        self.start_y = y
        self.move_x = move_x
        self.move_y = move_y
        self.range_x = range_x
        self.range_y = range_y
        self.speed = speed
        self.direction_x = 1 if move_x else 0
        self.direction_y = 1 if move_y else 0
        self.previous_x = x
        self.previous_y = y

    def update(self):
        self.previous_x = self.rect.x
        self.previous_y = self.rect.y

        if self.move_x:
            self.rect.x += self.speed * self.direction_x
            if self.rect.x > self.start_x + self.range_x or self.rect.x < self.start_x:
                self.direction_x *= -1

        if self.move_y:
            self.rect.y += self.speed * self.direction_y
            if self.rect.y > self.start_y + self.range_y or self.rect.y < self.start_y:
                self.direction_y *= -1

    def get_movement(self):
        return self.rect.x - self.previous_x, self.rect.y - self.previous_y

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)