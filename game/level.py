import pygame

from .character import Firegirl, Waterboy
from .door import Door


class LevelBase:
    def __init__(self, game, waterboy_pos, firegirl_pos):
        self.game = game
        self.timer_start = pygame.time.get_ticks()
        self.timer_font = pygame.font.Font(None, 36)
        self.timer_position = (400, 50)

        self.waterboy_start_pos = waterboy_pos
        self.waterboy = Waterboy(waterboy_pos[0],waterboy_pos[1],game.textures["WATERBOY"],self.game.sounds["MALE_JUMP"],self.game.sounds["MALE_DEATH"])
        self.firegirl_start_pos = firegirl_pos
        self.firegirl = Firegirl(firegirl_pos[0],firegirl_pos[1],game.textures["FIREGIRL"],self.game.sounds["FEMALE_JUMP"],self.game.sounds["FEMALE_DEATH"])
        self.waterDoor = Door
        self.lavaDoor = Door
        self.platforms = []
        self.crystals = []
        self.game_over = False
        self.background = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
        self.firegirl.handle_event(event)
        self.waterboy.handle_event(event)

    def update(self):
        if not self.game_over:
            self.firegirl.update(self.platforms, self.crystals, self)
            self.waterboy.update(self.platforms, self.crystals, self)
            self.check_level_completion()
            for p in self.platforms:
                p.update()

            self.timer_current = pygame.time.get_ticks()

    def draw(self, screen):
        if not self.game_over:
            if self.background:
                screen.blit(self.background, (0, 0))
            else:
                screen.fill((153, 153, 102))
            self.waterDoor.draw(screen)
            self.lavaDoor.draw(screen) 
            for crystal in self.crystals:
                crystal.draw(screen)
            self.firegirl.draw(screen)
            self.waterboy.draw(screen)
            for platform in self.platforms:
                platform.draw(screen)

            timer_text = f"{int((self.timer_current - self.timer_start) / 1000/60):02d}:{int((self.timer_current - self.timer_start) / 1000):02d}"
            timer_surface = self.timer_font.render(timer_text, True, (255, 255, 255))
            timer_rect = timer_surface.get_rect(center=self.timer_position)
            screen.blit(timer_surface, timer_rect)
            

    def game_over_screen(self):
        self.game_over = True
        self.game.game_over_menu.active = True 

    def game_won_screen(self):
        self.game_over = True
        self.game.game_won_menu.active = True 

    def reset_level(self):
        self.game.game_over_menu.active = False
        self.game.game_won_menu.active = False
        self.game_over = False
        self.crystals = self.__class__(self.game).crystals
        self.waterboy.hitbox.topleft = self.waterboy_start_pos
        self.waterboy.restart()
        self.firegirl.hitbox.topleft = self.firegirl_start_pos
        self.firegirl.restart()
        self.timer_start = pygame.time.get_ticks()

    def check_level_completion(self):
        if not self.crystals and self.firegirl.hitbox.colliderect(self.lavaDoor.rect) and self.waterboy.hitbox.colliderect(self.waterDoor.rect):
            self.game.completed_levels.append(self.game.current_level)
            score = 360-int((self.timer_current - self.timer_start)/1000)
            self.game.score = score
            self.game.update_highscore(self.game.current_level,score)
            self.game.save_game()
            self.game_won_screen()
