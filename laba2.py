from abc import ABC, abstractmethod

class Attacker(ABC):
    @abstractmethod
    def attack(self, unit):
        pass

class Moveable(ABC):
    @abstractmethod
    def move(self, x, y):
        pass

class GameObject(ABC):
    def __init__(self, id: int, name: str, x: int, y: int):
        self._id = id
        self._name = name
        self._x = x
        self._y = y

    def getId(self) -> int:
        return self._id

    def getName(self) -> str:
        return self._name

    def getX(self) -> int:
        return self._x

    def getY(self) -> int:
        return self._y

class Unit(GameObject):
    def __init__(self, id: int, name: str, x: int, y: int, hp: float):
        super().__init__(id, name, x, y)
        self._hp = hp
        self._alive = True

    def isAlive(self) -> bool:
        return self._alive

    def getHp(self) -> float:
        return self._hp

    def receiveDamage(self, damage: float):
        if not self._alive:
            return
        self._hp = max(0.0, self._hp - damage)
        if self._hp == 0.0:
            self._alive = False

class Archer(Unit, Attacker, Moveable):
    def __init__(self, id: int, name: str, x: int, y: int, hp: float, damage: float):
        super().__init__(id, name, x, y, hp)
        self._damage = damage

    def attack(self, unit: Unit):
        if self.isAlive() and unit.isAlive():
            unit.receiveDamage(self._damage)

    def move(self, x: int, y: int):
        if self.isAlive():
            self._x = x
            self._y = y

class Building(GameObject):
    def __init__(self, id: int, name: str, x: int, y: int, built: bool = False):
        super().__init__(id, name, x, y)
        self._built = built

    def isBuilt(self) -> bool:
        return self._built

    def build(self):
        self._built = True

class Fort(Building, Attacker):
    def __init__(self, id: int, name: str, x: int, y: int, damage: float, built: bool = False):
        super().__init__(id, name, x, y, built)
        self._damage = damage

    def attack(self, unit: Unit):
        if self.isBuilt() and unit.isAlive():
            unit.receiveDamage(self._damage)

class MobileHouse(Building, Moveable):
    def move(self, x: int, y: int):
        if self.isBuilt():
            self._x = x
            self._y = y
