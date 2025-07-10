from point import Point
from entities import Entity


MAP_HEIGHT = 10
MAP_WEIGHT = 10


class Map():

    def __init__(self, height: int, weight: int) -> None:
        self.height = height
        self.weight = weight
        self.coordinates = {}
    
    def get_height(self) -> int:
        return self.height
    
    def get_weight(self) -> int:
        return self.weight
    
    def get_entity(self, coordinate: Point):
        return self.coordinates.get(coordinate)
    
    def set_entity(self, object: Entity) -> None:
        self.coordinates[object.get_point()] = object

    def remove_entity(self, point: Point) -> None:
        if point in self.coordinates:
            del self.coordinates[point]
    
    def get_all_obj(self, obj_type: type) -> list:
        objects = []
        for obj in self.coordinates:
            a = self.get_entity(obj)
            if obj_type == type(a):
                objects.append(a)
        return objects

    def check_bounds(self, point: Point) -> bool | None:
        if point.x < 0 or point.x >= self.weight or point.y < 0 or point.y >= self.height:
            return True
        

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