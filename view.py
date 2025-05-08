import pyxel
from model import GameModel


class GameView:
    def __init__(self, model: GameModel):
        self.model = model

    def draw(self):
        pyxel.cls(0)
        if self.model.egg.is_alive():
            pyxel.rect(self.model.egg.x, self.model.egg.y, self.model.egg.width, self.model.egg.height, 7)
            for enemy in self.model.eggnemies:
                pyxel.rect(enemy.x, enemy.y, enemy.width, enemy.height, 8)
            pyxel.text(2, 2, f"{self.model.egg.hp}/{self.model.egg.max_hp}", 7)
