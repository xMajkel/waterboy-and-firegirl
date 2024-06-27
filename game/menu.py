import os

import pygame


class MainMenu:
    def __init__(self, game):
        self.game = game
        self.active = True
        self.font = pygame.font.Font(os.path.join(os.getcwd(),"assets","fonts","Roboto-Bold.ttf"), 56)
        self.italic_font = pygame.font.Font(os.path.join(os.getcwd(),"assets","fonts","Roboto-BlackItalic.ttf"), 56)
        self.small_font = pygame.font.Font(os.path.join(os.getcwd(),"assets","fonts","Roboto-Bold.ttf"), 26)
        self.buttons = [
            {"text": "Kontynuuj", "action": self.continue_game, "rect": None,"position": None},
            {"text": "Wybierz poziom", "action": self.level_select, "rect": None,"position": None},
            {"text": "Wyjdź", "action": self.quit_game, "rect": None,"position": None},
            {"text": "Music: On", "action": self.toggle_music, "rect": None,"position": (700, 550)},
            {"text": "SFX: On", "action": self.toggle_sfx, "rect": None,"position": (700, 580)},
        ]

        self.menu_background = pygame.Surface((600, 300), pygame.SRCALPHA)
        self.menu_background.fill((0, 0, 0,128))
        self.menu_rect = self.menu_background.get_rect()
        self.menu_rect.topleft = (100, 150)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for button in self.buttons:
                if button["rect"].collidepoint(x, y):
                    button["action"](button)


    def continue_game(self, button):
        self.active = False
        self.game.current_level = self.game.get_first_unfinished_level()
        self.game.levels[self.game.current_level].reset_level()

    def level_select(self, button):
        self.active = False
        self.game.level_select_menu.active = True

    def quit_game(self, button):
        self.game.running = False

    def toggle_music(self, button):
        self.game.music_on = not self.game.music_on
        for track in self.game.music.keys():
            self.game.music[track].set_volume(1 if self.game.music_on else 0)
        button["text"] = "Music: On" if self.game.music_on else "Music: Off"

    def toggle_sfx(self, button):
        self.game.sfx_on = not self.game.sfx_on
        button["text"] = "SFX: On" if self.game.sfx_on else "SFX: Off"

    def draw(self, screen):
        screen.blit(self.game.textures["BACKGROUNDS"]["MENU"], (0, 0))
        screen.blit(self.menu_background, self.menu_rect.topleft)
        title = self.italic_font.render("Waterboy & Firegirl", True, (255, 255, 255))
        rect = title.get_rect(center=(400, 200))
        screen.blit(title, rect.topleft)

        mouse_pos = pygame.mouse.get_pos()

        for i, button in enumerate(self.buttons):
            if button["rect"] is None:
                if button["position"] is None:
                    rect = self.small_font.render(button["text"], True, (255, 255, 255)).get_rect(center=(400, 300 + i * 50))
                else:
                    rect = self.small_font.render(button["text"], True, (255, 255, 255)).get_rect(center=button["position"])
                button["rect"] = rect

            if button["rect"].collidepoint(mouse_pos):
                text = self.small_font.render(button["text"], True, (150, 150, 150))
            else:
                text = self.small_font.render(button["text"], True, (220, 220, 220))

            screen.blit(text, button["rect"].topleft)

        author_text = self.small_font.render("by Michał Adamski", True, (255, 255, 255))
        screen.blit(author_text, (10, 570))

    def update(self):
        pass


