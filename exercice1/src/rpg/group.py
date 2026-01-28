from typing import List

from .interfaces import ICombatUnit


class CombatGroup(ICombatUnit):
    def __init__(self) -> None:
        self._children: List[ICombatUnit] = []

    def add(self, unit: ICombatUnit) -> None:
        self._children.append(unit)

    def remove(self, unit: ICombatUnit) -> None:
        self._children.remove(unit)

    def move(self, x: int, y: int) -> None:
        for unit in self._children:
            unit.move(x, y)

    def rest(self, d: int) -> None:
        for unit in self._children:
            unit.rest(d)

    def take_damage(self, i: int) -> None:
        if not self._children:
            return
        share = i // len(self._children)
        for unit in self._children:
            unit.take_damage(share)

    def display(self) -> str:
        return "[" + ", ".join(unit.display() for unit in self._children) + "]"

    def attack(self, target: ICombatUnit) -> None:
        for unit in self._children:
            unit.attack(target)