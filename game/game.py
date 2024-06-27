import os

import pygame

from levels.level1 import Level1
from levels.level2 import Level2
from levels.level3 import Level3

from .menu import (GameOverMenu, GameWonMenu, LevelSelectMenu, MainMenu,
                   PauseMenu)


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.sfx_on = True
        self.music_on = True
        
        self.current_level = 0
        self.completed_levels = []
        self.score = 0
        self.highscores = {}

        self.font = load_fonts()
        self.show_loading_screen()
        self.textures = load_textures()
        self.sounds = load_sounds()
        self.music = load_music()
        self.load_save_file()


        self.levels = [Level1(self),Level2(self),Level3(self)]
        self.menu = MainMenu(self)
        self.level_select_menu = LevelSelectMenu(self)
        self.game_over_menu = GameOverMenu(self)
        self.game_won_menu = GameWonMenu(self)
        self.pause_menu = PauseMenu(self)

    def run(self):
        self.music["BACKGROUND"].play(-1)
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.menu.active:
                self.menu.handle_event(event)
            elif self.level_select_menu.active:
                self.level_select_menu.handle_event(event)
            elif self.game_over_menu.active:
                self.game_over_menu.handle_event(event)
            elif self.game_won_menu.active:
                self.game_won_menu.handle_event(event)
            elif self.pause_menu.active:
                self.pause_menu.handle_event(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_menu.active = True
            else:
                self.levels[self.current_level].handle_event(event)

    def update(self):
        if self.menu.active:
            self.menu.update()
        elif self.level_select_menu.active:
            self.level_select_menu.update()
        elif self.game_over_menu.active:
            self.game_over_menu.update()
        elif self.pause_menu.active:
            self.pause_menu.update()
        elif self.game_won_menu.active:
            self.game_over_menu.update()
        else:
            self.levels[self.current_level].update()

    def draw(self):
        if self.menu.active:
            self.menu.draw(self.screen)
        elif self.level_select_menu.active:
            self.level_select_menu.draw(self.screen)
        elif self.game_over_menu.active:
            self.game_over_menu.draw(self.screen)
        elif self.pause_menu.active:
            self.pause_menu.draw(self.screen)
        elif self.game_won_menu.active:
            self.game_won_menu.draw(self.screen)
        else:
            self.levels[self.current_level].draw(self.screen)
        pygame.display.flip()

    def get_first_unfinished_level(self):
        for i, level in enumerate(self.levels):
            if i not in self.completed_levels:
                return i
        return 0
    
    def show_loading_screen(self):
        font = pygame.font.Font(None, 32)
        text = self.font.render("Ładowanie...", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.screen.fill((0, 0, 0))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def load_save_file(self):
        if os.path.exists('savegame.save'):
            with open('savegame.save', 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if lines:
                    self.completed_levels = list(map(int, lines[0].strip().split(',')))
                for line in lines[1:]:
                    level, score = map(int, line.strip().split(':'))
                    self.highscores[level] = score
        else:
            self.completed_levels = []
            self.highscores = {}

    def save_game(self):
        with open('savegame.save', 'w', encoding='utf-8') as f:
            f.write(','.join(map(str, self.completed_levels)) + '\n')
            for level, score in self.highscores.items():
                f.write(f"{level}:{score}\n")

    def game_over(self):
        self.game_over_menu.active = True

    def update_highscore(self, level, score):
        if level not in self.highscores:
            self.highscores[level] = score
        else:
            if score > self.highscores[level]:
                self.highscores[level] = score

    def quit(self):
        self.save_game()
        pygame.quit()

def load_fonts():
        file_path = os.path.join('assets', 'fonts', 'Roboto-Regular.ttf')
        return pygame.font.Font(file_path, 32)

def load_textures():
    textures = {}
    textures_path = os.path.join(os.getcwd(),'assets','textures')
    for dir in os.listdir(textures_path):
        textures[dir.upper()] = {}
        for file in os.listdir(os.path.join(textures_path,dir)):
            name, ext = os.path.splitext(file)
            if ext == '.png':
                img = pygame.image.load(os.path.join(textures_path,dir,file)).convert_alpha()
                if "walk" in name:
                    textures[dir.upper()][name.upper()+"_L"] = pygame.transform.flip(pygame.transform.scale(img, (125,125)), True, False)
                    textures[dir.upper()][name.upper()+"_R"] = pygame.transform.scale(img, (125,125))
                elif dir in ["waterboy","firegirl"]:
                    textures[dir.upper()][name.upper()] = pygame.transform.scale(img, (125,125))
                elif dir == "backgrounds":
                    textures[dir.upper()][name.upper()] = pygame.transform.scale(img, (800,600))
                else:
                    textures[dir.upper()][name.upper()] = img
    return textures

def load_sounds():
    sounds = {}
    sounds_path = os.path.join(os.getcwd(),'assets','sounds')
    for file in os.listdir(sounds_path):
        name, ext = os.path.splitext(file)
        if ext == '.ogg':
            sounds[name.upper()] = pygame.mixer.Sound(os.path.join(sounds_path,file))
    return sounds

def load_music():
    music = {}
    music_path = os.path.join(os.getcwd(),'assets','music')
    for file in os.listdir(music_path):
        name, ext = os.path.splitext(file)
        if ext == '.ogg':
            music[name.upper()] = pygame.mixer.Sound(os.path.join(music_path,file))
    return music