import random
from constants import *


class Crab():
    """
    The Crab class represents a crab that lives in the water.
    """
    def __init__(self, location):
        self.location = location
        self.health = random.random() * MAX_HEALTH

    #### Getters / Setters
    def get_location(self):
        return list(self.location)

    def set_location(self, loc):
        self.location = loc

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