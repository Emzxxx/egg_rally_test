from model import GameModel, Eggnemy
from typing import Any
import json

'''
    Unit Testing
    
    Note: Any setting important has to be set in the function itself in case the settings get messed up at any point
'''


#Import settings for tests, usually only really works if in its base settings
with open("settings.json") as f:
    settings: dict[str, Any] = json.load(f)

#To make it concrete
settings["world_width"] = 256
settings["world_height"] = 256

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
    model = GameModel(settings)
    egg = model.egg
    egg.set_speed(3)

    center_x = settings["world_width"] // 2
    center_y = settings["world_height"] // 2

    # Move Left
    egg.relative_x = center_x
    model.update(True, False, False, False, False, False)
    assert egg.relative_x == center_x - 3

    # Move Right
    egg.relative_x = center_x
    model.update(False, True, False, False, False, False)
    assert egg.relative_x == center_x + 3

    # Move Up
    egg.relative_y = center_y
    model.update(False, False, True, False, False, False)
    assert egg.relative_y == center_y - 3

    # Move Down
    egg.relative_y = center_y
    model.update(False, False, False, True, False, False)
    assert egg.relative_y == center_y + 3

    # Edge case: West boundary
    egg.relative_x = 0
    model.update(True, False, False, False, False, False)
    assert egg.relative_x == 0

    # Edge case: East boundary
    egg.relative_x = settings["world_width"] - egg.width
    model.update(False, True, False, False, False, False)
    assert egg.relative_x == settings["world_width"] - egg.width

    # Edge case: North boundary
    egg.relative_y = 0
    model.update(False, False, True, False, False, False)
    assert egg.relative_y == 0

    # Edge case: South boundary
    egg.relative_y = settings["world_height"] - egg.height
    model.update(False, False, False, True, False, False)
    assert egg.relative_y == settings["world_height"] - egg.height

    # Edge case: NW corner
    egg.relative_x = 0
    egg.relative_y = 0
    model.update(True, False, True, False, False, False)
    assert egg.relative_x == 0
    assert egg.relative_y == 0

    # Edge case: NE corner
    egg.relative_x = settings["world_width"] - egg.width
    egg.relative_y = 0
    model.update(False, True, True, False, False, False)
    assert egg.relative_x == settings["world_width"] - egg.width
    assert egg.relative_y == 0

    # Edge case: SW corner
    egg.relative_x = 0
    egg.relative_y = settings["world_height"] - egg.height
    model.update(True, False, False, True, False, False)
    assert egg.relative_x == 0
    assert egg.relative_y == settings["world_height"] - egg.height

    # Edge case: SE corner
    egg.relative_x = settings["world_width"] - egg.width
    egg.relative_y = settings["world_height"] - egg.height
    model.update(False, True, False, True, False, False)
    assert egg.relative_x == settings["world_width"] - egg.width
    assert egg.relative_y == settings["world_height"] - egg.height

