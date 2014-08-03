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
        died = False
        spawned = False
        if self.health > 0:
            if cell.pollution > 0:
                self.health -= cell.pollution
                if self.health <= 0:
                    self.die(cell, world)
                    died = True
            else:
                self.health += 0.1
                if self.health > MAX_HEALTH:
                    self.spawn(cell, world)
                    died = True

        if not died and not spawned:
            self.move(cell, world)

    def move(self, cell, world):
        new_loc = self.find_best_nearby_cell(world)
        if new_loc != self.location:
            # print "MOVE FROM " + str(self.location) + " to " + str(new_loc)
            new_cell = world.get_cell(new_loc[ROW_INDEX], new_loc[COL_INDEX])
            temp_health = self.health
            self.health = 0
            world.fire_crab_handlers(cell)
            cell.crab = None
            new_cell.crab = self
            self.location = new_loc
            self.health = temp_health
            world.fire_crab_handlers(new_cell)
            # print cell, cell.location, cell.crab
            # print new_cell, new_cell.location, new_cell.crab

    def die(self, cell, world):
        # print "DIE AT " + str(self.location)
        self.health = 0
        world.fire_crab_handlers(cell)
        cell.crab = None
        # world.num_crabs -= 1
        # print "crab DIED", world.num_crabs

    def spawn(self, cell, world):
        # print "SPAWN AT " + str(self.location)
        new_loc = self.get_random_direction(world)
        if new_loc != self.location:
            # print "   NEW LOCATION FOUND"
            new_cell = world.get_cell(new_loc[ROW_INDEX], new_loc[COL_INDEX])
            if not new_cell.crab:
                # print "  SUCCESSFUL CRAB SPAWN"
                new_crab = Crab(new_loc)
                new_cell.crab = new_crab
                world.fire_crab_handlers(new_cell)
                self.health /= 2.0
                world.fire_crab_handlers(cell)
                # world.num_crabs += 1
                # print "spawned crab", world.num_crabs