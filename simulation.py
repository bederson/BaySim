from world import World
from creature import Creature
from cells import *


def neighbors(cell):
    return cell.neighbors(include_water=False)


class Simulation():
    def __init__(self, number_of_creatures=1, world_width=WORLD_WIDTH, world_height = WORLD_HEIGHT, num_foods=NUM_FOODS, num_water_sources=NUM_WATER_SOURCES):
        self.world = World(world_width, world_height, num_foods, num_water_sources)
        self.creature = self.world.creature
        self.creature_num_skip_steps = DEFAULT_NUM_CREATURE_STEPS_TO_SKIP
        self.world_handlers = []             # List of world handler callbacks
        self.creature_handlers = []          # List of creature handler callbacks

    def add_world_handler(self, handler):
        self.world_handlers.append(handler)

    def add_creature_handler(self, handler):
        self.creature_handlers.append(handler)

    def fire_world_handler(self):
        for handler in self.world_handlers:
            handler()

    def fire_creature_handler(self, original_location, new_location):
        if self.creature.get_hunger_level() >= 10:
            new_location = None
        for handler in self.creature_handlers:
            handler(original_location, new_location)

    def delay_creature_auto_movement(self):
        self.creature_num_skip_steps = NUM_CREATURE_STEPS_TO_SKIP_AFTER_MANUAL_MOVE

    def step(self):
        # Update world
        updated_hunger = self.creature.get_hunger_level() + HUNGER_GROWTH
        self.creature.set_hunger_level(updated_hunger)
        self.fire_world_handler()

        # Process water
        self.world.step()

        # Move the creature
        if self.creature_num_skip_steps > 0:
            # Don't move the creature this step
            self.creature_num_skip_steps -= 1
        else:
            # Auto-move creature
            original_location = self.creature.get_location()
            new_location = self.creature.find_best_nearby_cell(self.world)
            if new_location:
                self.creature.set_location(new_location)
                self.creature.eat(self.world)

            self.creature_num_skip_steps = DEFAULT_NUM_CREATURE_STEPS_TO_SKIP
            self.fire_creature_handler(original_location, new_location)