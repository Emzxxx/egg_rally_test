from model import GameModel, Eggnemy, Boss
from typing import Any
import json

#Unit Testing

#Import settings for tests
with open("settings.json") as f:
    settings: dict[str, Any] = json.load(f)

def test_initial_game_state():
    model = GameModel(settings)

    assert model.boss is None
    assert model.eggnemies_defeated == 0
    assert model.total_frames_passed == 0
    assert model.game_over_loss == False
    assert len(model.eggnemies) == settings["eggnemy_count"]
    assert len(model.leaderboard) == 0

    model.init_state()
    assert model.boss is None
    assert model.eggnemies_defeated == 0
    assert model.total_frames_passed == 0
    assert model.game_over_loss == False
    assert len(model.eggnemies) == settings["eggnemy_count"]

def test_collision_egg_eggnemy():
    #Improve collision code to make it have to accept an egg rin so we can test it here
    ...

def test_collision_egg_wall():
    #testing the max min jazz n stuff of the movemebt
    ...

def test_in_range():
    #lots of eggnemies, have it check if eggnemies are in range or not
    ...

def test_boss_spawning_conditions():
    #if less than the required amount killed, wala pa. If >= that the required then its spawned
    test_settings = settings
    test_settings["boss_spawn_threshhold"] = 7
    test_settings["eggnemy_count"] = 0 #To make it as isolated as possible, chance to randomly kill a stray egg to skew tests
    model = GameModel(test_settings)

    model.eggnemies_defeated = 3
    model.attack() 
    assert model.boss is None

    model.attack() 
    model.eggnemies_defeated = 6
    assert model.boss is None

    model.eggnemies_defeated = 7
    #To access the if condition detailing the boss spawning conditions [You need to attack to kill and need to kill to spawn boss]
    model.attack() 
    assert model.boss is not None

    model.eggnemies_defeated = 10
    model.attack() 
    assert model.boss is not None


def test_win_condition_simple():
    #if boss dead, dapat win na
    test_settings = settings
    #To make it as isolated as possible, less chance to randomly kill or get damaged by a stray egg to skew tests
    test_settings["eggnemy_count"] = 0 
    model = GameModel(test_settings)

    #Newly created
    assert model.boss is None
    model.update(False, False, False, False, False, False)

    #Boss "Exists" for example; Boss just spawned
    model.boss = Boss(0,0,1,1,5,0,0)
    assert model.boss is not None
    model.update(False, False, False, False, False, False)

    #Boss is damaged but not dead
    model.boss.hp = 1
    model.update(False, False, False, False, False, False)
    assert model.boss is not None
    model.update(False, False, False, False, False, False)

    #Boss is dead and is back to being None
    model.boss = None
    model.update(False, False, False, False, False, False)


def test_loss_condition_simple():
    #if egg dead, dapat loss na
    test_settings = settings
    #To make it as isolated as possible, less chance to randomly kill or get damaged by a stray egg to skew tests
    test_settings["eggnemy_count"] = 0 
    model = GameModel(test_settings)
    
    #Newly created
    assert model.game_over_loss == False
    model.update(False, False, False, False, False, False)
    assert model.game_over_loss == False

    #0 hp
    model.egg.hp = 0
    model.update(False, False, False, False, False, False)
    assert model.game_over_loss == True

    #restart game state
    model.init_state()
    
    #<0 hp
    model.egg.hp = -3
    model.update(False, False, False, False, False, False)
        
    assert model.game_over_loss == True

def test_simple_eggnemy_cardinal_movement():
    #4 eggs in 4 cardinal directions, update once, then they're supposed to be closer to the egg
    test_settings = settings
    #To make it as isolated as possible, less chance to randomly kill or get damaged by a stray egg to skew tests
    test_settings["eggnemy_count"] = 0 
    model = GameModel(test_settings)

    north = Eggnemy(
                test_settings["world_width"]//2,
                0,
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"],
                0,0
            )
    south = Eggnemy(
                test_settings["world_width"]//2,
                test_settings["world_height"],
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"],
                0,0
            )
    east = Eggnemy(
                test_settings["world_width"],
                test_settings["world_height"]//2,
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"],
                0,0
            )
    west = Eggnemy(
                0,
                test_settings["world_height"]//2,
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"],
                0,0
            )
    model.eggnemies = [north, south, east, west]

    #1 frame of enemy movement
    model.update(False, False, False, False, False, False)
    
    assert north.x == test_settings["world_width"]//2
    assert north.y == 1

    assert south.x == test_settings["world_width"]//2
    assert south.y == test_settings["world_height"]-1
                
    assert east.x == test_settings["world_width"] - 1
    assert east.y == test_settings["world_height"]//2

    assert west.x == 1
    assert west.y == test_settings["world_height"]//2


def test_simple_eggnemy_ordinal_movement():
    #4 eggs in 4 ordinal directions, update once, then they're supposed to be closer to the egg more
    test_settings = settings
    #To make it as isolated as possible, less chance to randomly kill or get damaged by a stray egg to skew tests
    test_settings["eggnemy_count"] = 0 
    model = GameModel(test_settings)

    north_east = Eggnemy(
                test_settings["world_width"],
                0,
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"],
                0,0
            )
    north_west = Eggnemy(
                0,
                0,
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"],
                0,0
            )
    south_east = Eggnemy(
                test_settings["world_width"],
                test_settings["world_height"],
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"],
                0,0
            )
    south_west = Eggnemy(
                0,
                test_settings["world_height"],
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"],
                0,0
            )
    model.eggnemies = [north_east, north_west, south_east, south_west]
    
    #1 frame of enemy movement
    model.update(False, False, False, False, False, False)

    assert north_east.x == test_settings["world_width"]-1
    assert north_east.y == 1

    assert north_west.x == 1
    assert north_west.y == 1

    assert south_east.x == test_settings["world_width"]-1
    assert south_east.y == test_settings["world_height"]-1

    assert south_west.x == 1
    assert south_west.y == test_settings["world_height"]-1


def test_damage_done_by_enemy_simple():
    ...

def test_damage_done_by_egg_simple():
    ...

def test_removal_when_enemy_dies():
    ...


def test_restart():
    ...

def test_leaderboard():
    ...


