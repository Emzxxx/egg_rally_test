import random
from typing import Literal, Any
from project_types import Egg, Eggnemy_Template, Eggnemy_Spawner_Interface, Boss_Spawner_Interface


class GameModel:
    def __init__(self, settings: dict[str, Any], eggnemy_spawner : Eggnemy_Spawner_Interface, boss_spawner: Boss_Spawner_Interface):
        self._settings = settings
        self._width: int = settings["world_width"]
        self._height: int = settings["world_height"]
        self._fps: int = settings["fps"]
        self._egg_range: int = 10
        self._leaderboard: list[int] = []
        self._eggnemy_spawner = eggnemy_spawner
        self._boss_spawner = boss_spawner

        self._just_defeated_boss = False
        self._just_unlocked_egghancement = False
        self._just_died = False

        self.waiting_for_egghancement = False
        self.hp_incr = settings["hp_incr"]
        self.attack_incr = settings["attack_incr"]
        self.speed_incr = settings["speed_incr"]
        self.egghancement_threshhold = settings["egghancement_threshhold"]

        self.eggnemy_hp_incr = settings["eggnemy_wave_increment_hp"]
        self.eggnemy_attack_incr = settings["eggnemy_wave_increment_attack"]
        self.eggnemy_speed_incr = settings["eggnemy_wave_increment_speed"]
        
        
        self.boss_hp_incr = settings["boss_wave_increment_hp"]
        self.boss_attack_incr = settings["boss_wave_increment_attack"]
        self.boss_speed_incr = settings["boss_wave_increment_speed"]

        self.invalid_enemy_x_spawn: list[int] = [_ for _ in range(self.width//2-12, self.width//2+self._settings["egg_width"]+13)]
        self.invalid_enemy_y_spawn: list[int] = [_ for _ in range(self.height//2-12, self.height//2+self._settings["egg_height"]+13)]

        self.init_state()

    def init_state(self):
        self.i_frame: int = 0
        self.eggnemies_defeated: int = 0
        self.next_egghancement_at = self.egghancement_threshhold
        self._wave = 0

        self.total_frames_passed: int = 0
        self._game_over_loss: bool = False
        self.can_spawn_boss: bool = False

        self.egg: Egg = Egg(
            self.width // 2,
            self.height // 2,
            self._settings["egg_width"],
            self._settings["egg_height"],
            self._settings["egg_initial_hp"],
            self._settings["egg_initial_attack"],
            self._settings["egg_initial_speed"],
        )
        self.normal_eggnemies: list[Eggnemy_Template] = []
        self.spawn_enemies()

        self.bosses: list[Eggnemy_Template] = []
        self.bosses_spawned: int = 0
        
    def valid_enemy_spawn_x(self):
        while True:
            x = random.randint(-150, self.width + 150)
            if x not in self.invalid_enemy_x_spawn:
                return x

    def valid_enemy_spawn_y(self):
        while True:
            y = random.randint(-150, self.height + 150)
            if y not in self.invalid_enemy_y_spawn:
                return y

    def spawn_enemies(self):
        occupied_centers: set[tuple[float, float]] = set()

        for _ in range(self._settings["eggnemy_count"]):
            while True:
                x = self.valid_enemy_spawn_x()
                y = self.valid_enemy_spawn_y()
                new_enemy = self._eggnemy_spawner.spawn_eggnemy(
                    x,
                    y,
                    self._settings["eggnemy_width"],
                    self._settings["eggnemy_height"],
                    self._settings["eggnemy_initial_hp"] + self.eggnemy_hp_incr * self.wave,
                    self._settings["eggnemy_initial_attack"] + self.eggnemy_attack_incr * self.wave,
                    self._settings["eggnemy_initial_speed"] + self.eggnemy_speed_incr * self.wave
                )
                if new_enemy.center not in occupied_centers:
                    self.normal_eggnemies.append(new_enemy)
                    occupied_centers.add(new_enemy.center)
                    break
    
    def next_wave(self):
        self._wave += 1

    def is_in_collision(self, enemy: Eggnemy_Template) -> bool:
        egg = self.egg
        if egg.right < enemy.left or egg.left > enemy.right:
            return False
        if egg.top > enemy.bottom or egg.bottom < enemy.top:
            return False
        return True

    def is_in_range(self, enemy: Eggnemy_Template) -> bool:
        egg = self.egg
        if enemy.left - egg.right > self.egg_range or egg.left - enemy.right > self.egg_range:
            return False
        if egg.top - enemy.bottom > self.egg_range or enemy.top - egg.bottom > self.egg_range:
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

        for enemy in self.current_total_eggnemies:
            enemy.x += dx
            enemy.y += dy

    def add_to_leaderboard(self, new_score_in_frames: int):
        self.leaderboard.append(new_score_in_frames)
        self.leaderboard.sort(reverse=True)
        if len(self.leaderboard) > 3:
            self.leaderboard.pop()

    def update_entities(self):
        current_centers = {enemy.center for enemy in self.current_total_eggnemies}

        new_centers: set[tuple[float, float]] = set()

        for enemy in self.current_total_eggnemies:
            # Keep old center in case a move is rejected
            old_center = enemy.center
            dx = 0
            dy = 0

            if enemy.x < self.egg.x:
                dx = enemy.speed
            elif enemy.x > self.egg.x:
                dx = -enemy.speed

            if enemy.y < self.egg.y:
                dy = enemy.speed
            elif enemy.y > self.egg.y:
                dy = -enemy.speed

            new_x = enemy.x + dx
            new_y = enemy.y + dy

            # Compute the new center
            temp_center = (new_x + enemy.width / 2, new_y + enemy.height / 2)

            # Only apply move if no eggnemy has the new center
            if temp_center not in current_centers and temp_center not in new_centers:
                enemy.x = new_x
                enemy.y = new_y
                new_centers.add(temp_center)
            else:
                # Keep old center
                new_centers.add(old_center)

        if self.i_frame == 0:
            for enemy in self.current_total_eggnemies:
                if self.is_in_collision(enemy):
                    self.egg.hp -= enemy.attack_stat
                    self.i_frame = self._fps
                    break

        if self.i_frame > 0:
            self.i_frame -= 1

    def attack(self):
        #Normal enemies
        for enemy in self.normal_eggnemies:
            if self.is_in_range(enemy):
                enemy.hp -= self.egg.attack_stat
                if enemy.hp <= 0:
                    self.normal_eggnemies.remove(enemy)
                    self.eggnemies_defeated += 1
                    self.egg.eggxperience += 1
                    self.can_spawn_boss = True
                    #Can only spawn a boss after killing something

        #Boss type enemies (separated since normals and bosses have different extra conditions)
        for boss in self.bosses:
            if self.is_in_range(boss):
                boss.hp -= self.egg.attack_stat
                if boss.hp <= 0:
                    self.bosses.remove(boss)
                    self._just_defeated_boss = True
                    self.next_wave()
                    self.spawn_enemies()
                    self.eggnemies_defeated += 1
                    self.egg.eggxperience += 1
                    self.can_spawn_boss = True
                    #Can only spawn a boss after killing something


        if (
            self.eggnemies_defeated / self._settings["boss_spawn_threshhold"] >= self.bosses_spawned + 1
            and self.can_spawn_boss
        ):
            #Can only spawn a boss once per wave
            self.can_spawn_boss = False

            while True:
                x = self.valid_enemy_spawn_x()
                y = self.valid_enemy_spawn_y()
                new_boss = self._boss_spawner.spawn_boss(
                    x, y,
                    self._settings["boss_width"],
                    self._settings["boss_height"],
                    self._settings["boss_initial_hp"] + self.boss_hp_incr * self.wave,
                    self._settings["boss_initial_attack"] + self.boss_attack_incr * self.wave,
                    self._settings["boss_initial_speed"] + self.boss_speed_incr * self.wave
                )
                if all(new_boss.center != e.center for e in self.current_total_eggnemies):
                    self.bosses.append(new_boss)
                    break

            self.bosses_spawned += 1

    def update(self, pressing_left: bool, pressing_right: bool, pressing_up: bool, pressing_down: bool, pressing_attack: bool, pressing_restart: bool):
        
        if pressing_restart and self._game_over_loss:
            self.add_to_leaderboard(self.total_frames_passed)
            self.init_state()
            return

        egg = self.egg

        if egg.hp <= 0:
            if not self._game_over_loss:
                self._just_died = True
            self._game_over_loss = True
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

        if self.egg.eggxperience >= self.next_egghancement_at:
            self._just_unlocked_egghancement = True
            self.waiting_for_egghancement = True

        if self.waiting_for_egghancement:
            return

        self.update_entities()
        self.total_frames_passed += 1
    
    def apply_egghancement(self, choice: int):
        if choice == 1:
            self.egg.max_hp += self.hp_incr
            self.egg.hp += self.hp_incr
        elif choice == 2:
            self.egg.set_attack(self.egg.attack_stat + self.attack_incr)
        elif choice == 3:
            self.egg.set_speed(self.egg.speed + self.speed_incr)

        self.waiting_for_egghancement = False
        self.next_egghancement_at += self.egghancement_threshhold  

    def reset_just_defeated_boss(self):
        self._just_defeated_boss = False

    def reset_just_died(self):
        self._just_died = False

    def reset_just_unlocked_egghancement(self):
        self._just_unlocked_egghancement = False

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
    def egg_range(self):
        return self._egg_range
    @property
    def wave(self):
        return self._wave
    
    @property
    def game_over_loss(self):
        return self._game_over_loss
    
    @property
    def just_defeated_boss(self) -> bool:
        return self._just_defeated_boss
    
    @property
    def just_died(self) -> bool:
        return self._just_died

    @property
    def just_unlocked_egghancement(self) -> bool:
        return self._just_unlocked_egghancement
    
    @property
    def current_total_eggnemies(self):
        return self.normal_eggnemies + self.bosses
    
    @property
    def leaderboard(self):
        return self._leaderboard

    @property
    def export_egg(self):
        return self.egg
    
    @property
    def settings(self):
        return self._settings