from model import GameModel, Eggnemy
from typing import Any
import json

'''
    Unit Testing
    
    Note: Any setting important has to be set in the function itself in case the settings get messed up at any point
'''


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

def test_egg_movement():
    #testing the max min jazz n stuff of the movemebt

    #normal cases:
    #from the center move like 3 to each direction then check if tama na
    #make sure to set the egg speed 
    #separate the directions

    #Edge cases: 
    #Egg at east, west, north, south, NE, NW, SE, SW
    #update/move once then no more

    ...

def test_collision_egg_eggnemy():
    #lots of eggnemies, have it check if eggnemies are in collision w egg or not

    #not in range 5 examples
    '''
    2 pixel away from being at the edge
    2 at random areas 

    '''

    #in range 
    '''
    4 edge to edge (1 per edge)
    4 corner to corner (1 per corner)
    3 intersecting
    1 direectly on it
    '''
    ...

def test_in_range():
    #lots of eggnemies, have it check if eggnemies are in range or not

    #not in range 5 examples
    '''
    2 pixel away from being at the edge
    2 at random areas 

    '''

    #in range 
    '''
    4 edge to edge (1 per edge)
    4 corner to corner (1 per corner)
    3 in range but not in contact
    2 intersecting w egg
    1 direectly on egg
    '''
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

def test_next_wave_eggnemy_stats():
    #play with wave counts and stat count of enemy with a preset stat increase set here
    ...

def test_shift_enemies_normal():
    '''
    All directions put in one test function for compactness

    Could theoretically separate each direction with its own eggnemies setup
    '''

    test_settings = settings
    test_settings["eggnemy_count"] = 0 #To make it as isolated as possible, chance to randomly kill a stray egg to skew tests
    test_settings["egg_initial_speed"] = 2

    model = GameModel(test_settings)

    #Setup enemies
    north = Eggnemy(
            test_settings["world_width"]//2,
            0,
            test_settings["world_height"],
            test_settings["world_height"],
            1, 0, 0
                )
    south = Eggnemy(
                test_settings["world_width"]//2,
                test_settings["world_height"],
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                1, 0, 0
            )
    east = Eggnemy(
                test_settings["world_width"],
                test_settings["world_height"]//2,
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                1, 0, 0
            )
    west = Eggnemy(
                0,
                test_settings["world_height"]//2,
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                1, 0, 0
            )
    north_east = Eggnemy(
                test_settings["world_width"],
                0,
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                1, 0, 0
            )
    north_west = Eggnemy(
                0,
                0,
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                1, 0, 0
            )
    south_east = Eggnemy(
                test_settings["world_width"],
                test_settings["world_height"],
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                1, 0, 0
            )
    south_west = Eggnemy(
                0,
                test_settings["world_height"],
                test_settings["eggnemy_width"],
                test_settings["eggnemy_height"],
                1, 0, 0
            )

    local_eggnemies = [north, south, east, west, north_east, north_west, south_east, south_west]
    model.normal_eggnemies = local_eggnemies
    
    '''
        TEST SHIFTING TO THE LEFT
    '''
    model.shift_enemies("left")

    assert north.x == test_settings["world_width"]//2 - 2
    assert north.y == 0

    assert south.x == test_settings["world_width"]//2 - 2
    assert south.y == test_settings["world_height"]
                
    assert east.x == test_settings["world_width"] - 2
    assert east.y == test_settings["world_height"]//2

    assert west.x == - 2 #Out of the screen
    assert west.y == test_settings["world_height"]//2


    assert north_east.x == test_settings["world_width"] - 2
    assert north_east.y == 0

    assert north_west.x == - 2
    assert north_west.y == 0

    assert south_east.x == test_settings["world_width"] - 2
    assert south_east.y == test_settings["world_height"]

    assert south_west.x == - 2
    assert south_west.y == test_settings["world_height"]

    #shift left 2 more times, 3 total
    model.shift_enemies("left")
    model.shift_enemies("left")
    
    assert north.x == test_settings["world_width"]//2 - 6
    assert north.y == 0

    assert south.x == test_settings["world_width"]//2 - 6
    assert south.y == test_settings["world_height"]
                
    assert east.x == test_settings["world_width"] - 6
    assert east.y == test_settings["world_height"]//2

    assert west.x == - 6
    assert west.y == test_settings["world_height"]//2


    assert north_east.x == test_settings["world_width"] - 6
    assert north_east.y == 0

    assert north_west.x == - 6
    assert north_west.y == 0

    assert south_east.x == test_settings["world_width"] - 6
    assert south_east.y == test_settings["world_height"]

    assert south_west.x == - 6
    assert south_west.y == test_settings["world_height"]

    '''
        TEST SHIFTING TO THE RIGHT
    '''
    model.shift_enemies("right")

    assert north.x == test_settings["world_width"]//2 - 4
    assert north.y == 0

    assert south.x == test_settings["world_width"]//2 - 4
    assert south.y == test_settings["world_height"]
                
    assert east.x == test_settings["world_width"] - 4
    assert east.y == test_settings["world_height"]//2

    assert west.x == - 2
    assert west.y == test_settings["world_height"]//2


    assert north_east.x == test_settings["world_width"] - 4
    assert north_east.y == 0

    assert north_west.x == - 4
    assert north_west.y == 0

    assert south_east.x == test_settings["world_width"] - 4
    assert south_east.y == test_settings["world_height"]

    assert south_west.x == - 4
    assert south_west.y == test_settings["world_height"]

    #shift right 3 more times, 4 total
    model.shift_enemies("right")
    model.shift_enemies("right")
    
    assert north.x == test_settings["world_width"]//2 + 2
    assert north.y == 0

    assert south.x == test_settings["world_width"]//2 + 2
    assert south.y == test_settings["world_height"]
                
    assert east.x == test_settings["world_width"] + 2
    assert east.y == test_settings["world_height"]//2

    assert west.x == 2 #Back into the screen
    assert west.y == test_settings["world_height"]//2


    assert north_east.x == test_settings["world_width"] + 2
    assert north_east.y == 0

    assert north_west.x == 2
    assert north_west.y == 0

    assert south_east.x == test_settings["world_width"] + 2
    assert south_east.y == test_settings["world_height"]

    assert south_west.x == 2
    assert south_west.y == test_settings["world_height"]
    
