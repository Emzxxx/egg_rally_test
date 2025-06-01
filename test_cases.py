from model import GameModel, Eggnemy, egg_range
from typing import Any
import json

#Unit Testing

#Import settings for tests
with open("settings.json") as f:
    settings: dict[str, Any] = json.load(f)

def test_initial_game_state():
    model = GameModel(settings)

    assert len(model.bosses) == 0
    assert model.eggnemies_defeated == 0
    assert model.total_frames_passed == 0
    assert model.game_over_loss == False
    assert len(model.normal_eggnemies) == settings["eggnemy_count"]
    assert len(model.leaderboard) == 0

    model.init_state()
    assert len(model.bosses) == 0
    assert model.eggnemies_defeated == 0
    assert model.total_frames_passed == 0
    assert model.game_over_loss == False
    assert len(model.normal_eggnemies) == settings["eggnemy_count"]

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
    model.can_spawn_boss = True

    model.attack() 
    assert len(model.bosses) == 0

    model.eggnemies_defeated = 6
    model.can_spawn_boss = True

    model.attack() 
    assert len(model.bosses) == 0

    model.eggnemies_defeated = 7
    model.can_spawn_boss = True
    #To access the if condition detailing the boss spawning conditions [You need to attack to kill and need to kill to spawn boss]
    model.attack() 
    assert len(model.bosses) == 1

    model.eggnemies_defeated = 10
    model.can_spawn_boss = True

    model.attack() 
    assert len(model.bosses) == 1

    model.eggnemies_defeated = 13
    model.can_spawn_boss = True

    model.attack() 
    assert len(model.bosses) == 1

    model.eggnemies_defeated = 14
    model.can_spawn_boss = True

    model.attack() 
    assert len(model.bosses) == 2

    model.eggnemies_defeated = 20
    model.can_spawn_boss = True

    model.attack() 
    assert len(model.bosses) == 2

    model.eggnemies_defeated = 21
    model.can_spawn_boss = True

    model.attack() 
    assert len(model.bosses) == 3


'''
Test case does not apply for phase 6 beyond
Can be converted into wave count tests with just a little tweakinf
since they have similar enough logic 

def test_win_condition_simple():
    #if boss dead, dapat win na
    test_settings = settings
    #To make it as isolated as possible, less chance to randomly kill or get damaged by a stray egg to skew tests
    test_settings["eggnemy_count"] = 0 
    model = GameModel(test_settings)

    #Newly created
    assert len(model.bosses) == 0
    model.update(False, False, False, False, False, False)

    #Boss "Exists" for example; Boss just spawned
    model.bosses = Boss(0,0,1,1,5,0,0)
    assert model.bosses is not None
    model.update(False, False, False, False, False, False)

    #Boss is damaged but not dead
    model.bosses.hp = 1
    model.update(False, False, False, False, False, False)
    assert model.bosses is not None
    model.update(False, False, False, False, False, False)

    #Boss is dead and is back to being None
    model.bosses = None
    model.update(False, False, False, False, False, False)

'''

def test_loss_condition():
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
    test_settings["eggnemy_initial_speed"] = 1

    model = GameModel(test_settings)

    north = Eggnemy(
                test_settings["world_width"]//2,
                0,
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"],
                0,
                test_settings["eggnemy_initial_speed"]
            )
    south = Eggnemy(
                test_settings["world_width"]//2,
                test_settings["world_height"],
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"],
                0,
                test_settings["eggnemy_initial_speed"]
            )
    east = Eggnemy(
                test_settings["world_width"],
                test_settings["world_height"]//2,
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"],
                0,
                test_settings["eggnemy_initial_speed"]
            )
    west = Eggnemy(
                0,
                test_settings["world_height"]//2,
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"],
                0,
                test_settings["eggnemy_initial_speed"]
            )
    model.normal_eggnemies = [north, south, east, west]

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
    test_settings["eggnemy_initial_speed"] = 1
    model = GameModel(test_settings)

    north_east = Eggnemy(
                test_settings["world_width"],
                0,
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"],
                0,
                test_settings["eggnemy_initial_speed"]
            )
    north_west = Eggnemy(
                0,
                0,
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"],
                0,
                test_settings["eggnemy_initial_speed"]
            )
    south_east = Eggnemy(
                test_settings["world_width"],
                test_settings["world_height"],
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"],
                0,
                test_settings["eggnemy_initial_speed"]
            )
    south_west = Eggnemy(
                0,
                test_settings["world_height"],
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                test_settings["eggnemy_initial_hp"],
                0,
                test_settings["eggnemy_initial_speed"]
            )
    model.normal_eggnemies = [north_east, north_west, south_east, south_west]
    
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
    test_settings = settings
    test_settings["eggnemy_count"] = 0
    model = GameModel(test_settings)

    # Place one enemy overlapping the egg
    enemy = Eggnemy(
        model.egg.x,
        model.egg.y,
        test_settings["eggnemy_width"],
        test_settings["eggnemy_height"],
        test_settings["eggnemy_initial_hp"],
        2,  # damage per hit
        test_settings["eggnemy_initial_speed"]
    )
    model.normal_eggnemies = [enemy]

    initial_hp = model.egg.hp

    # First update should cause damage
    model.update(False, False, False, False, False, False)
    assert model.egg.hp == initial_hp - 2
    first_i_frame = model.i_frame
    assert first_i_frame == model.fps - 1 # 1 frame has passed

    # Damage is not dealt due to i_frame
    model.update(False, False, False, False, False, False)
    assert model.egg.hp == initial_hp - 2
    assert model.i_frame == first_i_frame - 1

    # Update until i_frame = 0
    for _ in range(first_i_frame - 1):
        model.update(False, False, False, False, False, False)

    # i_frame should be 0 again
    assert model.i_frame == 0

    # Second update, enemy deals damage
    model.update(False, False, False, False, False, False)
    assert model.egg.hp == initial_hp - 4
    assert model.i_frame == model.fps - 1

