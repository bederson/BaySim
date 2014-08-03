import random
from constants import *


class Crab():
    """
    The Crab class represents a crab that lives in the water.
    """
    def __init__(self, location):
        self.location = location
        self.health = self.init_health()

    #### Getters / Setters
    def get_location(self):
        return list(self.location)

    def set_location(self, loc):
        self.location = loc

    def init_health(self):
        return random.random() * MAX_HEALTH / 2.0

    def good_move(self, loc, world):
        """
        legal_move(list, world) -> Boolean
        Returns True if a given location is within the world and if that location doesn't
        have any water in it.
        """
        loc_row = loc[ROW_INDEX]
        loc_col = loc[COL_INDEX]
        world_dim = world.get_dim()
        if (loc_row >= 0) and (loc_row < world_dim[1]) and (loc_col >= 0) and (loc_col < world_dim[0]):
            cell = world.get_cell(loc_row, loc_col)
            if cell.get_water_level() > 2:
                return True
        return False

    def get_random_direction(self, world):
        neighbor_dirs = DIRECTION_DELTAS.values()
        keep_looking = True
        tries = 5
        loc = None
        crab_loc = self.get_location()
        while keep_looking:
            direction = neighbor_dirs[random.randint(0, 3)]
            loc = [crab_loc[0] + direction[0], crab_loc[1] + direction[1]]
            keep_looking = not self.good_move(loc, world)
            tries -= 1
            if tries == 1:
                loc = crab_loc
                break
        return loc

    def find_best_nearby_cell(self, world):
        loc = self.get_random_direction(world)

        return loc

    def step(self, cell, world):
        self.move(cell, world)

        if self.health > 0:
            if cell.pollution > 0:
                self.health -= cell.pollution
                if self.health <= 0:
                    self.die(cell, world)
            else:
                self.health += 0.1
                if self.health > MAX_HEALTH:
                    self.spawn(world)

    def move(self, cell, world):
        new_loc = self.find_best_nearby_cell(world)
        if new_loc:
            cell.crab = None
            self.location = new_loc
            new_cell = world.get_cell(new_loc[ROW_INDEX], new_loc[COL_INDEX])
            new_cell.crab = self

    def die(self, cell, world):
        # When UI updates, the crab reference will be removed
        self.health = 0
        world.num_crabs -= 1
        print "crab died", world.num_crabs

    def spawn(self, world):
        new_loc = self.get_random_direction(world)
        if new_loc:
            new_cell = world.get_cell(new_loc[ROW_INDEX], new_loc[COL_INDEX])
            if not new_cell.crab:
                self.health = self.init_health()
                new_crab = Crab(new_loc)
                new_cell.crab = new_crab
                world.num_crabs += 1
                print "spawned crab", world.num_crabs