def test_collision_egg_eggnemy():
    model = GameModel(settings)
    egg = model.egg

    # Not in collision
    not_colliding = [
        Eggnemy(egg.x - egg.width - 2, 
                egg.y, 
                16, 
                16, 
                1, 
                1, 
                1),  # left
        Eggnemy(egg.x + egg.width + 2, 
                egg.y, 
                16, 
                16, 
                1, 
                1, 
                1),  # right
        Eggnemy(egg.x, 
                egg.y - egg.height - 2, 
                16, 
                16, 
                1, 
                1, 
                1),  # above
        Eggnemy(egg.x, 
                egg.y + egg.height + 2, 
                16, 
                16, 
                1, 
                1, 
                1),  # below
        Eggnemy(0, 
                0, 
                16, 
                16, 
                1, 
                1, 
                1),  # random far corner
    ]
    for enemy in not_colliding:
        assert not model.is_in_collision(enemy)

    # Edge-to-edge collision
    colliding = [
        Eggnemy(egg.x - 16, 
                egg.y, 16, 
                16, 
                1, 
                1, 
                1),  # left edge
        Eggnemy(egg.x + egg.width - 1, 
                egg.y, 
                16, 
                16, 
                1, 
                1, 
                1),  # right edge
        Eggnemy(egg.x, 
                egg.y - 16, 
                16, 
                16, 
                1, 
                1, 
                1),  # top edge
        Eggnemy(egg.x, 
                egg.y + egg.height - 1, 
                16, 
                16, 
                1, 
                1, 
                1),  # bottom edge
        Eggnemy(egg.x, 
                egg.y, 
                egg.width, egg.height, 1, 1, 1),  # full overlap
        Eggnemy(egg.x + 4, 
                egg.y + 4, 
                16, 
                16, 
                1, 
                1, 
                1),  # corner overlap
        Eggnemy(egg.x - 8, 
                egg.y - 8, 
                16, 
                16, 
                1, 
                1, 
                1),  # corner intersect
        Eggnemy(egg.x + 8, 
                egg.y + 8, 
                16, 
                16, 
                1, 
                1, 
                1),  # opposite corner intersect
    ]
    for enemy in colliding:
        assert model.is_in_collision(enemy)


