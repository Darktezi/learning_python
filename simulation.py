from map import Map, Renderer, MAP_HEIGHT, MAP_WEIGHT
from actions import Actions
from threading import Event
from time import sleep
import keyboard

class Simulation():
    def __init__(self):
        self.world = Map(MAP_HEIGHT, MAP_WEIGHT)
        self.act = Actions(self.world)
        self.rend = Renderer(self.world)
        self.pause_event = Event()
        self.exit_event = Event()

    def next_turn(self):
        self.act.turn_actions()
        self.act.spawn_objects()
        print("=" * MAP_WEIGHT * 2)
        self.rend.render_map()
        print("=" * MAP_WEIGHT * 2)

    def start_simulation(self):
        while not self.exit_event.is_set():
            if not self.pause_event.is_set():
                self.next_turn()
            sleep(1)

    def input_listener(self):
        while not self.exit_event.is_set():
            if keyboard.is_pressed('2'):
                self.pause_event.set()
                print("\nСимуляция приостановлена")
                sleep(0.3)
            elif keyboard.is_pressed('1'):
                self.pause_event.clear()
                print("\nСимуляция возобновлена")
                sleep(0.3)
            elif keyboard.is_pressed('q'):
                self.exit_event.set()
                print("\nЗавершение программы...")
                break
            sleep(0.1)