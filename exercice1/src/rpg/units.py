from abc import ABC, abstractmethod
from dataclasses import dataclass

from .interfaces import ICombatUnit


@dataclass
class Position:
    x: int = 0
    y: int = 0


class CombatUnitBase(ICombatUnit, ABC):
    def __init__(self, hp: int = 100, xp: int = 0) -> None:
        self._hp = hp
        self._xp = xp
        self._position = Position()

    @property
    def hp(self) -> int:
        return self._hp

    @property
    def xp(self) -> int:
        return self._xp

    @property
    def position(self) -> Position:
        return self._position

    def rest(self, d: int) -> None:
        if d < 0:
            raise ValueError()
        self._hp += d

    def take_damage(self, i: int) -> None:
        if i < 0:
            raise ValueError()
        self._hp = max(0, self._hp - i)

    @abstractmethod
    def move(self, x: int, y: int) -> None:
        pass

    @abstractmethod
    def display(self) -> str:
        pass

    @abstractmethod
    def attack(self, target: ICombatUnit) -> None:
        pass


class Warrior(CombatUnitBase):
    def move(self, x: int, y: int) -> None:
        self._position = Position(x, y)

    def display(self) -> str:
        return f"Warrior(hp={self._hp}, xp={self._xp}, pos=({self._position.x},{self._position.y}))"

    def attack(self, target: ICombatUnit) -> None:
        target.take_damage(10)
        self._xp += 5


class Spy(CombatUnitBase):
    def move(self, x: int, y: int) -> None:
        self._position = Position(x, y)

    def display(self) -> str:
        return f"Spy(hp={self._hp}, xp={self._xp}, pos=({self._position.x},{self._position.y}))"

    def attack(self, target: ICombatUnit) -> None:
        target.take_damage(6)
        self._xp += 7


class Wizard(CombatUnitBase):
    def move(self, x: int, y: int) -> None:
        self._position = Position(x, y)

    def display(self) -> str:
        return f"Wizard(hp={self._hp}, xp={self._xp}, pos=({self._position.x},{self._position.y}))"

    def attack(self, target: ICombatUnit) -> None:
        target.take_damage(8)
        self._xp += 6