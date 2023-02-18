import pygame
from pygame.sprite import Sprite
class Alien(Sprite):
    '''Клас для одного прибульця'''
    def __init__(self, ai_game):
        '''Ініціалізує прибульця'''
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings  
        #завантаження зображення прибульця та призначення атр rect
        self.image=pygame.image.load('images/alien.bmp')
        self.rect=self.image.get_rect()
        #Кожен новий прибулець з'являється у лів верхньому куті
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        #збереження точної горизонтальної позиції
        self.x=float(self.rect.x)
    def check_edges(self):
        '''Тру, якщо прибульці бфілчя краю'''
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right or self.rect.left<=0:
            return True
    def update(self):
        '''Перміщує прибульців'''
        self.x+=self.settings.alien_speed*self.settings.fleet_direction
        self.rect.x=self.x