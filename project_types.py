from typing import Protocol


class UpdateHandler(Protocol):
    def update(self) -> None: ...


class DrawHandler(Protocol):
    def draw(self) -> None: ...

class EggInfo(Protocol):
    @property
    def x(self) -> int:
        ...

    @property
    def y(self) -> int:
        ...

    @property
    def width(self) -> int:
        ...

    @property
    def height(self) -> int:
        ...

    @property
    def hp(self) -> int:
        ...

    @property
    def max_hp(self) -> int:
        ...

    @property
    def top(self) -> int:
        ...

    @property
    def bottom(self) -> int:
        ...

    @property
    def left(self) -> int:
        ...

    @property
    def right(self) -> int:
        ...