from entities import Rock, Tree, Grass, Herbivore, Predator, Creature
from map import Map, MAP_HEIGHT, MAP_WEIGHT
from point import Point
from collections import deque
from math import floor
import random
 

class Actions():
    def __init__(self, world: Map) -> None:
        self._proportion = {
            Rock: 0.1,
            Tree: 0.1,
            Grass: 0.1,
            Herbivore: 0.1,
            Predator: 0.03
        }
        self._world = world

    def spawn_objects(self) -> None:
        for obj, proportion in self._proportion.items():
            active_obj = self._world.get_all_obj(obj)
            self._add_object(self._get_number_obj(proportion, active_obj), obj)
    
    def _get_number_obj(self, proportion, active_obj) -> None:
        return (floor(proportion * self._world.get_area())) - len(active_obj)

    def _add_object(self, count, obj) -> None:
        while (count):
            point = Point(random.randint(0, self._world.weight - 1), random.randint(0, self._world.height - 1))
            if not self._world.get_entity(point):
                self._world.set_entity(obj(point))
                count -= 1
    
    def find_paths(self, start: Point, target_type: type) -> list[list[Point]]:
        paths = []
    
        visited: dict = {start: None}
        queue = deque([start])

        while queue:
            current = queue.popleft()
            current_entity_type = type(self._world.get_entity(current))
            if current_entity_type == target_type:
                path = []
                while current != start:
                    path.append(current)
                    current = visited[current]
                path.reverse()
                paths.append(path)

            neighbors = current.find_neighbors()

            for neighbor in neighbors:
                
                if self._world.check_bounds(neighbor): 
                    continue
                
                if neighbor in visited: 
                    continue
                
                neighbor_entity = self._world.get_entity(neighbor)
                
                if neighbor_entity:
                    if not isinstance(neighbor_entity, target_type):
                        continue
                
                visited[neighbor] = current
                queue.append(neighbor)
        return paths
    
    def find_shorter_path(self, paths: list[list[Point]]) -> list[Point]:
        return min(paths, key=len, default=[])
    
    def turn_actions(self) -> None:

        self._move_sheeps()
        self._move_wolfs()
    
    def _move_sheeps(self) -> None:
        sheeps = self._world.get_all_obj(Herbivore)
        for sheep in sheeps:
            paths = self.find_paths(sheep.point, Grass)
            path = self.find_shorter_path(paths)
            if not path:
                continue
                
            steps = min(len(path), sheep.speed)
            for i in range(steps):
                next_point = path[i]
                if not isinstance(self._world.get_entity(next_point), Herbivore):
                    self._change_obj_position(sheep, next_point)
    
    def _move_wolfs(self) -> None:
        wolfs = self._world.get_all_obj(Predator)
        for wolf in wolfs:
            paths = self.find_paths(wolf.point, Herbivore)
            path = self.find_shorter_path(paths)

            steps = min(len(path), wolf.speed)
            for i in range(steps):
                next_point = path[i]
                next_entity = self._world.get_entity(next_point)

                if isinstance(next_entity, Creature) and next_entity.health > wolf.damage:
                    next_entity.health -= wolf.damage
                    break
                else:
                    self._change_obj_position(wolf, next_point)
    
    def _change_obj_position(self, obj: Creature, next_point: Point) -> None:
        self._world.remove_entity(obj.point)
        obj.makeMove(next_point)
        self._world.set_entity(obj)