import pyxel
import json
from abc import ABC
import random

with open("settings.json") as f:
    settings = json.load(f)

# Global variables
i_frame: int = settings["fps"]
egg_range: int = 10
eggnemies_defeated: int = 0

class Egg(ABC):
    def __init__(self, x: int, y: int, width: int, height: int, hp: int):
        self.x = x
        self.y = y
        self.relative_x = x
        self.relative_y = y
        self.width = width
        self.height = height
        self.max_hp = hp
        self.hp = hp
        self.speed = 2
        

    @property
    def top(self) -> int:
        return self.y

    @property
    def bottom(self) -> int:
        return self.y + self.height

    @property
    def left(self) -> int:
        return self.x

    @property
    def right(self) -> int:
        return self.x + self.width
    
class Eggnemy(Egg):
    def __init__(self, x: int, y: int, width: int, height: int, hp: int):
        super().__init__(
            x,
            y,
            width,
            height,
            hp
        )
        self.speed = 1

class Boss(Eggnemy):
    def __init__(self, x: int, y: int, width: int, height: int, hp: int):
        super().__init__(
            x,
            y,
            width,
            height,
            hp
        )
        self.speed = 1.5

#helper functions
def is_in_collision(egg: Egg, enemy: Eggnemy) -> bool:
    if egg.right < enemy.left:
        return False
    elif egg.left > enemy.right:
        return False
    else:
        if egg.top > enemy.bottom:
            return False
        elif egg.bottom < enemy.top:
            return False
        else:
            return True

def is_in_range(egg: Egg, enemy: Egg) -> bool:
    if enemy.left - egg.right > egg_range:
        return False
    elif egg.left - enemy.right > egg_range:
        return False
    else:
        if egg.top - enemy.bottom > egg_range:
            return False
        elif enemy.top - egg.bottom > egg_range:
            return False
        else:
            return True

def remove_enemy(enemy: Eggnemy, Eggnemies: list[Eggnemy]):
    Eggnemies.remove(enemy)

#TODO: Refactor this into class methods
def shift_enemy_left(enemies: list[Eggnemy]):
    if egg.relative_x + egg.width == settings["world_width"]:
        return
    
    for enemy in enemies:
        enemy.x -= egg.speed

def shift_enemy_right(enemies: list[Eggnemy]):
    if egg.relative_x == 0:
        return
    for enemy in enemies:
        enemy.x += egg.speed

def shift_enemy_up(enemies: list[Eggnemy]):
    if egg.relative_y + egg.height == settings["world_height"]:
        return
    
    for enemy in enemies:
        enemy.y -= egg.speed

def shift_enemy_down(enemies: list[Eggnemy]):
    if egg.relative_y == 0:
        return
    
    for enemy in enemies:
        enemy.y += egg.speed


# Initialize entities
boss = None

egg = Egg(
    settings["world_width"] // 2,
    settings["world_height"] // 2,
    settings["egg_width"],
    settings["egg_height"],
    settings["egg_initial_hp"]
)

enemies: list[Eggnemy] = [
    Eggnemy(
        random.randint(0, settings["world_width"]),
        random.randint(0, settings["world_height"]),
        settings["eggnemy_width"], settings["eggnemy_height"], settings["eggnemy_initial_hp"]
    )
    for _ in range(settings["eggnemy_count"])
]

def update():
    global i_frame
    global eggnemies_defeated
    global boss

    if egg.hp == 0:
        return

    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
        egg.relative_x = max(0, egg.relative_x - egg.speed)
        shift_enemy_right(enemies)
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
        egg.relative_x = min(settings["world_width"] - egg.width, egg.relative_x + egg.speed)
        shift_enemy_left(enemies)
    if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
        egg.relative_y = min(settings["world_height"] - egg.height, egg.relative_y + egg.speed)
        shift_enemy_up(enemies)
    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
        egg.relative_y = max(0, egg.relative_y - egg.speed)
        shift_enemy_down(enemies)

    #Can do better (refactor movemebt INTO an Egg class method)
    for enemy in enemies:
        if enemy.x < egg.x:
            enemy.x += enemy.speed
        if enemy.x > egg.x:
            enemy.x -= enemy.speed
        if enemy.y < egg.y:
            enemy.y += enemy.speed
        if enemy.y > egg.y:
            enemy.y -= enemy.speed
    
    if boss:
        if boss.x < egg.x:
            boss.x += boss.speed
        if boss.x > egg.x:
            boss.x -= boss.speed
        if boss.y < egg.y:
            boss.y += boss.speed
        if boss.y > egg.y:
            boss.y -= boss.speed

    for enemy in enemies:
        if i_frame > 0:
            break
        if is_in_collision(egg, enemy):
            egg.hp -= 1
            i_frame = settings["fps"]

    if i_frame > 0:
        i_frame -= 1

    if pyxel.btn(pyxel.KEY_L):
        for enemy in enemies[:]:
            if is_in_range(egg, enemy):
                enemy.hp -= 1
                if enemy.hp == 0:
                    remove_enemy(enemy, enemies)
                    eggnemies_defeated += 1
                # print(eggnemies_defeated) ## debug
                if (boss is None and 
                    eggnemies_defeated >= settings["boss_spawn_threshhold"]):
                        boss = Boss(
                            random.randint(0, settings["world_width"]),
                            random.randint(0, settings["world_height"]),
                            settings["boss_width"], settings["boss_height"], settings["boss_initial_hp"]
                        )
                        enemies.append(boss)

def draw_world_border():
    pyxel.rectb(settings["world_width"]//2 - egg.relative_x,
               settings["world_height"]//2 - egg.relative_y,
               settings["world_width"], settings["world_height"], 
               7)

def draw_egg(egg: Egg):
    pyxel.rect(egg.x, egg.y, egg.width, egg.height, 7)

def draw_egg_hp(egg: Egg):
    pyxel.text(egg.x - 5, egg.y + 10, f"{egg.hp}/{egg.max_hp}", 7)

def draw_range(egg: Egg):
    pyxel.rectb(egg.x - egg_range, egg.y - egg_range, egg.width + 2 * egg_range, egg.height + 2 * egg_range, 1)

def draw_eggnemies(enemies: list[Eggnemy]) -> None:
    for enemy in enemies:
        pyxel.rect(enemy.x, enemy.y, enemy.width, enemy.height, 8)

def draw_eggnemies_defeated(eggnemies_defeated: int):
    pyxel.text(10, 10, f'{eggnemies_defeated}', 7)

def draw_eggnemies_hp(enemies: list[Eggnemy]) -> None:
    for enemy in enemies:
        pyxel.text(enemy.x - 5, enemy.y + 10, f"{enemy.hp}/{enemy.max_hp}", 7)

def draw_boss(boss: Boss):
    pyxel.rect(boss.x, boss.y, boss.width, boss.height, 9)

def draw_boss_hp(boss: Boss):
    pyxel.text(boss.x - 5, boss.y + 10, f"{boss.hp}/{boss.max_hp}", 9)

def draw():
    pyxel.cls(0)
    draw_world_border()
    draw_egg(egg)
    draw_egg_hp(egg)
    draw_range(egg)
    draw_eggnemies(enemies)
    draw_eggnemies_defeated(eggnemies_defeated)
    draw_eggnemies_hp(enemies)
    if boss:
        if boss.hp > 0:
            draw_boss(boss)
            draw_boss_hp(boss)

def main():
    pyxel.init(settings["world_width"], settings["world_height"], fps=settings["fps"])
    pyxel.run(update, draw)

if __name__ == "__main__":
    main()