def test_in_range():
    model = GameModel(settings)
    egg = model.egg
    r = model.egg_range

    # Not in range
    not_in_range = [
        Eggnemy(egg.x - r - 17, 
                egg.y, 
                16, 
                16, 
                1, 
                1, 
                1), # left, outside attack range
        Eggnemy(egg.x + egg.width + r + 1, 
                egg.y, 
                16, 
                16, 
                1, 
                1, 
                1), # above, outside attack range
        Eggnemy(egg.x, # right, outside attack range
                egg.y - r - 17, 
                16, 
                16, 
                1, 
                1, 
                1),
        Eggnemy(egg.x, 
                egg.y + egg.height + r + 1, 
                16, 
                16, 
                1, 
                1, 
                1), # below, outside attack range
        Eggnemy(0, 
                0, 
                16, 
                16, 
                1, 
                1, 
                1), # top left corner of map
    ]
    for enemy in not_in_range:
        assert not model.is_in_range(enemy)

    # In range
    in_range = [
        Eggnemy(egg.x - r, 
                egg.y, 
                16, 
                16, 
                1, 
                1, 
                1), # touching left edge of attack range
        Eggnemy(egg.x + egg.width + r - 1, 
                egg.y, 
                16, 
                16, 
                1, 
                1, 
                1), # touching right edge of attack range
        Eggnemy(egg.x, 
                egg.y - r, 
                16, 
                16, 
                1, 
                1, 
                1), # touching top edge of attack range
        Eggnemy(egg.x, 
                egg.y + egg.height + r - 1, 
                16, 
                16, 
                1, 
                1, 
                1), # touching bottom edge of attack range
        Eggnemy(egg.x, 
                egg.y, 
                egg.width, 
                egg.height, 
                1, 
                1, 
                1), # fully overlapping with egg
        Eggnemy(egg.x + 4, 
                egg.y + 4, 
                16, 
                16, 
                1, 
                1, 
                1), # slightly inside bottom-right quadrant of egg
        Eggnemy(egg.x - 8, 
                egg.y - 8, 
                16, 
                16, 
                1, 
                1, 
                1), # slightly inside top-left quadrant of egg
        Eggnemy(egg.x + 8, 
                egg.y + 8, 
                16, 
                16, 
                1, 
                1, 
                1), # deeper into bottom-right of egg
        Eggnemy(egg.x - 1, 
                egg.y - 1, 
                16, 
                16, 
                1, 
                1, 
                1), # 1 pixel to the top-left of egg
        Eggnemy(egg.x + 1, 
                egg.y + 1, 
                16, 
                16, 
                1, 
                1, 
                1), # 1 pixel to the bottom-right of egg
    ]
    for enemy in in_range:
        assert model.is_in_range(enemy)


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
    # Reduce count for isolation
    settings["eggnemy_count"] = 1  
    model = GameModel(settings)

    base_hp = settings["eggnemy_initial_hp"]
    base_attack = settings["eggnemy_initial_attack"]
    base_speed = settings["eggnemy_initial_speed"]

    hp_incr = settings["eggnemy_wave_increment_hp"]
    atk_incr = settings["eggnemy_wave_increment_attack"]
    spd_incr = settings["eggnemy_wave_increment_speed"]

    for wave in range(5):
        model.normal_eggnemies = []
        model.spawn_enemies()

        enemy = model.normal_eggnemies[0]
        assert enemy.hp == base_hp + hp_incr * wave
        assert enemy.attack_stat == base_attack + atk_incr * wave
        assert enemy.speed == base_speed + spd_incr * wave

        model.normal_eggnemies = []
        model.next_wave()

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

    assert west.x == - 4
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

    '''
        TEST SHIFTING UPWARDS 
    '''
    model.shift_enemies("up")

    assert north.x == test_settings["world_width"]//2 + 2
    assert north.y == - 2

    assert south.x == test_settings["world_width"]//2 + 2
    assert south.y == test_settings["world_height"] - 2
                
    assert east.x == test_settings["world_width"] + 2
    assert east.y == test_settings["world_height"]//2 - 2

    assert west.x == 2 
    assert west.y == test_settings["world_height"]//2 - 2


    assert north_east.x == test_settings["world_width"] + 2
    assert north_east.y == - 2

    assert north_west.x == 2
    assert north_west.y == - 2

    assert south_east.x == test_settings["world_width"] + 2
    assert south_east.y == test_settings["world_height"] - 2

    assert south_west.x == 2
    assert south_west.y == test_settings["world_height"] - 2

    #shift up 4 more times, 5 total
    model.shift_enemies("up")
    model.shift_enemies("up")
    model.shift_enemies("up")
    model.shift_enemies("up")

    assert north.x == test_settings["world_width"]//2 + 2
    assert north.y == -10

    assert south.x == test_settings["world_width"]//2 + 2
    assert south.y == test_settings["world_height"] -10
                
    assert east.x == test_settings["world_width"] + 2
    assert east.y == test_settings["world_height"]//2 -10

    assert west.x == 2
    assert west.y == test_settings["world_height"]//2 -10


    assert north_east.x == test_settings["world_width"] + 2
    assert north_east.y == -10

    assert north_west.x == 2
    assert north_west.y == -10

    assert south_east.x == test_settings["world_width"] + 2
    assert south_east.y == test_settings["world_height"] -10

    assert south_west.x == 2
    assert south_west.y == test_settings["world_height"] -10

    '''
        TEST SHIFTING DOWNWARDS 
    '''
    model.shift_enemies("down")

    assert north.x == test_settings["world_width"]//2 + 2
    assert north.y == - 8

    assert south.x == test_settings["world_width"]//2 + 2
    assert south.y == test_settings["world_height"] - 8
                
    assert east.x == test_settings["world_width"] + 2
    assert east.y == test_settings["world_height"]//2 - 8

    assert west.x == 2
    assert west.y == test_settings["world_height"]//2 - 8


    assert north_east.x == test_settings["world_width"] + 2
    assert north_east.y == - 8

    assert north_west.x == 2
    assert north_west.y == - 8

    assert south_east.x == test_settings["world_width"] + 2
    assert south_east.y == test_settings["world_height"] - 8

    assert south_west.x == 2
    assert south_west.y == test_settings["world_height"] - 8

    #shift down 2 more times, 3 total
    model.shift_enemies("down")
    model.shift_enemies("down")

    assert north.x == test_settings["world_width"]//2 + 2
    assert north.y == - 4

    assert south.x == test_settings["world_width"]//2 + 2
    assert south.y == test_settings["world_height"] - 4
                
    assert east.x == test_settings["world_width"] + 2
    assert east.y == test_settings["world_height"]//2 - 4

    assert west.x == 2
    assert west.y == test_settings["world_height"]//2 - 4


    assert north_east.x == test_settings["world_width"] + 2
    assert north_east.y == - 4

    assert north_west.x == 2
    assert north_west.y == - 4

    assert south_east.x == test_settings["world_width"] + 2
    assert south_east.y == test_settings["world_height"] - 4

    assert south_west.x == 2
    assert south_west.y == test_settings["world_height"] - 4