class LevelSelectMenu:
    def __init__(self, game):
        self.game = game
        self.active = False
        self.font = pygame.font.Font(os.path.join(os.getcwd(),"assets","fonts","Roboto-Bold.ttf"), 56)
        self.small_font = pygame.font.Font(os.path.join(os.getcwd(),"assets","fonts","Roboto-Bold.ttf"), 26)
        self.levels = self.game.levels
        self.current_selection = 0
        self.level_rects = []
        self.back_button_rect = None

        self.menu_background = pygame.Surface((600, 500), pygame.SRCALPHA)
        self.menu_background.fill((0, 0, 0,128))
        self.menu_rect = self.menu_background.get_rect()
        self.menu_rect.topleft = (100, 50)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.back_button_rect and self.back_button_rect.collidepoint(x, y):
                self.back_to_main_menu()
            for i, rect in enumerate(self.level_rects):
                if rect.collidepoint(x, y):
                    self.select_level(i)

    def select_level(self, level_index):
        self.game.current_level = level_index
        self.active = False
        self.game.menu.active = False
        self.levels[level_index].reset_level()

    def back_to_main_menu(self):
        self.active = False
        self.game.menu.active = True

    def draw(self, screen):
        screen.blit(self.game.textures["BACKGROUNDS"]["LEVELS"], (0, 0))
        screen.blit(self.menu_background, self.menu_rect.topleft)
        title = self.font.render("Wybierz poziom", True, (255, 255, 255))
        screen.blit(title, (200, 100))

        mouse_pos = pygame.mouse.get_pos()

        self.level_rects = []
        for i, level in enumerate(self.levels):
            rect = self.small_font.render(f"Poziom {i + 1} | Rekord: {self.game.highscores.get(i, 0)}", True, (220, 220, 220)).get_rect(center=(400, 250 + i * 50))
            self.level_rects.append(rect)

        for i, rect in enumerate(self.level_rects):
            text_color = (150, 150, 150) if rect.collidepoint(mouse_pos) else (220, 220, 220)
            text = self.small_font.render(f"Poziom {i + 1} | Rekord: {self.game.highscores.get(i, 0)}", True, text_color)
            screen.blit(text, rect.topleft)

        if not self.back_button_rect:
            self.back_button_rect = self.small_font.render("Powrót", True, (220, 220, 220)).get_rect(center=(400, 500))

        back_text_color = (150, 150, 150) if self.back_button_rect.collidepoint(mouse_pos) else (220, 220, 220)
        back_text = self.small_font.render("Powrót", True, back_text_color)
        screen.blit(back_text, self.back_button_rect.topleft)

    def update(self):
        pass

