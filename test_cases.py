from model import GameModel, Eggnemy
from typing import Any

#Unit Testing

#Settings locally defined for tests
settings: dict[str, Any] = {
    "fps": 30,
    "world_width": 256,
    "world_height": 256,
    "screen_width": 1024,
    "screen_height": 1024,
    "egg_initial_hp": 10,
    "egg_width": 8,
    "egg_height": 10,
    "eggnemy_initial_hp": 2,
    "eggnemy_count": 10,
    "eggnemy_width": 8,
    "eggnemy_height": 10,
    "boss_spawn_threshhold": 10,
    "boss_initial_hp": 20,
    "boss_width": 8,
    "boss_height": 10
}

def test_initial_game_state():
    model = GameModel(settings)

    assert model.boss is None
    assert model.boss_has_spawned == False
    assert model.eggnemies_defeated == 0
    assert model.total_frames_passed == 0
    assert model.game_over_win == False
    assert model.game_over_loss == False
    assert len(model.eggnemies) == settings["eggnemy_count"]
    assert len(model.leaderboard) == 0

    model.init_state()
    assert model.boss is None
    assert model.boss_has_spawned == False
    assert model.eggnemies_defeated == 0
    assert model.total_frames_passed == 0
    assert model.game_over_win == False
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
    assert model.boss_has_spawned == False
    assert model.boss is None

    model.attack() 
    model.eggnemies_defeated = 6
    assert model.boss_has_spawned == False
    assert model.boss is None

    model.eggnemies_defeated = 7
    #To access the if condition detailing the boss spawning conditions [You need to attack to kill and need to kill to spawn boss]
    model.attack() 
    assert model.boss_has_spawned == True
    assert model.boss is not None

    model.eggnemies_defeated = 10
    model.attack() 
    assert model.boss_has_spawned == True
    assert model.boss is not None


def test_win_condition_simple():
    #if boss dead, dapat win na
    ...

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

    #<0 hp
    model.update(False, False, False, False, False, False)
    model.egg.hp = -3
        
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
                test_settings["eggnemy_initial_hp"]
            )
    south = Eggnemy(
                test_settings["world_width"]//2,
                test_settings["world_height"],
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"]
            )
    east = Eggnemy(
                test_settings["world_width"],
                test_settings["world_height"]//2,
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"]
            )
    west = Eggnemy(
                0,
                test_settings["world_height"]//2,
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"]
            )
    model.eggnemies = [north, south, east, west]

    model.update(False, False, False, False, False, False)
    
    # [north, south, east, west] = model.eggnemies

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
    ...

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