def test_shift_enemies_edges():
    test_settings = settings
    test_settings["eggnemy_count"] = 0 #To make it as isolated as possible, chance to randomly kill a stray egg to skew tests
    test_settings["egg_initial_speed"] = 2

    model = GameModel(test_settings)
    egg = model.egg

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
    

    #Egg at the very right shift left
    egg.relative_x = test_settings["world_width"] - egg.width
    egg.relative_y = test_settings["world_height"]//2

    model.shift_enemies("left")

    assert north.x == test_settings["world_width"]//2  
    assert north.y == 0

    assert south.x == test_settings["world_width"]//2  
    assert south.y == test_settings["world_height"]
                
    assert east.x == test_settings["world_width"]  
    assert east.y == test_settings["world_height"]//2

    assert west.x == 0
    assert west.y == test_settings["world_height"]//2


    assert north_east.x == test_settings["world_width"]  
    assert north_east.y == 0

    assert north_west.x == 0
    assert north_west.y == 0

    assert south_east.x == test_settings["world_width"]  
    assert south_east.y == test_settings["world_height"]

    assert south_west.x == 0
    assert south_west.y == test_settings["world_height"]


    #Egg at the very left shift right
    egg.relative_x = 0 - 2
    egg.relative_y = test_settings["world_height"]//2

    model.shift_enemies("right")

    assert north.x == test_settings["world_width"]//2  
    assert north.y == 0

    assert south.x == test_settings["world_width"]//2  
    assert south.y == test_settings["world_height"]
                
    assert east.x == test_settings["world_width"]  
    assert east.y == test_settings["world_height"]//2

    assert west.x == 0
    assert west.y == test_settings["world_height"]//2


    assert north_east.x == test_settings["world_width"]  
    assert north_east.y == 0

    assert north_west.x == 0
    assert north_west.y == 0

    assert south_east.x == test_settings["world_width"]  
    assert south_east.y == test_settings["world_height"]

    assert south_west.x == 0
    assert south_west.y == test_settings["world_height"]


    #Egg at the very top shift down
    egg.relative_x = test_settings["world_width"]//2
    egg.relative_y = 0

    model.shift_enemies("down")
    assert north.x == test_settings["world_width"]//2  
    assert north.y == 0

    assert south.x == test_settings["world_width"]//2  
    assert south.y == test_settings["world_height"]
                
    assert east.x == test_settings["world_width"]  
    assert east.y == test_settings["world_height"]//2

    assert west.x == 0
    assert west.y == test_settings["world_height"]//2


    assert north_east.x == test_settings["world_width"]  
    assert north_east.y == 0

    assert north_west.x == 0
    assert north_west.y == 0

    assert south_east.x == test_settings["world_width"]  
    assert south_east.y == test_settings["world_height"]

    assert south_west.x == 0
    assert south_west.y == test_settings["world_height"]


    #Egg at the very bottom shift up
    egg.relative_x = test_settings["world_width"]//2
    egg.relative_y = test_settings["world_height"]

    model.shift_enemies("up")
    assert north.x == test_settings["world_width"]//2  
    assert north.y == 0

    assert south.x == test_settings["world_width"]//2  
    assert south.y == test_settings["world_height"]
                
    assert east.x == test_settings["world_width"]  
    assert east.y == test_settings["world_height"]//2

    assert west.x == 0
    assert west.y == test_settings["world_height"]//2


    assert north_east.x == test_settings["world_width"]  
    assert north_east.y == 0

    assert north_west.x == 0
    assert north_west.y == 0

    assert south_east.x == test_settings["world_width"]  
    assert south_east.y == test_settings["world_height"]

    assert south_west.x == 0
    assert south_west.y == test_settings["world_height"]


    #Egg at the very top right shift down and left
    egg.relative_x = test_settings["world_width"] - egg.width
    egg.relative_y = 0

    model.shift_enemies("left")
    model.shift_enemies("down")

    assert north.x == test_settings["world_width"]//2  
    assert north.y == 0

    assert south.x == test_settings["world_width"]//2  
    assert south.y == test_settings["world_height"]
                
    assert east.x == test_settings["world_width"]  
    assert east.y == test_settings["world_height"]//2

    assert west.x == 0
    assert west.y == test_settings["world_height"]//2


    assert north_east.x == test_settings["world_width"]  
    assert north_east.y == 0

    assert north_west.x == 0
    assert north_west.y == 0

    assert south_east.x == test_settings["world_width"]  
    assert south_east.y == test_settings["world_height"]

    assert south_west.x == 0
    assert south_west.y == test_settings["world_height"]


    #Egg at the very top left shift down and right
    egg.relative_x = 0
    egg.relative_y = 0

    model.shift_enemies("right")
    model.shift_enemies("down")

    assert north.x == test_settings["world_width"]//2  
    assert north.y == 0

    assert south.x == test_settings["world_width"]//2  
    assert south.y == test_settings["world_height"]
                
    assert east.x == test_settings["world_width"]  
    assert east.y == test_settings["world_height"]//2

    assert west.x == 0
    assert west.y == test_settings["world_height"]//2


    assert north_east.x == test_settings["world_width"]  
    assert north_east.y == 0

    assert north_west.x == 0
    assert north_west.y == 0

    assert south_east.x == test_settings["world_width"]  
    assert south_east.y == test_settings["world_height"]

    assert south_west.x == 0
    assert south_west.y == test_settings["world_height"]


    #Egg at the very bottom right shift up and left
    egg.relative_x = test_settings["world_width"] - egg.width
    egg.relative_y = test_settings["world_height"]

    model.shift_enemies("up")
    model.shift_enemies("left")
    
    assert north.x == test_settings["world_width"]//2  
    assert north.y == 0

    assert south.x == test_settings["world_width"]//2  
    assert south.y == test_settings["world_height"]
                
    assert east.x == test_settings["world_width"]  
    assert east.y == test_settings["world_height"]//2

    assert west.x == 0
    assert west.y == test_settings["world_height"]//2


    assert north_east.x == test_settings["world_width"]  
    assert north_east.y == 0

    assert north_west.x == 0
    assert north_west.y == 0

    assert south_east.x == test_settings["world_width"]  
    assert south_east.y == test_settings["world_height"]

    assert south_west.x == 0
    assert south_west.y == test_settings["world_height"]

    #Egg at the very bottom left shift up and right
    egg.relative_x = 0
    egg.relative_y = test_settings["world_height"]

    model.shift_enemies("right")
    model.shift_enemies("up")
    
    assert north.x == test_settings["world_width"]//2  
    assert north.y == 0

    assert south.x == test_settings["world_width"]//2  
    assert south.y == test_settings["world_height"]
                
    assert east.x == test_settings["world_width"]  
    assert east.y == test_settings["world_height"]//2

    assert west.x == 0
    assert west.y == test_settings["world_height"]//2


    assert north_east.x == test_settings["world_width"]  
    assert north_east.y == 0

    assert north_west.x == 0
    assert north_west.y == 0

    assert south_east.x == test_settings["world_width"]  
    assert south_east.y == test_settings["world_height"]

    assert south_west.x == 0
    assert south_west.y == test_settings["world_height"]
    

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
Test case no longer applies for phase 6 beyond

def test_win_condition_simple():
    #if boss dead, win condition reached
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
        model.egg.x + model.egg_range,
        model.egg.y + model.egg_range + model.egg.bottom,
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
        model.egg.x + model.egg_range,
        model.egg.y + model.egg_range,
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
