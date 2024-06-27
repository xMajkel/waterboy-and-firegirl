import time

import pygame

from .crystal import BLUE, RED
from .platform import AcidPlatform, LavaPlatform, WaterPlatform


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites, jump_sound=None, death_sound=None):
        super().__init__()
        self.sprites = sprites
        self.jump_sound = jump_sound
        self.death_sound = death_sound
        self.image = self.sprites["IDLE_0"]
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(x, y, 30, 40)
        self.rect.midbottom = self.hitbox.midbottom
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.is_dying = False
        self.direction = "R"
        self.walk_anim_n = 0
        self.idle_anim_n = 0
        self.animation_delay = 3
        self.animation_timer = 0
        self.death_animation_started = False
        self.death_animation_timer = 0

    def restart(self):
        self.is_dying = False
        self.death_animation_started = False
        self.death_animation_timer = 0

    def handle_event(self, event):
        pass

    def update(self, platforms, crystals, level):
        keys = pygame.key.get_pressed()
        if self.is_dying:
            self.die(level)
            return

        self.vel_x = 0
        if self.controls['left'](keys):
            self.vel_x = -5
            self.direction = "L"
        if self.controls['right'](keys):
            self.vel_x = 5
            self.direction = "R"
        if self.controls['jump'](keys) and self.on_ground:
            self.vel_y = -15
            self.on_ground = False
            if level.game.sfx_on and self.jump_sound:
                self.jump_sound.play()

        self.vel_y += 1

        self.hitbox.x += self.vel_x
        self.collide(self.vel_x, 0, platforms, crystals, level)
        self.hitbox.y += self.vel_y
        self.on_ground = False
        self.collide(0, self.vel_y, platforms, crystals, level)

        if self.hitbox.left < 0:
            self.hitbox.left = 0
        if self.hitbox.right > 800:
            self.hitbox.right = 800
        if self.hitbox.top < 0:
            self.hitbox.top = 0
        if self.hitbox.bottom > 600:
            self.hitbox.bottom = 600
            self.vel_y = 0
            self.on_ground = True

        self.rect.midbottom = self.hitbox.midbottom
        self.rect.y += 17

        self.update_animation()

    def die(self, level):
        self.is_dying = True
        if level.game.sfx_on and self.death_sound:
            self.death_sound.play()
        current_time = pygame.time.get_ticks()
        if not self.death_animation_started:
            self.death_animation_started = True
            self.death_animation_timer = current_time
        else:
            elapsed_time = current_time - self.death_animation_timer
            frame_index = elapsed_time // (500//3)
            if frame_index < 3:
                self.image = self.sprites[f"DEATH_{frame_index}"]
            else:
                level.game_over_screen()

    def update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_delay:
            if self.vel_x != 0:
                self.walk_anim_n = (self.walk_anim_n + 1) % 7 
                self.image = self.sprites[f"WALK_{self.walk_anim_n+1}_{self.direction}"]
            else:
                self.idle_anim_n = (self.idle_anim_n + 1) % 5
                self.image = self.sprites[f"IDLE_{self.idle_anim_n+1}"]
            self.animation_timer = 0

    def collide(self, vel_x, vel_y, platforms, crystals, level):
        for platform in platforms:
            if self.hitbox.colliderect(platform.rect):
                if isinstance(platform, WaterPlatform):
                    if isinstance(self, Firegirl):
                        self.die(level)
                    elif isinstance(self, Waterboy):
                        continue
                if isinstance(platform, LavaPlatform):
                    if isinstance(self, Waterboy):
                        self.die(level)
                    elif isinstance(self, Firegirl):
                        continue
                if isinstance(platform, AcidPlatform):
                    self.die(level)

                if vel_x > 0:
                    self.hitbox.right = platform.rect.left
                if vel_x < 0:
                    self.hitbox.left = platform.rect.right
                if vel_y > 0:
                    self.hitbox.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                if vel_y < 0:
                    self.hitbox.top = platform.rect.bottom
                    self.vel_y = 0

        for crystal in crystals:
            if self.hitbox.colliderect(crystal.rect):
                if ((isinstance(self, Firegirl) and crystal.color == RED) or
                        (isinstance(self, Waterboy) and crystal.color == BLUE)):
                    crystals.remove(crystal)

    def draw(self, screen, debug=False):
        screen.blit(self.image, self.rect.topleft)
        if debug:
            pygame.draw.rect(screen, (0, 255, 0), self.hitbox, 2)
class Firegirl(Character):
    def __init__(self, x, y, sprites, jump_sound=None, death_sound=None):
        super().__init__(x, y, sprites, jump_sound, death_sound)
        self.controls = {
            'left': lambda keys: keys[pygame.K_LEFT],
            'right': lambda keys: keys[pygame.K_RIGHT],
            'jump': lambda keys: keys[pygame.K_UP]
        }

class Waterboy(Character):
    def __init__(self, x, y, sprites, jump_sound=None, death_sound=None):
        super().__init__(x, y, sprites, jump_sound, death_sound)
        self.controls = {
            'left': lambda keys: keys[pygame.K_a],
            'right': lambda keys: keys[pygame.K_d],
            'jump': lambda keys: keys[pygame.K_w]
        }
