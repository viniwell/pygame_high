import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    '''Управление кораблем'''
    def __init__(self, ai_game):
        '''инициализирует корабль и задает его начальную позицию'''
        super().__init__()
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        self.settings=ai_game.settings
        #Загружает изображение корабля и получает прямоугольник
        self.image=pygame.image.load('images/ship.bmp')
        self.rect=self.image.get_rect()
        # Каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom=self.screen_rect.midbottom

        self.x=float(self.rect.x)
        #Флаг перемещения
        self.moving_right=False
        self.moving_left=False

    def update(self):
        '''Метод обновляет позицию корабля с учетом флага'''
        #Обновляется атрибут x
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.x+=self.settings.ship_speed
        if self.moving_left and self.rect.left>0:
            self.x-=self.settings.ship_speed
        #Обновление атрибута rect на основе self.x
        self.rect.x=self.x
    def blitme(self):
        '''Рисует корабль в текущей позиции'''
        self.screen.blit(self.image, self.rect)
    def center_ship(self):
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)