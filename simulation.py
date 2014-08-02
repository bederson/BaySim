from world import World
from creature import Creature
from cells import *


def neighbors(cell):
    return cell.neighbors(include_water=False)


class Simulation():
    def __init__(self, number_of_creatures=1, world_dim=WORLD_DIM, num_foods=NUM_FOODS, num_water_sources=NUMBER_OF_WATER_SOURCES, creature_location=START_LOCATION, creature_hunger_level=INIT_HUNGER):
        self.world = World(world_dim, num_foods, num_water_sources)
        self.creature = Creature(creature_location, creature_hunger_level)
        self.creature_num_skip_steps = DEFAULT_NUM_CREATURE_STEPS_TO_SKIP
        self.world_handlers = []             # List of world handler callbacks
        self.creature_handlers = []          # List of creature handler callbacks

    def start_text_simulation(self):
        pass

    def __str__(self):
        output = ""
        print(self.creature.get_location())
        for row_num, row in enumerate(self.world.grid):
            for col_num, cell in enumerate(row):
                location = [row_num, col_num]
                if location == self.creature.get_location():
                    output += "ME(" + str(self.creature.get_hunger_level()) + ") "
                elif isinstance(cell, ArableLandCell):
                    output += "FOOD(" + str(self.world.get_food_level(row_num, col_num)) + ")"
                else:
                    output += "  ---  "
                output += " "
            output += "\n"
        return output

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
        self.world.grow_all_food_level()
        self.fire_world_handler()

        # Process water
        self.world.step_water()

        # Move the creature
        if self.creature_num_skip_steps > 0:
            # Auto-move creature
            self.creature_num_skip_steps -= 1
        else:
            original_location = self.creature.get_location()
            new_location = self.creature.find_best_nearby_cell(self.world)
            if new_location:
                self.creature.set_location(new_location)
                self.creature.eat(self.world)

            self.creature_num_skip_steps = DEFAULT_NUM_CREATURE_STEPS_TO_SKIP
            self.fire_creature_handler(original_location, new_location)