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
    def __init__(self, x: int, y: int):
        super().__init__(
            x,
            y,
            settings["eggnemy_width"],
            settings["eggnemy_height"],
            settings["eggnemy_initial_hp"]
        )
        self.speed = 1

class Boss(Egg):
    def __init__(self, x: int, y: int):
        super().__init__(
            x,
            y,
            settings["boss_width"],
            settings["boss_height"],
            settings["boss_initial_hp"]
        )
        self.speed = 1.5

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

def is_in_range(egg: Egg, enemy: Eggnemy | Boss) -> bool:
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
        egg.x = max(0, egg.x - egg.speed)
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
        egg.x = min(settings["world_width"] - egg.width, egg.x + egg.speed)
    if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
        egg.y = min(settings["world_height"] - egg.height, egg.y + egg.speed)
    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
        egg.y = max(0, egg.y - egg.speed)

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
                        random.randint(0, settings["world_height"])
                    )

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
    draw_egg(egg)
    draw_egg_hp(egg)
    draw_range(egg)
    draw_eggnemies(enemies)
    draw_eggnemies_defeated(eggnemies_defeated)
    draw_eggnemies_hp(enemies)
    if boss:
        draw_boss(boss)
        draw_boss_hp(boss)

def main():
    pyxel.init(settings["world_width"], settings["world_height"], fps=settings["fps"])
    pyxel.run(update, draw)

if __name__ == "__main__":
    main()
