import random
# from abc import ABC 
from typing import Literal, Any


egg_range: int = 10


class Egg:
    def __init__(self, x: float, y: float, width: float, height: float, hp: int):
        self.x = x
        self.y = y
        self.relative_x = x
        self.relative_y = y
        self.width = width
        self.height = height
        self.max_hp = hp
        self.hp = hp
        self._speed = 2

    @property
    def top(self) -> float:
        return self.y

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.x + self.width
    
    @property
    def speed(self):
        return self._speed
    
    @property
    def center(self) -> tuple[float, float]:
        return (self.x + self.width / 2, self.y + self.height / 2)

class Eggnemy(Egg):
    def __init__(self, x: float, y: float, width: float, height: float, hp: int):
        super().__init__(x, y, width, height, hp)
        self._speed = 1
        self._dps = 1
        self._is_boss: bool = False    

    @property
    def speed(self):
        return self._speed
    
    @property
    def dps(self):
        return self._dps
    
    @property
    def is_boss(self):
        return self._is_boss

class Boss(Eggnemy):
    def __init__(self, x: float, y: float, width: float, height: float, hp: int):
        super().__init__(x, y, width, height, hp)
        self._speed = 1.5
        self._dps = 3
        self._is_boss: bool = True    


class GameModel:
    def __init__(self, settings: dict[str, Any]):
        self._settings = settings
        self._width: int = settings["world_width"]
        self._height: int = settings["world_height"]
        self._fps: int = settings["fps"]
        self.leaderboard: list[int] = []
        self.init_state()

    def init_state(self):
        self.egg: Egg = Egg(
            self._settings["world_width"] // 2,
            self._settings["world_height"] // 2,
            self._settings["egg_width"],
            self._settings["egg_height"],
            self._settings["egg_initial_hp"]
        )

        self.eggnemies: list[Eggnemy] = []
        occupied_centers: set[tuple[float, float]] = set()

        for _ in range(self._settings["eggnemy_count"]):
            while True:
                x = random.randint(-150, self._width + 150)
                y = random.randint(-150, self._height + 150)
                new_enemy = Eggnemy(
                    x,
                    y,
                    self._settings["eggnemy_width"],
                    self._settings["eggnemy_height"],
                    self._settings["eggnemy_initial_hp"]
                )
                if new_enemy.center not in occupied_centers:
                    self.eggnemies.append(new_enemy)
                    occupied_centers.add(new_enemy.center)
                    break

        self.boss: Boss | None = None
        self.boss_has_spawned: bool = False

        self.i_frame: int = 0
        self.eggnemies_defeated: int = 0
        self.total_frames_passed: int = 0
        self._game_over_win: bool = False
        self._game_over_loss: bool = False

    def is_in_collision(self, enemy: Eggnemy) -> bool:
        egg = self.egg
        if egg.right < enemy.left or egg.left > enemy.right:
            return False
        if egg.top > enemy.bottom or egg.bottom < enemy.top:
            return False
        return True

    def is_in_range(self, enemy: Eggnemy) -> bool:
        egg = self.egg
        if enemy.left - egg.right > egg_range or egg.left - enemy.right > egg_range:
            return False
        if egg.top - enemy.bottom > egg_range or enemy.top - egg.bottom > egg_range:
            return False
        return True

    def shift_enemies(self, direction: Literal["left", "right", "up", "down"]):
        dx, dy = 0, 0
        if direction == "left" and self.egg.relative_x + self.egg.width < self._settings["world_width"]:
            dx = -self.egg.speed
        elif direction == "right" and self.egg.relative_x > 0:
            dx = self.egg.speed
        elif direction == "up" and self.egg.relative_y + self.egg.height < self._settings["world_height"]:
            dy = -self.egg.speed
        elif direction == "down" and self.egg.relative_y > 0:
            dy = self.egg.speed

        for enemy in self.eggnemies:
            enemy.x += dx
            enemy.y += dy

    def add_to_leaderboard(self, new_score_in_frames: int):
        #Pretty lazy way of doing it
        self.leaderboard.append(new_score_in_frames)
        self.leaderboard.sort()
        if len(self.leaderboard) > 3:
            self.leaderboard.pop()

    def update_entities(self):
        for enemy in self.eggnemies:
            if enemy.x < self.egg.x:
                enemy.x += enemy.speed
            elif enemy.x > self.egg.x:
                enemy.x -= enemy.speed
            if enemy.y < self.egg.y:
                enemy.y += enemy.speed
            elif enemy.y > self.egg.y:
                enemy.y -= enemy.speed

        if self.i_frame == 0:
            for enemy in self.eggnemies:
                if self.is_in_collision(enemy):
                    self.egg.hp -= enemy.dps
                    self.i_frame = self._fps
                    break

        if self.i_frame > 0:
            self.i_frame -= 1

    def attack(self):
        for enemy in self.eggnemies[:]:
            if self.is_in_range(enemy):
                enemy.hp -= 1
                if enemy.hp == 0:
                    if enemy.is_boss:
                        self.boss = None
                    self.eggnemies.remove(enemy)
                    self.eggnemies_defeated += 1

        if (
            self.boss is None 
            and self.eggnemies_defeated >= 3 
            and not self.boss_has_spawned
        ):
            self.boss = Boss(
                random.randint(-150, self._settings["world_width"] + 150),
                random.randint(-150, self._settings["world_height"] + 150),
                self._settings["boss_width"],
                self._settings["boss_height"],
                self._settings["boss_initial_hp"]
            )
            self.boss_has_spawned = True
            self.eggnemies.append(self.boss)

    def update(self, pressing_left: bool, pressing_right: bool, pressing_up: bool, pressing_down: bool, pressing_attack: bool, pressing_restart: bool):
        if pressing_restart and (self._game_over_win or self._game_over_loss):
            self.add_to_leaderboard(self.total_frames_passed)
            self.init_state()
            return

        egg = self.egg

        if egg.hp <= 0:
            self._game_over_loss = True
            return

        #TODO: Fix win condition
        if self.boss_has_spawned and self.boss is None:
            self._game_over_win = True
            return

        if pressing_left:
            egg.relative_x = max(0, egg.relative_x - egg.speed)
            self.shift_enemies("right")
        if pressing_right:
            egg.relative_x = min(self._settings["world_width"] - egg.width, egg.relative_x + egg.speed)
            self.shift_enemies("left")
        if pressing_down:
            egg.relative_y = min(self._settings["world_height"] - egg.height, egg.relative_y + egg.speed)
            self.shift_enemies("up")
        if pressing_up:
            egg.relative_y = max(0, egg.relative_y - egg.speed)
            self.shift_enemies("down")

        if pressing_attack:
            self.attack()

        self.update_entities()
        self.total_frames_passed += 1
    
    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def fps(self):
        return self._fps
    
    @property
    def game_over_win(self):
        return self._game_over_win
    
    @property
    def game_over_loss(self):
        return self._game_over_loss

    @property
    def export_egg(self):
        return self.egg
