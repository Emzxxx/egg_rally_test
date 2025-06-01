from typing import Protocol
from abc import ABC

class UpdateHandler(Protocol):
    def update(self) -> None: ...


class DrawHandler(Protocol):
    def draw(self) -> None: ...

class Egg:
    def __init__(self, x: float, 
                 y: float, 
                 width: float, 
                 height: float, 
                 hp: float,
                 initial_attack: float,
                 initial_speed: float):
        self.x = x
        self.y = y
        self.relative_x = x
        self.relative_y = y
        self.width = width
        self.height = height
        self.max_hp = hp
        self.hp = hp
        self._attack_stat = initial_attack
        self._speed = initial_speed
        self.eggxperience = 0

    def set_speed(self, new_speed: int):
        self._speed = new_speed

    def set_attack(self, new_attack: int):
        self._attack_stat = new_attack

    @property
    def top(self) -> float:
        return self.y

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.x + self.width
    
    @property
    def speed(self):
        return self._speed
    
    @property
    def attack_stat(self):
        return self._attack_stat

    @property
    def center(self) -> tuple[float, float]:
        return (self.x + self.width / 2, self.y + self.height / 2)


class Eggnemy_Template(ABC):
    '''
    One Abstract Class only for both normal eggnemies and bosses since bosses are just eggnemies that are a little different
    Additionally, this is also more compact

    If a boss ever really does something unique only to itself, it wouldn't be too hard to make an interface specific to the boss and its
    unique attributes and skills

    '''
    def __init__(self, x: float, 
                 y: float, 
                 width: float, 
                 height: float, 
                 hp: float,
                 initial_attack: float,
                 initial_speed: float):
        self.x = x
        self.y = y
        self.relative_x = x
        self.relative_y = y
        self.width = width
        self.height = height
        self.max_hp = hp
        self.hp = hp
        self._attack_stat = initial_attack
        self._speed = initial_speed

    @property
    def top(self) -> float:
        return self.y

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def left(self) -> float:
        return self.x

    @property
    def right(self) -> float:
        return self.x + self.width
    
    @property
    def speed(self):
        return self._speed
    
    @property
    def attack_stat(self):
        return self._attack_stat

    @property
    def center(self) -> tuple[float, float]:
        return (self.x + self.width / 2, self.y + self.height / 2)

class Eggnemy(Eggnemy_Template):
    #Nothing really different happens in the class itslef, moreso in the stats that get passed to it so empty for now
    ...
class Boss(Eggnemy_Template):
    #Nothing really different happens in the class itslef, moreso in the stats that get passed to it so empty for now
    ...

class Eggnemy_Spawner_Interface(Protocol):
    #Same idea for both normal eggnemy and boss, you want a spawner
    def spawn_eggnemy(self, x: float, y: float, width: float, height: float, hp: int, initial_attack: int, initial_speed: int) -> Eggnemy_Template:
        ...
class Boss_Spawner_Interface(Protocol):
    #Same idea for both normal eggnemy and boss, you want a spawner
    def spawn_boss(self, x: float, y: float, width: float, height: float, hp: int, initial_attack: int, initial_speed: int) -> Eggnemy_Template:
        ...


class Eggnemy_Spawner(Eggnemy_Spawner_Interface):
    def spawn_eggnemy(self, x: float, y: float, width: float, height: float, hp: int, initial_attack: int, initial_speed: int):
        return Eggnemy(x, y, width, height, hp, initial_attack, initial_speed)

class Boss_Spawner(Boss_Spawner_Interface):
    def spawn_boss(self, x: float, y: float, width: float, height: float, hp: int, initial_attack: int, initial_speed: int):
        return Boss(x, y, width, height, hp, initial_attack, initial_speed)



class EggInfo(Protocol):
    @property
    def x(self) -> float:
        ...

    @property
    def y(self) -> float:
        ...

    @property
    def width(self) -> float:
        ...

    @property
    def height(self) -> float:
        ...

    @property
    def hp(self) -> float:
        ...

    @property
    def max_hp(self) -> float:
        ...

    @property
    def top(self) -> float:
        ...

    @property
    def bottom(self) -> float:
        ...

    @property
    def left(self) -> float:
        ...

    @property
    def right(self) -> float:
        ...

    @property
    def center(self) -> tuple[float, float]:
        ...

    @property
    def attack_stat(self) -> float:
        ...

    @property
    def speed(self) -> float:
        ...

    @property
    def eggxperience(self) -> int:
        ...







# class Boss_Template(ABC):
#     def __init__(self, 
#                  x: float, 
#                  y: float, 
#                  width: float, 
#                  height: float, 
#                  hp: int,
#                  initial_attack: int,
#                  initial_speed: int):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.max_hp = hp
#         self.hp = hp
#         self._attack_stat = initial_attack
#         self._speed = initial_speed

#     @property
#     def top(self) -> float:
#         return self.y

#     @property
#     def bottom(self) -> float:
#         return self.y + self.height

#     @property
#     def left(self) -> float:
#         return self.x

#     @property
#     def right(self) -> float:
#         return self.x + self.width
    
#     @property
#     def speed(self):
#         return self._speed
    
#     @property
#     def attack_stat(self):
#         return self._attack_stat

#     @property
#     def center(self) -> tuple[float, float]:
#         return (self.x + self.width / 2, self.y + self.height / 2)
    
#     @abstractmethod
#     def spawn_boss(self,
#                     x: float, 
#                     y: float, 
#                     width: float, 
#                     height: float, 
#                     hp: int,
#                     initial_attack: int,
#                     initial_speed: int):
#         ...