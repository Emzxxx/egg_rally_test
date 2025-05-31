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
            pyxel.rect(egg.x, egg.y, egg.width, egg.height, 7)
            self.draw_range(egg)
            self.draw_egg_hp(egg)

    def draw_egg_hp(self, egg: EggInfo):
        pyxel.text(egg.x - 5, egg.y + 10, f"{egg.hp}/{egg.max_hp}", 7)

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
            pyxel.rect(enemy.x, enemy.y, enemy.width, enemy.height, 8)

    def draw_eggnemies_defeated(self, eggnemies_defeated: int):
        pyxel.text(10, 10, f'{eggnemies_defeated}', 7)

    def draw_egg_stats(self, egg: EggInfo):
        pyxel.text(10, 20, f"ATK: {egg.attack_stat}", 7)
        pyxel.text(10, 30, f"SPD: {egg.speed}", 7)
        pyxel.text(10, 40, f"EXP: {egg.eggxperience}", 7)

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
            pyxel.text(enemy.x - 5, enemy.y + 10, f"{enemy.hp}/{enemy.max_hp}", 7)

    def draw_boss(self, boss: EggInfo):
        pyxel.rect(boss.x, boss.y, boss.width, boss.height, 9)

    def draw_boss_hp(self, boss: EggInfo):
        pyxel.text(boss.x - 5, boss.y + 10, f"{boss.hp}/{boss.max_hp}", 9)

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
