from abc import ABC, abstractmethod


# ==========================================
# 1. SINGLETON (Одиночка)
# Управление единым трекером здоровья собаки
# ==========================================
class DogHealthTracker:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.energy_points = 1000
            cls._instance.is_happy = True
        return cls._instance

    def spend_energy(self, amount: int):
        self.energy_points -= amount
        print(f"[Dog Tracker] Энергия собаки снижена. Остаток: {self.energy_points} ккал.")

    def get_status(self):
        return f"Энергия: {self.energy_points} ккал, Настроение отличное: {self.is_happy}"


# ==========================================
# 2. FACTORY METHOD (Фабричный метод)
# Создание разных видов лакомств для собаки
# ==========================================
class DogTreat(ABC):
    calories = 0

    @abstractmethod
    def give_treat(self):
        pass


class MeatTreat(DogTreat):
    calories = 15

    def give_treat(self):
        print(f"Выдано мясное лакомство (калорийность: {self.calories} ккал)")


class BoneTreat(DogTreat):
    calories = 30

    def give_treat(self):
        print(f"Выдана косточка (калорийность: {self.calories} ккал)")


class VeggieTreat(DogTreat):
    calories = 10

    def give_treat(self):
        print(f"Выдано овощное лакомство (калорийность: {self.calories} ккал)")


class TreatDispenser(ABC):
    @abstractmethod
    def create_treat(self) -> DogTreat:
        pass

    def dispense_treat(self):
        treat = self.create_treat()
        treat.give_treat()


class MeatDispenser(TreatDispenser):
    def create_treat(self) -> DogTreat:
        return MeatTreat()


class BoneDispenser(TreatDispenser):
    def create_treat(self) -> DogTreat:
        return BoneTreat()


# ==========================================
# 3. ABSTRACT FACTORY (Абстрактная фабрика)
# Создание комплектов амуниции для разных пород собак
# ==========================================
class Collar(ABC):
    @abstractmethod
    def put_on(self):
        pass


class Leash(ABC):
    @abstractmethod
    def attach(self):
        pass


class SmallDogCollar(Collar):
    def put_on(self):
        print("Надет легкий ошейник для маленьких пород (с бантиком).")


class SmallDogLeash(Leash):
    def attach(self):
        print("Пристегнут тонкий поводок-рулетка.")


class LargeDogCollar(Collar):
    def put_on(self):
        print("Надет широкий нейлоновый ошейник с металлическими кольцами.")


class LargeDogLeash(Leash):
    def attach(self):
        print("Пристегнут сверхпрочный поводок для тренировок.")


class DogGearFactory(ABC):
    @abstractmethod
    def create_collar(self) -> Collar:
        pass

    @abstractmethod
    def create_leash(self) -> Leash:
        pass


class SmallDogGearFactory(DogGearFactory):
    def create_collar(self) -> Collar:
        return SmallDogCollar()

    def create_leash(self) -> Leash:
        return SmallDogLeash()


class LargeDogGearFactory(DogGearFactory):
    def create_collar(self) -> Collar:
        return LargeDogCollar()

    def create_leash(self) -> Leash:
        return LargeDogLeash()


# ==========================================
# 4. BUILDER (Строитель)
# Поэтапная сборка пакета услуг по уходу за собакой (Груминг)
# ==========================================
class GroomingPackage:
    def __init__(self):
        self.package_name = ""
        self.services = []

    def add_service(self, service: str):
        self.services.append(service)

    def __str__(self):
        srv = ", ".join(self.services) if self.services else "пустой пакет"
        return f"Пакет услуг '{self.package_name}' [Услуги: {srv}]"


class GroomingBuilder(ABC):
    def __init__(self):
        self.package = GroomingPackage()

    def build_bath(self):
        pass

    def build_haircut(self):
        pass

    def build_nails(self):
        pass

    def build_perfume(self):
        pass

    def get_result(self) -> GroomingPackage:
        return self.package


class BasicGroomingBuilder(GroomingBuilder):
    has_nails = True
    has_perfume = False

    def build_bath(self):
        self.package.package_name = "Базовый уход"
        self.package.add_service("Купание с гипоаллергенным шампунем")

    def build_haircut(self):
        self.package.add_service("Гигиеническая стрижка")

    def build_nails(self):
        self.package.add_service("Стрижка когтей")

    def build_perfume(self):
        pass  # В базовый пакет парфюм не входит


class LuxuryGroomingBuilder(GroomingBuilder):
    has_nails = True
    has_perfume = True

    def build_bath(self):
        self.package.package_name = "Люкс-уход"
        self.package.add_service("Купание с массажем и кондиционером")

    def build_haircut(self):
        self.package.add_service("Модельная стрижка по фото")

    def build_nails(self):
        self.package.add_service("Шлифовка когтей и уход за подушечками лап")

    def build_perfume(self):
        self.package.add_service("Нанесение гипоаллергенного парфюма")


class GroomerDirector:
    """Директор, который знает правильный порядок оказания услуг грумера"""

    def __init__(self, builder: GroomingBuilder):
        self.builder = builder

    def assemble_package(self):
        self.builder.build_bath()
        self.builder.build_haircut()

        # Безопасная проверка атрибутов конструктора без хардкода
        if getattr(self.builder, 'has_nails', False):
            self.builder.build_nails()
        if getattr(self.builder, 'has_perfume', False):
            self.builder.build_perfume()