import pyxel
from model import Egg, Eggnemy
from collections.abc import Callable

class View:
    def __init__(self, width: int, height: int) -> None:
        pyxel.init(width, height)
        self._width = width
        self._height = height

    def start(self, fps: int, update_fn: Callable[[], None], draw_fn: Callable[[], None]) -> None:
        pyxel.run(update_fn, draw_fn)

    def clear(self) -> None:
        pyxel.cls(0)

    def draw_egg(self, egg: Egg) -> None:
        pyxel.rect(egg.x, egg.y, egg.width, egg.height, 7)

    def draw_eggnemies(self, enemies: list[Eggnemy]) -> None:
        for e in enemies:
            pyxel.rect(e.x, e.y, e.width, e.height, 8)

    def draw_hp(self, hp: int, max_hp: int) -> None:
        pyxel.text(5, 5, f"Health: {hp}/{max_hp}", 7)

    def is_left_pressed(self) -> bool:
        return pyxel.btn(pyxel.KEY_LEFT)

    def is_right_pressed(self) -> bool:
        return pyxel.btn(pyxel.KEY_RIGHT)

    def is_up_pressed(self) -> bool:
        return pyxel.btn(pyxel.KEY_UP)

    def is_down_pressed(self) -> bool:
        return pyxel.btn(pyxel.KEY_DOWN)

    def is_l_pressed(self) -> bool:
        return pyxel.btnp(pyxel.KEY_L)