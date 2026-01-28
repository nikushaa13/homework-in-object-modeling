from typing import List

from .group import CombatGroup
from .interfaces import ICombatUnit
from .units import Spy, Warrior, Wizard


class Commander:
    def __init__(self) -> None:
        self._units: List[ICombatUnit] = []

    def create_warrior(self) -> Warrior:
        unit = Warrior()
        self._units.append(unit)
        return unit

    def create_spy(self) -> Spy:
        unit = Spy()
        self._units.append(unit)
        return unit

    def create_wizard(self) -> Wizard:
        unit = Wizard()
        self._units.append(unit)
        return unit

    def create_group(self) -> CombatGroup:
        grp = CombatGroup()
        self._units.append(grp)
        return grp

    def units(self) -> List[ICombatUnit]:
        return list(self._units)