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