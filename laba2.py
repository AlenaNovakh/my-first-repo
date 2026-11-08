from abc import ABC, abstractmethod

class Attacker(ABC):
    @abstractmethod
    def attack(self, unit):
        pass

class Moveable(ABC):
    @abstractmethod
    def move(self, x, y):
        pass

class GameObject:
    def __init__(self, id, name, x, y):
        self._id = id
        self._name = name
        self._x = x
        self._y = y

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

class Unit(GameObject):
    def __init__(self, id, name, x, y, hp):
        super().__init__(id, name, x, y)
        self._hp = hp
        self._alive = True

    def is_alive(self):
        return self._alive

    def get_hp(self):
        return self._hp

    def receive_damage(self, damage):
        self._hp -= damage
        if self._hp <= 0:
            self._hp = 0
            self._alive = False

class Archer(Unit, Attacker, Moveable):
    def __init__(self, id, name, x, y, hp, damage):
        super().__init__(id, name, x, y, hp)
        self._damage = damage

    def attack(self, unit):
        if self.is_alive():
            unit.receive_damage(self._damage)

    def move(self, x, y):
        if self.is_alive():
            self._x = x
            self._y = y

class Building(GameObject):
    def __init__(self, id, name, x, y):
        super().__init__(id, name, x, y)
        self._built = False

    def is_built(self):
        return self._built

class Fort(Building, Attacker):
    def __init__(self, id, name, x, y, damage=0):
        super().__init__(id, name, x, y)
        self._damage = damage

    def attack(self, unit):
        if self.is_built():
            unit.receive_damage(self._damage)

class MobileHouse(Building, Moveable):
    def move(self, x, y):
        if self.is_built():
            self._x = x
            self._y = y