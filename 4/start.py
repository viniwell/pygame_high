import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import Game_stats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from gr_rect import Gr_rect


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и слздает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Створення екземпляру для зберігання ігрової статистики
        self.stats = Game_stats(self)
        self.sb=Scoreboard(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.gr_rect=Gr_rect(self)
        self._create_fleet()
        self.start_game()
        self.play_button=Button(self, 'Play')
        self.b1=Button(self, '1')
        self.b2=Button(self, '2')
        self.b3=Button(self, '3')
        self.b4=Button(self, '4')
        self.b5=Button(self, '5')
        self.buttons_pos()
    def buttons_pos(self):
        self.b1.rect.centerx=self.screen.get_rect().centerx
        self.b2.rect.centerx=self.screen.get_rect().centerx
        self.b3.rect.centerx=self.screen.get_rect().centerx
        self.b4.rect.centerx=self.screen.get_rect().centerx
        self.b5.rect.centerx=self.screen.get_rect().centerx
        self.b1.rect.top=200
        self.b2.rect.top=self.b1.rect.bottom+20
        self.b3.rect.top=self.b2.rect.bottom+20
        self.b4.rect.top=self.b3.rect.bottom+20
        self.b5.rect.top=self.b4.rect.bottom+20
        self.b1.msg_image_rect.top=200
        self.b2.msg_image_rect.top=self.b1.msg_image_rect.top+70
        self.b3.msg_image_rect.top=self.b2.msg_image_rect.top+70
        self.b4.msg_image_rect.top=self.b3.msg_image_rect.top+70
        self.b5.msg_image_rect.top=self.b4.msg_image_rect.top+70


    def _create_fleet(self):
        """Створення флота прибульців"""
        # Створення прибульця і обрахунок кількості прибульців в ряду
        # Інтервал між сусідніми прибульцями дорівнює ширині прибульця
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Визначення кількості рядів
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Створення флоту прибульців
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)            

    def _create_alien(self, alien_number, row_number):
        # Створення прибульця та розміщення його в ряду
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагує на досягнення прибульцем краю екрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        """Опускає весь флот та змінєю його напрям руху"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            if not self.settings.ask:
                self.ship.update()
                self._update_bullets()
                if self.stats.game_active:
                    self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)  
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                if self.settings.ask:
                    self.check_buttons(mouse_pos)
                self._check_play_button(mouse_pos)


    def _check_play_button(self, mouse_pos):
        button_click=self.play_button.rect.collidepoint(mouse_pos)
        if button_click and self.settings.draw_button:
            self.stats.game_active=True
            self.start_game()
    def check_buttons(self, mouse_pos):
        if self.settings.ask:
            button_click=[]
            button_click.append(self.b1.rect.collidepoint(mouse_pos))
            button_click.append(self.b2.rect.collidepoint(mouse_pos))
            button_click.append(self.b3.rect.collidepoint(mouse_pos))
            button_click.append(self.b4.rect.collidepoint(mouse_pos))
            button_click.append(self.b5.rect.collidepoint(mouse_pos))
            for button in button_click:
                if button:
                    self.settings.hardness=button_click.index(True)+1
                    self.settings.ask=False
    def start_game(self):
        if self.stats.game_active:
            self.settings.ask=True
            self.ship=Ship(self)
            self.settings.initialyse_dynamic_settings()
            self.stats.reset_stats()
            self.sb._prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.stats.game_active=True

            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(True)
        else:
            self.ship=Ship(self)
            self.settings.b_missed=0
            self.ship.center_ship()
            pygame.mouse.set_visible(True)
    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш"""
        if self.stats.game_active:
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            elif event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_SPACE:
                self._fire_bullet()
            elif event.key==pygame.K_p:
                if not self.stats.game_active:
                    self.stats.game_active=True
                    self.start_game()
        else:
            if event.key == pygame.K_UP:
                self.ship.moving_up = True
                self.settings.draw_button=False
            elif event.key == pygame.K_DOWN:
                self.ship.moving_down = True
                self.settings.draw_button=False
            elif event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_SPACE:
                self._fire_bullet()
                self.settings.draw_button=False
            elif event.key==pygame.K_p:
                if not self.stats.game_active:
                    self.stats.game_active=True
                    self.start_game()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key==pygame.K_UP:
            self.ship.moving_up=False
        if event.key==pygame.K_DOWN:
            self.ship.moving_down=False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды"""
        self.bullets.update()

        # Удаление снарядов, вішедших за край экрана
        if self.stats.game_active:
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            
            self._check_bullet_alien_collisions()
        else:
            for bullet in self.bullets.copy():
                if bullet.rect.collidepoint((self.gr_rect.rect.x, self.gr_rect.rect.y)):
                    self.bullets.remove(bullet)
                if bullet.rect.left >= self.settings.screen_width:
                    self.bullets.remove(bullet)
                    self.settings.b_missed+=1
                    if self.settings.b_missed==3:
                        self.settings.draw_button=True
                        self.settings.b_missed=0


    def _check_bullet_alien_collisions(self):
        if self.stats.game_active:
            # Перевірка потраплянь у прибульців
            collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
            if collisions:
                for aliens in collisions.values():
                    self.stats.score+=self.settings.alien_points*len(aliens           )
                self.sb._prep_score()
                self.sb.check_high_score()
            if not self.aliens:
                # Знищення існуючих снарядів та створення нового флоту
                self.bullets.empty()
                sleep(0.1)
                self._create_fleet()
                self.settings.increase_speed()

                self.stats.level+=1
                self.sb.prep_level()

    def _update_aliens(self):
        """Оновлює позиції всіх прибільців з флоту"""
        self._check_fleet_edges()
        self.aliens.update()

        # Перевірка колізій "прибулець - корабель"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Перевірити, чи досягли прибульці нижнього краю
        self._check_aliens_bottom()
    
    def _check_aliens_bottom(self):
        """Перевіряє, чи досягли прибульці нижнього краю екрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        """Обробляє зіткнення корабля з прибульцем"""
        if self.stats.ships_left > 1:
            # Зменшення ships_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Очищення списків прибульців та снарядів
            self.aliens.empty()
            self.bullets.empty()

            # Створення нового флоту та розміщення корабля по центру
            self._create_fleet()
            self.ship.center_ship()

            # Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран"""
        if self.stats.game_active:
            if not self.settings.ask:
                self.screen.fill(self.settings.bg_color)
                self.ship.blitme()
                for bullet in self.bullets.sprites():
                    bullet.draw_bullet()
                self.aliens.draw(self.screen)
                self.sb.show_score()
            else:
                self.screen.fill(self.settings.bg_color)
                self.b1.draw_button()
                self.b2.draw_button()
                self.b3.draw_button()
                self.b4.draw_button()
                self.b5.draw_button()
        else:
            self.screen.fill(self.settings.bg_color)
            if self.settings.draw_button:
                self.play_button.draw_button()
                self.ship.center_ship()
                self.gr_rect.start_pos()
                self.ship.blitme()
                self.gr_rect.draw()
            else:
                self.ship.blitme()
                self.gr_rect.update()
                self.gr_rect.draw()
                for bullet in self.bullets.sprites():
                    bullet.draw_bullet()
        # Отображение последнего прорисованного экрана
        pygame.display.flip()

if __name__ == '__main__':
    # Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()