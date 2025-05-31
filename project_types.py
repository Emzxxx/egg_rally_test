from typing import Protocol


class UpdateHandler(Protocol):
    def update(self) -> None: ...


class DrawHandler(Protocol):
    def draw(self) -> None: ...

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
    def hp(self) -> int:
        ...

    @property
    def max_hp(self) -> int:
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
    def attack_stat(self) -> int:
        ...

    @property
    def speed(self) -> int:
        ...

    @property
    def eggxperience(self) -> int:
        ...