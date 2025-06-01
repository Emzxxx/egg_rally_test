import pyxel
from project_types import EggInfo, UpdateHandler, DrawHandler
from collections.abc import Sequence


class GameView:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height

    def start(self, fps: int, update_handler: UpdateHandler, draw_handler: DrawHandler):
        pyxel.init(
            self._width,
            self._height,
            fps=fps
        )
        pyxel.load("assets.pyxres")
        pyxel.run(update_handler.update, draw_handler.draw)

    #Drawing functions
    def draw_world_border(self, relative_x: float, relative_y: float):
        pyxel.rectb(
            self._width // 2 - relative_x,
            self._height // 2 - relative_y,
            self._width,
            self._height,
            7
        )

    def draw_egg(self, egg: EggInfo):
        if egg.hp > 0:
            pyxel.blt(egg.x, egg.y, img=0, u=0, v=0, w=16, h=16, colkey=0)
            self.draw_range(egg)
            self.draw_egg_hp(egg)

    def draw_egg_hp(self, egg: EggInfo):
        pyxel.text(egg.x - 2, egg.y + 20, f"{egg.hp}/{egg.max_hp}", 7)

    def draw_range(self, egg: EggInfo):
        pyxel.rectb(
            egg.x - 10,
            egg.y - 10,
            egg.width + 20,
            egg.height + 20,
            1
        )

    def draw_eggnemies(self, enemies: Sequence[EggInfo]):
        for enemy in enemies:
            pyxel.blt(enemy.x, enemy.y, img=1, u=0, v=0, w=16, h=16, colkey=0)

    def draw_eggnemies_defeated(self, eggnemies_defeated: int):
        pyxel.text(10, 10, f'{eggnemies_defeated}', 7)

    def draw_egg_stats(self, egg: EggInfo):
        pyxel.text(self._width - 50, self._height - 40, f"Atk: {egg.attack_stat}", 7)
        pyxel.text(self._width - 50, self._height - 30, f"Spd: {egg.speed}", 7)
        pyxel.text(self._width - 50, self._height - 20, f"Exp: {egg.eggxperience}", 7)

    def draw_egghancement_prompt(self):
        pyxel.rect(self._width // 4, self._height // 2 - 50, 120, 45, 0)
        pyxel.rectb(self._width // 4, self._height // 2 - 50, 120, 45, 7)
        pyxel.text(self._width // 4 + 10, self._height // 2 - 40, "[1] Increase max HP by 5", 7)
        pyxel.text(self._width // 4 + 10, self._height // 2 - 30, "[2] Increase attack by 1", 7)
        pyxel.text(self._width // 4 + 10, self._height // 2 - 20, "[3] Increase speed by 1", 7)

    def draw_time_passed(self, total_frames_passed: int, fps: int):
        pyxel.text(self._width - 40, 10, self.convert_frame_to_time(total_frames_passed, fps), 7)

    def draw_leaderboard(self, leaderboard: list[int], fps: int):
        score_ctr: int = 0
        pyxel.text(20, self._height - 40, "Top", 7)
        for score in leaderboard:
            pyxel.text(40, self._height - (40 - 10*score_ctr), self.convert_frame_to_time(score, fps), 7)
            score_ctr += 1
        while score_ctr < 3:
            pyxel.text(40, self._height - (40 - 10*score_ctr), "--:--", 7)
            score_ctr += 1

    def convert_frame_to_time(self, frame_count: int, fps: int):
        seconds = frame_count // fps
        minutes = seconds // 60
        seconds %= 60
        return f"{minutes} : {seconds:02}"

    def draw_eggnemies_hp(self, enemies: Sequence[EggInfo]):
        for enemy in enemies:
            pyxel.text(enemy.x - 2, enemy.y + 20, f"{enemy.hp}/{enemy.max_hp}", 7)

    def draw_boss(self, boss: EggInfo):
        pyxel.blt(boss.x, boss.y, img=2, u=0, v=0, w=16, h=16, colkey=0)

    def draw_boss_hp(self, boss: EggInfo):
        pyxel.text(boss.x - 2, boss.y + 20, f"{boss.hp}/{boss.max_hp}", 9)

    def draw_win_message(self):
        pyxel.text(
            self._width // 2 - 10,
            self._height // 2 - 20,
            "You Win!",
            7
        )
    
    def draw_restart_option_message(self):
        pyxel.text(
            self._width // 2 - 20,
            self._height // 2 + 30,
            "Restart? [R]",
            7
        )
    #Key input functions
    def pressing_left_key(self):
        return pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A)
    
    def pressing_right_key(self):
        return pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D)
    
    def pressing_down_key(self):
        return pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S)
    
    def pressing_up_key(self):
        return pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W)
    
    def pressing_attack_key(self):
        return pyxel.btn(pyxel.KEY_L)
    
    def pressing_restart_key(self):
        return pyxel.btn(pyxel.KEY_R)
    
    def pressing_key_1(self): 
        return pyxel.btn(pyxel.KEY_1)
    
    def pressing_key_2(self): 
        return pyxel.btn(pyxel.KEY_2)
    
    def pressing_key_3(self): 
        return pyxel.btn(pyxel.KEY_3)
