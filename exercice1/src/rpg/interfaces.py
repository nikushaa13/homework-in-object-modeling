from abc import ABC, abstractmethod


class ICombatUnit(ABC):
    @abstractmethod
    def move(self, x: int, y: int) -> None:
        pass

    @abstractmethod
    def rest(self, d: int) -> None:
        pass

    @abstractmethod
    def display(self) -> str:
        pass

    @abstractmethod
    def attack(self, target: "ICombatUnit") -> None:
        pass

    @abstractmethod
    def take_damage(self, i: int) -> None:
        pass