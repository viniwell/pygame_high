import pygame
class Gr_rect:

    def __init__(self, ai_game):
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()
        self.width, self.height=100, 100
        self.button_color=(0, 255, 0)
        self.scale=1
        self.y=self.rect.y
        self.start_pos()
    def start_pos(self):
        self.rect=pygame.Rect(0, 0, self.width, self.height)
        self.rect.right=self.screen_rect.right
    def update(self):
        if self.rect.bottom==self.screen_rect.bottom:
            self.scale=-1
        elif self.rect.top==self.screen_rect.top:
            self.scale=1
        self.y+=self.scale*5
    def draw(self):
        self.screen.fill(self.button_color, self.rect)
