
class Game_stats:
    def __init__(self, ai_game):
        self.settings=ai_game.settings
        self.reset_stats()

        self.game_active=False
        with open('5/record.txt', 'r', encoding='UTF-8') as file:
            self.high_score=int(file.readlines()[-1])
    def reset_stats(self):
        self.ships_left=self.settings.ships_limit
        self.score=0
        self.level=1