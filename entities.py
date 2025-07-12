from abc import ABC
from point import Point


class Entity(ABC):
    def __init__(self, point: Point, icon: str) -> None:
        self.point = point
        self.icon = icon

    def __str__(self) -> str:
        return self.icon
    
    def get_point(self) -> Point:
        return self.point


class Creature(Entity):
    def __init__(self, point: Point, speed: int, health: int, icon: str) -> None:
        super().__init__(point, icon)
        self.speed = speed
        self.health = health
        self.current_path = None
    
    def makeMove(self, target: Point) -> None:
        self.point = target


class Herbivore(Creature):
    def __init__(self, point: Point, speed: int = 2, health: int = 2, icon: str = "🐑") -> None:
        super().__init__(point, speed, health, icon)


class Predator(Creature):
    def __init__(self, point: Point, speed: int=3, health: int=2, damage: int=1, icon: str="🐺") -> None:
        super().__init__(point, speed, health, icon)
        self.damage = damage


class Grass(Entity):
    def __init__(self, point: Point, icon="🌿") -> None:
        super().__init__(point, icon)


class Rock(Entity):
    def __init__(self, point: Point, icon="🗿") -> None:
        super().__init__(point, icon)
        

class Tree(Entity):
    def __init__(self, point: Point, icon="🌲") -> None:
        super().__init__(point, icon)