def test_shift_enemies_at_edge():
    #the above but relative x and relative y change to specifically target the failing conditions of the function
    ...
    
def test_egghancements():
    test_settings = settings
    test_settings["eggnemy_count"] = 0 #To make it as isolated as possible, chance to randomly kill a stray egg to skew tests
    test_settings["egg_initial_hp"] = 10
    test_settings["egg_initial_attack"] = 1
    test_settings["egg_initial_speed"] = 2
    test_settings["hp_incr"] = 5
    test_settings["attack_incr"] = 1
    test_settings["speed_incr"] = 1

    model = GameModel(test_settings)
    egg = model.egg
    #At the start
    assert egg.max_hp == 10
    assert egg.attack_stat == 1
    assert egg.speed == 2

    #Choose 1 (increase hp)
    model.apply_egghancement(1)
    assert egg.max_hp == 15
    assert egg.attack_stat == 1
    assert egg.speed == 2

    #Choose 1 (increase hp), 3 more times [total of 4]
    for _ in range(3):
        model.apply_egghancement(1)
    assert egg.max_hp == 30
    assert egg.attack_stat == 1
    assert egg.speed == 2

    #Choose 2 (increase attack)
    model.apply_egghancement(2)
    assert egg.max_hp == 30
    assert egg.attack_stat == 2
    assert egg.speed == 2

    #Choose 2 (increase attack), 3 more times [total of 4]
    for _ in range(3):
        model.apply_egghancement(2)
    assert egg.max_hp == 30
    assert egg.attack_stat == 5
    assert egg.speed == 2

    #Choose 3 (increase speed)
    model.apply_egghancement(3)
    assert egg.max_hp == 30
    assert egg.attack_stat == 5
    assert egg.speed == 3

    #Choose 3 (increase speed), 3 more times [total of 4]
    for _ in range(3):
        model.apply_egghancement(3)
    assert egg.max_hp == 30
    assert egg.attack_stat == 5
    assert egg.speed == 6


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
    ...

def test_damage_done_by_egg_simple():
    ...

def test_removal_when_enemy_dies():
    ...


def test_restart():
    ...

def test_leaderboard():
    ...


