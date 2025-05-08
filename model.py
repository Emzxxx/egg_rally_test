from __future__ import annotations
from typing import List, Dict
from random import randint

class Rectangle:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def intersects(self, other: Rectangle) -> bool:
        return (
            self.x < other.x + other.width
            and self.x + self.width > other.x
            and self.y < other.y + other.height
            and self.y + self.height > other.y
        )
    
class Egg(Rectangle):
    def __init__(self, x: int, y: int, width: int, height: int, hp: int):
        super().__init__(x, y, width, height)
        self.max_hp = hp
        self.hp = hp
        self.damage_timer = 0

    def is_alive(self) -> bool:
        return self.hp > 0

class Eggnemy(Rectangle):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)

class GameModel:
    def __init__(self, settings: Dict[str, int]):
        self.settings = settings
        self.egg = Egg(
            settings["world_width"] // 2 - settings["egg_width"] // 2,
            settings["world_height"] // 2 - settings["egg_height"] // 2,
            settings["egg_width"],
            settings["egg_height"],
            settings["egg_hp"]
            )
        self.eggnemies: List[Eggnemy] = [
            Eggnemy(
                randint(0, settings["world_width"] - settings["eggnemy_width"]),
                randint(0, settings["world_height"] - settings["eggnemy_height"]),
                settings["eggnemy_width"],
                settings["eggnemy_height"]
            )
            for _ in range(settings["eggnemy_count"])
        ]
        self.world_width = settings["world_width"]
        self.world_height = settings["world_height"]

    def update_damage_timer(self):
        self.egg.damage_timer += 1
        if self.egg.damage_timer >= self.settings["fps"]:
            self.egg.damage_timer = 0
    
    def damage_egg_if_touched(self):
        if self.egg.damage_timer == 0:
            for eggnemy in self.eggnemies:
                if self.egg.intersects(eggnemy):
                    self.egg.hp -= 1
                    break
    
    def remove_defeated_eggnemies(self):
        self.eggnemies = [e for e in self.eggnemies if not self.egg.intersects(e)]

    def game_should_stop(self):
        return not self.egg.is_alive()