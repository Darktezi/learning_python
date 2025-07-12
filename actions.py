from entities import Rock, Tree, Grass, Herbivore, Predator, Creature
from map import Map, MAP_HEIGHT, MAP_WEIGHT
from point import Point
from collections import deque
import random


class Actions():
    def __init__(self, world: Map) -> None:
        self.proportion = {
            Rock: 0.1,
            Tree: 0.1,
            Grass: 0.1,
            Herbivore: 0.1,
            Predator: 0.03
        }
        self.world = world

    def spawn_objects(self) -> None:
        world_size = float(self.world.height * self.world.weight)
        for obj in self.proportion:
            active_obj = self.world.get_all_obj(obj)
            number_of_obj = ((self.proportion[obj] * world_size)//1) - len(active_obj)
            while number_of_obj:
                object = obj(Point(random.randint(0, MAP_WEIGHT-1), random.randint(0, MAP_HEIGHT-1)))
                while self.world.get_entity(object.point) != None:
                    object = obj(Point(random.randint(0, MAP_WEIGHT-1), random.randint(0, MAP_HEIGHT-1)))
                self.world.set_entity(object)
                    
                number_of_obj -= 1
    
    def find_paths(self, start: Point, target_type: type) -> list:
        paths = []
    
        visited: dict = {start: None}
        queue = deque([start])

        while queue:
            current = queue.popleft()
            current_entity_type = type(self.world.get_entity(current))
            if current_entity_type == target_type:
                path = []
                while current != start:
                    path.append(current)
                    current = visited[current]
                path.reverse()
                paths.append(path)

            neighbors = current.find_neighbors()

            for neighbor in neighbors:
                
                if self.world.check_bounds(neighbor): 
                    continue
                
                if neighbor in visited: 
                    continue
                
                neighbor_entity = self.world.get_entity(neighbor)
                
                if neighbor_entity:
                    if isinstance(neighbor_entity, (Rock, Tree)):
                        continue
                
                visited[neighbor] = current
                queue.append(neighbor)
        return paths
    
    def find_shorter_path(self, paths: list) -> list:
        min = 999
        min_path = []
        for i in paths:
            if len(i) < min:
                min_path = i
                min = len(i)
        return min_path
    
    def turn_actions(self) -> None:
        sheeps = self.world.get_all_obj(Herbivore)
        wolfs = self.world.get_all_obj(Predator)

        for sheep in sheeps:
            paths = self.find_paths(sheep.point, Grass)
            path = self.find_shorter_path(paths)
            if len(path) <= sheep.speed:
                for i in range(len(path)):
                    next_point = path[i]
                    if type(self.world.get_entity(next_point)) != Herbivore:
                        self.world.remove_entity(sheep.point)
                        sheep.makeMove(next_point)
                        self.world.set_entity(sheep)
            elif len(path) >= sheep.speed:
                for i in range(sheep.speed):
                    next_point = path[i]
                    if type(self.world.get_entity(next_point)) != Herbivore:
                        self.world.remove_entity(sheep.point)
                        sheep.makeMove(next_point)
                        self.world.set_entity(sheep)

            else:
                continue
        
        for wolf in wolfs:
            paths = self.find_paths(wolf.point, Herbivore)
            path = self.find_shorter_path(paths)
            if len(path) <= wolf.speed:
                for i in range(len(path)):
                    next_point = path[i]
                    next_entity = self.world.get_entity(next_point)
                    if isinstance(next_entity, Creature) and next_entity.health > wolf.damage:
                        next_entity.health -= wolf.damage
                        continue
                    else:
                        self.world.remove_entity(wolf.point)
                        wolf.makeMove(next_point)
                        self.world.set_entity(wolf)
            elif len(path) >= wolf.speed:
                for i in range(wolf.speed):
                    next_point = path[i]
                    next_entity = self.world.get_entity(next_point)
                    if isinstance(next_entity, Creature) and next_entity.health > wolf.damage:
                        next_entity.health -= wolf.damage
                        continue
                    else:
                        self.world.remove_entity(wolf.point)
                        wolf.makeMove(next_point)
                        self.world.set_entity(wolf)
            else:
                continue