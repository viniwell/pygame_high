import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    '''Класс для управления снарядами'''
    def __init__(self, ai_game):
        super().__init__()
        self.game=ai_game
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.color=self.settings.bullet_color

        #Создание снаряда в позиции 0:0 и назначение правильной позиции
        if self.game.stats.game_active:
            self.rect=pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
            self.rect.midtop=ai_game.ship.rect.midtop
        else:
            self.rect=pygame.Rect(0, 0, self.settings.bullet_height, self.settings.bullet_width)
            self.rect.midleft=ai_game.ship.rect.midright   

        #позиция снаряда хранится в вещ формате
        self.x=float(self.rect.x)
        self.y=float(self.rect.y)

    def update(self):
        '''Пермещение снаряда'''
        if self.game.stats.game_active:
            self.y-=self.settings.bullet_speed
            self.rect.y=self.y
        else:
            self.x+=self.settings.bullet_speed
            self.rect.x=self.x
    def draw_bullet(self):
        '''Вывод снаряда на экран'''
        pygame.draw.rect(self.screen, self.color, self.rect)