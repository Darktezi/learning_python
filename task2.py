from abc import ABC
from typing import Optional
from collections import deque
import random


stone_emoji = "\U0001F5FF"
MAP_HEIGHT = 15
MAP_WEIGHT = 50


class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.data=[x, y]

    def __eq__(self, other) -> bool:
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __repr__(self):
        return f"({self.x}, {self.y})"


class Entity(ABC):
    def __init__(self, point: Point, icon):
        self.point = point
        self.icon = icon

    def __str__(self) -> str:
        return self.icon
    
    def get_point(self):
        return self.point


class Creature(Entity):
    def __init__(self, point: Point, speed: int, health: int, icon: str):
        self.point = point
        self.speed = speed
        self.health = health
        self.icon = icon
        self.current_path = None
    
    def makeMove(self, world):
        # Если нет пути или путь закончился, ищем новый
        if self.current_path is None or len(self.current_path) == 0:
            self.current_path = world.find_path(self.point)
            if self.current_path is None:
                print("Путь не найден!")
                return
        
        # Перемещаемся с учетом скорости
        steps = min(self.speed, len(self.current_path))
        for _ in range(steps):
            if len(self.current_path) == 0:
                break
            
            next_point = self.current_path.pop(0)
            
            # Проверяем, не стоим ли мы уже на траве
            current_entity = world.get_entity(self.point)
            if isinstance(current_entity, Grass):
                print("Достигнута трава!")
                self.current_path = None
                break
            
            # Перемещаем существо
            world.remove_entity(self.point)
            self.point = next_point
            world.set_entity(self)


class Herbivore(Creature):
    def __init__(self, point: Point, speed: int, health: int, icon: str="🐑"):
        super().__init__(point, speed, health, icon)

 

class Grass(Entity):
    def __init__(self, point: Point, icon="☘️"):
        super().__init__(point, icon)


class Rock(Entity):
    def __init__(self, point: Point, icon="⛰️"):
        super().__init__(point, icon)
        


class Tree(Entity):
    def __init__(self, point: Point, icon="🌲"):
        super().__init__(point, icon)


class Simulation():
    def next_turn(self):
        pass

    def start_simulation(self):
        pass

    def pause_simulation(self):
        pass


class Map():

    def __init__(self, height: int, weight: int) -> None:
        self.height = height
        self.weight = weight
        self.coordinates = {}
    
    def get_height(self) -> int:
        return self.height
    
    def get_weight(self) -> int:
        return self.weight
    
    def get_entity(self, coordinate: Point) -> Optional[Entity]:
        return self.coordinates.get(coordinate)
    
    def set_entity(self, object: Entity) -> None:
        self.coordinates[object.get_point()] = object

    def remove_entity(self, point: Point) -> None:
        if point in self.coordinates:
            del self.coordinates[point]

    def find_path(self, start: Point) -> Optional[list]:
        start_entity = self.get_entity(start)
        
        # Если уже стоим на траве
        if isinstance(start_entity, Grass):
            return []
        
        visited: dict = {start: None}
        queue = deque([start])
        
        while queue:
            current = queue.popleft()
            current_entity = self.get_entity(current)
            
            # Если нашли траву
            if isinstance(current_entity, Grass):
                path = []
                # Восстанавливаем путь
                while current != start:
                    path.append(current)
                    current = visited[current]
                path.reverse()
                return path
            
            # Проверяем соседние клетки
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = Point(current.x + dx, current.y + dy)
                
                # Проверка выхода за границы карты
                if neighbor.x < 0 or neighbor.x >= self.weight or neighbor.y < 0 or neighbor.y >= self.height:
                    continue
                
                # Если уже посещали эту клетку
                if neighbor in visited:
                    continue
                
                neighbor_entity = self.get_entity(neighbor)
                
                # Проверяем препятствия
                if neighbor_entity:
                    if isinstance(neighbor_entity, (Rock, Tree)):
                        continue
                
                visited[neighbor] = current
                queue.append(neighbor)
        
        return None
        

class Renderer():
    def __init__(self, world: Map):
        self.world = world
    
    def render_map(self):
        for y in range(self.world.get_height()):
            for x in range(self.world.get_weight()):
                entity = self.world.get_entity(Point(x, y))
                if entity:
                    print(entity, end="")
                else:
                    print("-", end="")
            print()


def main():
    static_objects = 5
    # Исправленный порядок размеров: высота, ширина
    world = Map(MAP_HEIGHT, MAP_WEIGHT)
    targets = []

    # Создаем объекты
    for _ in range(static_objects):
        rock = Rock(Point(random.randint(0, MAP_WEIGHT-1), random.randint(0, MAP_HEIGHT-1)))
        tree = Tree(Point(random.randint(0, MAP_WEIGHT-1), random.randint(0, MAP_HEIGHT-1)))
        grass = Grass(Point(random.randint(0, MAP_WEIGHT-1), random.randint(0, MAP_HEIGHT-1)))
        world.set_entity(rock)
        world.set_entity(tree)
        world.set_entity(grass)
        targets.append(grass.point)
    
    
    # позиция травоядного
    herbivore = Herbivore(Point(random.randint(0, MAP_WEIGHT-1), random.randint(0, MAP_HEIGHT-1)), 2, 3)
    world.set_entity(herbivore)
    
    print("Начальное состояние:")
    Renderer(world).render_map()
    
    # Запускаем 5 шагов симуляции
    for turn in range(5):
        print(f"\nХод {turn + 1}:")
        herbivore.makeMove(world)
        Renderer(world).render_map()
        
if __name__ == "__main__":
    main()