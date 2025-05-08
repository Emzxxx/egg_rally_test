from model import Model
from view import View

class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self._model = model
        self._view = view

    def update(self) -> None:
        keys = {
            "left": self._view.is_left_pressed(),
            "right": self._view.is_right_pressed(),
            "up": self._view.is_up_pressed(),
            "down": self._view.is_down_pressed(),
            "remove_defeated": self._view.is_l_pressed(),
        }
        self._model.update(keys)

    def draw(self) -> None:
        self._view.clear()
        self._view.draw_egg(self._model.egg)
        self._view.draw_eggnemies(self._model.eggnemies)
        self._view.draw_hp(self._model.egg.hp, self._model.egg.max_hp)