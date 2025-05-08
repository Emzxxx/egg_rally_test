import pyxel
from model import GameModel


class GameController:
    def __init__(self, model: GameModel):
        self.model = model
        self.speed = 2

    def update(self):
        if not self.model.egg.is_alive():
            return

        dx = (pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT)) - (pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT))
        dy = (pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN)) - (pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP))

        # Move the egg's x and y by dx, dy without exceeding world_width and world_height
        self.model.egg.x = max(0, min(self.model.egg.x + dx * self.speed, self.model.world_width - self.model.egg.width))
        self.model.egg.y = max(0, min(self.model.egg.y + dy * self.speed, self.model.world_height - self.model.egg.height))

        # Move eggnemies to follow the egg's x
        for enemy in self.model.eggnemies:
            if self.model.game_should_stop():
                continue
            if enemy.x < self.model.egg.x:
                enemy.x += 1
            elif enemy.x > self.model.egg.x:
                enemy.x -= 1
            if enemy.y < self.model.egg.y:
                enemy.y += 1
            elif enemy.y > self.model.egg.y:
                enemy.y -= 1

        # Continuously check for damage and attack
        self.model.update_damage_timer()
        self.model.damage_egg_if_touched()

        if pyxel.btn(pyxel.KEY_L):
            self.model.remove_defeated_eggnemies()