from abc import ABC
from typing import Optional
from collections import deque
import random


MAP_HEIGHT = 10
MAP_WEIGHT = 10


class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

    def find_neighbors(self):
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
                neighbor = Point(self.x + dx, self.y + dy)
                neighbors.append(neighbor)
        return neighbors


class Entity(ABC):
    def __init__(self, point: Point, icon: str):
        self.point = point
        self.icon = icon

    def __str__(self) -> str:
        return self.icon
    
    def get_point(self):
        return self.point


class Creature(Entity):
    def __init__(self, point: Point, speed: int, health: int, icon: str):
        super().__init__(point, icon)
        self.speed = speed
        self.health = health
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
    def __init__(self, point: Point, speed: int=2, health: int=2, icon: str="🐑"):
        super().__init__(point, speed, health, icon)


class Predator(Creature):
    def __init__(self, point: Point, speed: int=3, health: int=2, damage: int=1, icon: str="🐅"):
        super().__init__(point, speed, health, icon)
        self.damage = damage

 

class Grass(Entity):
    def __init__(self, point: Point, icon="🌿"):
        super().__init__(point, icon)


class Rock(Entity):
    def __init__(self, point: Point, icon="🗿"):
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
    
    def get_entity(self, coordinate: Point) -> Entity | None:
        return self.coordinates.get(coordinate)
    
    def set_entity(self, object: Entity) -> None:
        self.coordinates[object.get_point()] = object

    def remove_entity(self, point: Point) -> None:
        if point in self.coordinates:
            del self.coordinates[point]

    def find_path(self, start: Point) -> list | None:
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
            
            neighbors = current.find_neighbors()

            for neighbor in neighbors:
                
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
                    print(" .", end="")
            print()


class Actions():
    def __init__(self) -> None:
        self.proportion = {
            Rock: 0.1,
            Tree: 0.1,
            Grass: 0.1,
            Herbivore: 0.1,
            Predator: 0.03
        }
    def spawn_objects(self, world: Map):
        world_size = float(world.height * world.weight)
        counter = 0
        for obj in self.proportion:
            number_of_obj = (self.proportion[obj] * world_size)//1
            while counter != number_of_obj:
                object = obj(Point(random.randint(0, MAP_WEIGHT-1), random.randint(0, MAP_HEIGHT-1)))
                world.set_entity(object)
                counter += 1
            counter = 0

        


def main():
    # Исправленный порядок размеров: высота, ширина
    act = Actions()
    world = Map(MAP_HEIGHT, MAP_WEIGHT)
    act.spawn_objects(world)
    render = Renderer(world)
    render.render_map()

        
if __name__ == "__main__":
    main()