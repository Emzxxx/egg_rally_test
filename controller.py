import pyxel
from model import GameModel
from view import GameView

'''
    TODO: 
    - Boss Spawning Logic (Model)
    - Win conditions (Model)
'''
class GameController:
    def __init__(self, model: GameModel, view: GameView):
        self._model = model
        self._view = view

    def start(self):
        model = self._model

        self._view.start(model.fps, self, self)

    def update(self):
        self._model.update(
            self._view.pressing_left_key(),
            self._view.pressing_right_key(),
            self._view.pressing_up_key(),
            self._view.pressing_down_key(),
            self._view.pressing_attack_key(),
            self._view.pressing_restart_key()
        )


    def draw(self):
        pyxel.cls(0)
        self._view.draw_world_border(self._model.egg.relative_x, self._model.egg.relative_y)
        self._view.draw_egg(self._model.egg)
        self._view.draw_eggnemies(self._model.eggnemies)
        self._view.draw_eggnemies_defeated(self._model.eggnemies_defeated)
        self._view.draw_time_passed(self._model.total_frames_passed, self._model.fps)
        self._view.draw_eggnemies_hp(self._model.eggnemies)

        if self._model.boss and self._model.boss.hp > 0:
            self._view.draw_boss(self._model.boss)
            self._view.draw_boss_hp(self._model.boss)

        if self._model.game_over_win:
            self._view.draw_win_message()