class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.active = False
        self.font = pygame.font.Font(os.path.join(os.getcwd(),"assets","fonts","Roboto-Bold.ttf"), 56)
        self.small_font = pygame.font.Font(os.path.join(os.getcwd(),"assets","fonts","Roboto-Bold.ttf"), 26)
        self.buttons = [
            {"text": "Wznów", "action": self.unpause, "rect": None},
            {"text": "Zagraj ponownie", "action": self.retry_game, "rect": None},
            {"text": "Powrót do menu", "action": self.back_to_main_menu, "rect": None}
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for button in self.buttons:
                if button["rect"].collidepoint(x, y):
                    button["action"]()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.unpause()

    def unpause(self):
        self.active = False

    def retry_game(self):
        self.active = False
        self.game.levels[self.game.current_level].reset_level()

    def back_to_main_menu(self):
        self.active = False
        self.game.menu.active = True

    def draw(self, screen):
        screen.fill((0, 0, 0))
        title = self.font.render("PAUZA", True, (255, 0, 204))
        rect = title.get_rect(center=(400, 150))
        screen.blit(title, rect.topleft)

        mouse_pos = pygame.mouse.get_pos()

        for i, button in enumerate(self.buttons):
            if button["rect"] is None:
                rect = self.small_font.render(button["text"], True, (220, 220, 220)).get_rect(center=(400, 250 + i * 50))
                button["rect"] = rect

            if button["rect"].collidepoint(mouse_pos):
                text = self.small_font.render(button["text"], True, (150, 150, 150))
            else:
                text = self.small_font.render(button["text"], True, (220, 220, 220))

            screen.blit(text, button["rect"].topleft)

    def update(self):
        pass
class GameOverMenu:
    def __init__(self, game):
        self.game = game
        self.active = False
        self.color = (255,255,255)
        self.message = "MENU"
        self.font = pygame.font.Font(os.path.join(os.getcwd(),"assets","fonts","Roboto-Bold.ttf"), 56)
        self.small_font = pygame.font.Font(os.path.join(os.getcwd(),"assets","fonts","Roboto-Bold.ttf"), 26)
        self.buttons = [
            {"text": "Zagraj ponownie", "action": self.retry_game, "rect": None},
            {"text": "Powrót do menu", "action": self.back_to_main_menu, "rect": None}
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for button in self.buttons:
                if button["rect"].collidepoint(x, y):
                    button["action"]()

    def retry_game(self):
        self.active = False
        self.game.levels[self.game.current_level].reset_level()

    def back_to_main_menu(self):
        self.active = False
        self.game.levels[self.game.current_level].game_over = True
        self.game.menu.active = True

    def draw(self, screen):
        screen.fill((0, 0, 0))
        title = self.font.render("GAME OVER", True, (255,0,0))
        rect = title.get_rect(center=(400, 150))
        screen.blit(title, rect.topleft)

        mouse_pos = pygame.mouse.get_pos()

        for i, button in enumerate(self.buttons):
            if button["rect"] is None:
                rect = self.small_font.render(button["text"], True, (220, 220, 220)).get_rect(center=(400, 250 + i * 50))
                button["rect"] = rect

            if button["rect"].collidepoint(mouse_pos):
                text = self.small_font.render(button["text"], True, (150, 150, 150))
            else:
                text = self.small_font.render(button["text"], True, (220, 220, 220))

            screen.blit(text, button["rect"].topleft)

    def update(self):
        pass
class GameWonMenu:
    def __init__(self, game):
        self.game = game
        self.active = False
        self.color = (255,255,255)
        self.message = "MENU"
        self.font = pygame.font.Font(os.path.join(os.getcwd(),"assets","fonts","Roboto-Bold.ttf"), 56)
        self.small_font = pygame.font.Font(os.path.join(os.getcwd(),"assets","fonts","Roboto-Bold.ttf"), 26)
        self.buttons = [
            {"text": "Kontynuuj", "action": self.continue_game, "rect": None},
            {"text": "Zagraj ponownie", "action": self.retry_game, "rect": None},
            {"text": "Powrót do menu", "action": self.back_to_main_menu, "rect": None}
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for button in self.buttons:
                if button["rect"].collidepoint(x, y):
                    button["action"]()

    def continue_game(self):
        self.active = False
        self.game.current_level = self.game.get_first_unfinished_level()
        self.game.levels[self.game.current_level].reset_level()

    def retry_game(self):
        self.active = False
        self.game.levels[self.game.current_level].reset_level()

    def back_to_main_menu(self):
        self.active = False
        self.game.levels[self.game.current_level].game_over = True
        self.game.menu.active = True

    def draw(self, screen):
        screen.fill((0, 0, 0))
        title = self.font.render("WYGRANA", True, (0,255,0))
        rect = title.get_rect(center=(400, 150))
        screen.blit(title, rect.topleft)
        
        highscore_text = self.game.score
        if self.game.highscores.get(self.game.current_level, "") != "":
            if self.game.highscores[self.game.current_level] > self.game.score:
                highscore_text = self.game.highscores[self.game.current_level]
        
        title = self.small_font.render(f"WYNIK: {self.game.score} | REKORD: {highscore_text}", True, (255,204,0))
        rect = title.get_rect(center=(400, 200))
        screen.blit(title, rect.topleft)

        mouse_pos = pygame.mouse.get_pos()

        for i, button in enumerate(self.buttons):
            if button["rect"] is None:
                rect = self.small_font.render(button["text"], True, (220, 220, 220)).get_rect(center=(400, 250 + i * 50))
                button["rect"] = rect

            if button["rect"].collidepoint(mouse_pos):
                text = self.small_font.render(button["text"], True, (150, 150, 150))
            else:
                text = self.small_font.render(button["text"], True, (220, 220, 220))

            screen.blit(text, button["rect"].topleft)

    def update(self):
        pass