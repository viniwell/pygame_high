import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    '''Класс для управления снарядами'''
    def __init__(self, ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.color=self.settings.bullet_color

        #Создание снаряда в позиции 0:0 и назначение правильной позиции
        self.rect=pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop=ai_game.ship.rect.midtop

        #позиция снаряда хранится в вещ формате
        self.y=float(self.rect.y)

    def update(self):
        '''Пермещение снаряда'''
        self.y-=self.settings.bullet_speed
        self.rect.y=self.y
    def draw_bullet(self):
        '''Вывод снаряда на экран'''
        pygame.draw.rect(self.screen, self.color, self.rect)