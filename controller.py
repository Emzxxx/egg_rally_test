import pyxel
from model import GameModel
from view import GameView


class GameController:
    def __init__(self, model: GameModel, view: GameView):
        self.model = model
        self.view = view

    def start(self):
        model = self.model

        self.view.start(model.fps, self, self)

    def update(self):
        egg = self.model.egg

        if egg.hp == 0 or self.model.game_over_win:
            return

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            egg.relative_x = max(0, egg.relative_x - egg.speed)
            self.model.shift_enemies("right")
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            egg.relative_x = min(self.model.settings["world_width"] - egg.width, egg.relative_x + egg.speed)
            self.model.shift_enemies("left")
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            egg.relative_y = min(self.model.settings["world_height"] - egg.height, egg.relative_y + egg.speed)
            self.model.shift_enemies("up")
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            egg.relative_y = max(0, egg.relative_y - egg.speed)
            self.model.shift_enemies("down")

        if pyxel.btn(pyxel.KEY_L):
            self.model.attack()

        self.model.tick()


    def draw(self):
        pyxel.cls(0)
        self.view.draw_world_border(self.model.egg.relative_x, self.model.egg.relative_y)
        self.view.draw_egg(self.model.egg)
        self.view.draw_eggnemies(self.model.eggnemies)
        self.view.draw_eggnemies_defeated()
        self.view.draw_time_passed()
        self.view.draw_eggnemies_hp(self.model.eggnemies)

        if self.model.boss and self.model.boss.hp > 0:
            self.view.draw_boss(self.model.boss)
            self.view.draw_boss_hp(self.model.boss)

        if self.model.game_over_win:
            self.view.draw_win_message()
