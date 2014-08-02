from world import World
from cells import *

def neighbors(cell):
    return cell.neighbors(include_water=False)


class Simulation():
    def __init__(self, world_width=WORLD_WIDTH, world_height = WORLD_HEIGHT, num_foods=NUM_FOODS):
        self.world = World(world_width, world_height, num_foods)
        self.world_handlers = []             # List of world handler callbacks

    def add_world_handler(self, handler):
        self.world_handlers.append(handler)

    def fire_world_handler(self):
        for handler in self.world_handlers:
            handler()

    def step(self):
        # Process water
        self.world.step()

        # Update world
        self.fire_world_handler()