class Settings:
    '''класс для хранения всех настроек'''
    def __init__(self):
        '''Инициализирует настройки экрана'''
        self.screen_width=1200
        self.screen_height=800
        self.bg_color=(230, 230, 230)

        #Скорость корабля
        self.ships_limit=3

        #параметры снаряда
        
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=(60, 60, 60)
        self.bullets_allowed=3

        #Налаштування прибульців

        self.fleet_drop_speed=100



        self.speed_up_scale=1.3
        self.score_scale=1.5


        self.initialyse_dynamic_settings()


    def initialyse_dynamic_settings(self):
        self.ship_speed= 5
        self.bullet_speed=10
        self.alien_speed=1.5
        self.fleet_direction=1
        self.alien_points=10000
    def increase_speed(self):
        self.ship_speed*=self.speed_up_scale
        self.bullet_speed*=self.speed_up_scale
        self.alien_speed*=self.speed_up_scale
        self.alien_points=int(self.alien_points*self.score_scale)