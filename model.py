import random
from dataclasses import dataclass
from typing import Any

@dataclass
class Egg:
    x: int
    y: int
    width: int
    height: int
    hp: int
    max_hp: int

@dataclass
class Eggnemy:
    x: int
    y: int
    width: int
    height: int
    is_defeated: bool = False

    def move_toward(self, target_x: int, target_y: int) -> None:
        if self.x < target_x:
            self.x += 1
        elif self.x > target_x:
            self.x -= 1
        if self.y < target_y:
            self.y += 1
        elif self.y > target_y:
            self.y -= 1

class Model:
    def __init__(self, settings: dict[str, Any]) -> None:
        self.settings = settings
        self._width = settings["world_width"]
        self._height = settings["world_height"]
        self._egg = Egg(
            x = self._width // 2,
            y = self._height // 2,
            width = settings["egg_width"],
            height = settings["egg_height"],
            hp = settings["egg_hp"],
            max_hp = settings["egg_hp"],
        )
        self._eggnemies = [
            Eggnemy(
                x = random.randint(0, self._width),
                y = random.randint(0, self._height),
                width = settings["eggnemy_width"],
                height = settings["eggnemy_height"]
            )
            for _ in range(settings["eggnemy_count"])
        ]
        self._damage_cooldown = 0

    def update(self, keys: dict[str, bool]) -> None:
        speed = 2
        if keys["left"]:
            self._egg.x = max(0, self._egg.x - speed)
        if keys["right"]:
            self._egg.x = min(self._width - self._egg.width, self._egg.x + speed)
        if keys["up"]:
            self._egg.y = max(0, self._egg.y - speed)
        if keys["down"]:
            self._egg.y = min(self._height - self._egg.height, self._egg.y + speed)

        for enemy in self._eggnemies:
            if not enemy.is_defeated:
                enemy.move_toward(self._egg.x, self._egg.y)

        self._damage_cooldown += 1
        if self._damage_cooldown >= self.settings["fps"]:
            self._damage_cooldown = 0

        if self._damage_cooldown == 0:
            for enemy in self._eggnemies:
                if not enemy.is_defeated and self._is_colliding(self._egg, enemy):
                    self._egg.hp -= 1
                    break

        if keys["remove_defeated"]:
            for enemy in self._eggnemies:
                if not enemy.is_defeated and self._is_colliding(self._egg, enemy):
                    enemy.is_defeated = True
            self._eggnemies = [e for e in self._eggnemies if not e.is_defeated]


    def _is_colliding(self, a: Egg, b: Eggnemy) -> bool:
        return (
            a.x < b.x + b.width and
            a.x + a.width > b.x and
            a.y < b.y + b.height and
            a.y + a.height > b.y
        )

    @property
    def egg(self) -> Egg:
        return self._egg

    @property
    def eggnemies(self) -> list[Eggnemy]:
        return self._eggnemies

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height