def test_damage_done_by_egg_simple():
    test_settings = settings
    test_settings["eggnemy_count"] = 0
    model = GameModel(test_settings)

    enemy = Eggnemy(
        model.egg.x,
        model.egg.y,
        test_settings["eggnemy_width"],
        test_settings["eggnemy_height"],
        1,  # 1 hit kill
        test_settings["eggnemy_initial_attack"],
        test_settings["eggnemy_initial_speed"]
    )
    model.normal_eggnemies = [enemy]
    assert len(model.normal_eggnemies) == 1

    model.egg.set_attack(1)
    model.attack()

    assert len(model.normal_eggnemies) == 0

    # Eggnemy in range
    enemy1 = Eggnemy(
        model.egg.x,
        model.egg.y,
        test_settings["eggnemy_width"],
        test_settings["eggnemy_height"],
        2,  # 2 hit kill
        test_settings["eggnemy_initial_attack"],
        test_settings["eggnemy_initial_speed"]
    )
    # Eggnemy out of range
    enemy2 = Eggnemy(
        model.egg.x + egg_range,
        model.egg.y + egg_range + model.egg.bottom,
        test_settings["eggnemy_width"],
        test_settings["eggnemy_height"],
        2,  # 2 hit kill
        test_settings["eggnemy_initial_attack"],
        test_settings["eggnemy_initial_speed"]
    )
    model.normal_eggnemies = [enemy1, enemy2]
    assert model.normal_eggnemies == [enemy1, enemy2]
    
    model.egg.set_attack(settings["egg_initial_attack"])
    model.attack()
    assert enemy1.hp == 1
    assert model.normal_eggnemies == [enemy1, enemy2]
    assert enemy2.hp == 2 # fails

    model.attack()
    # enemy1 is killed, enemy2 is not killed
    assert model.normal_eggnemies == [enemy2]
    assert enemy1.hp == 0
    assert enemy2.hp == 2 # fails

def test_removal_when_enemy_dies():
    test_settings = settings
    test_settings["eggnemy_count"] = 0
    model = GameModel(test_settings)

    enemy = Eggnemy(
        model.egg.x,
        model.egg.y,
        test_settings["eggnemy_width"],
        test_settings["eggnemy_height"],
        1,  # 1 hit kill
        test_settings["eggnemy_initial_attack"],
        test_settings["eggnemy_initial_speed"]
    )
    model.normal_eggnemies = [enemy]
    assert len(model.normal_eggnemies) == 1

    model.egg.set_attack(1)
    model.attack()

    assert len(model.normal_eggnemies) == 0

    # Eggnemy in range
    enemy1 = Eggnemy(
        model.egg.x,
        model.egg.y,
        test_settings["eggnemy_width"],
        test_settings["eggnemy_height"],
        1,  # 1 hit kill
        test_settings["eggnemy_initial_attack"],
        test_settings["eggnemy_initial_speed"]
    )
    # Eggnemy out of range
    enemy2 = Eggnemy(
        model.egg.x + egg_range,
        model.egg.y + egg_range,
        test_settings["eggnemy_width"],
        test_settings["eggnemy_height"],
        1,  # 1 hit kill
        test_settings["eggnemy_initial_attack"],
        test_settings["eggnemy_initial_speed"]
    )
    model.normal_eggnemies = [enemy1, enemy2]
    assert len(model.normal_eggnemies) == 2
    
    model.egg.set_attack(settings["egg_initial_attack"])
    model.attack()

    # enemy1 is killed, enemy2 is not killed
    assert model.normal_eggnemies == [enemy2]
    assert len(model.normal_eggnemies) == 1


def test_restart():
    model = GameModel(settings)
    # Simulate ongoing game where egg is not dead
    model.egg.hp = 1
    model.total_frames_passed = 210
    model.eggnemies_defeated = 2
    # 1 tick
    model.update(False, False, False, False, False, False)
    # 2nd tick
    model.update(False, False, False, False, False, True)
    # Game should not have been restarted because egg is not dead
    assert model.egg.hp == 1
    # 2 frames have passed because of 2 updates
    assert model.total_frames_passed == 212
    # Eggnemies defeated remains the same
    assert model.eggnemies_defeated == 2

    # Egg is dead
    model.egg.hp = 0
    # Next frame, egg should be dead and model._game_over_loss = True
    model.update(False, False, False, False, False, False)
    # R is pressed
    model.update(False, False, False, False, False, True)

    # Game has been restarted => egg's hp returns to initial hp
    assert model.egg.hp == settings["egg_initial_hp"]
    # Timer is reset to 0
    assert model.total_frames_passed == 0
    # Enemies defeated reset to 0
    assert model.eggnemies_defeated == 0

def test_leaderboard():
    model = GameModel(settings)
    scores = [300, 150, 600, 450]

    # Create initial sample leaderboard
    for score in scores:
        model.add_to_leaderboard(score)
    assert model.leaderboard == [600, 450, 300]

    # New highest score
    model.add_to_leaderboard(700)
    assert model.leaderboard == [700, 600, 450]

    # New 2nd best score
    model.add_to_leaderboard(680)
    assert model.leaderboard == [700, 680, 600]

    # New 3rd best score
    model.add_to_leaderboard(620)
    assert model.leaderboard == [700, 680, 620]

    # New score but not > current 3 best scores
    model.add_to_leaderboard(450)
    assert model.leaderboard == [700, 680, 620]
