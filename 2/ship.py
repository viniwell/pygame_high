import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    '''Управление кораблем'''
    def __init__(self, ai_game):
        '''инициализирует корабль и задает его начальную позицию'''
        super().__init__()
        self.game=ai_game
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        self.settings=ai_game.settings
        #Загружает изображение корабля и получает прямоугольник
        if self.game.stats.game_active:
            self.image=pygame.image.load('images/ship.bmp')
        else:
            self.image=pygame.image.load('images/ship.bmp')
        self.rect=self.image.get_rect()
        # Каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom=self.screen_rect.midbottom

        self.x=float(self.rect.x)
        #Флаг перемещения
        self.moving_right=False
        self.moving_left=False
        self.moving_up=False
        self.moving_down=False


    def update(self):
        '''Метод обновляет позицию корабля с учетом флага'''
        #Обновляется атрибут x
        if self.game.stats.game_active:
            if self.moving_right and self.rect.right<self.screen_rect.right:
                self.x+=self.settings.ship_speed
            if self.moving_left and self.rect.left>0:
                self.x-=self.settings.ship_speed
            #Обновление атрибута rect на основе self.x
            self.rect.x=self.x
        else:
            if self.moving_up and self.rect.top<self.screen_rect.top:
                self.y+=self.settings.ship_speed
            if self.moving_down and self.rect.bottom>self.screen_rect.bottom:
                self.y-=self.settings.ship_speed
            #Обновление атрибута rect на основе self.x
            self.rect.y=self.y            
    def blitme(self):
        '''Рисует корабль в текущей позиции'''
        self.screen.blit(self.image, self.rect)
    def center_ship(self):
        if not self.game.stats.game_active:
            self.rect.midbottom=self.screen_rect.midbottom
            self.x=float(self.rect.x)
        else:
            self.rect.midleft=self.screen_rect.midleft
            self.y=float(self.rect.y)