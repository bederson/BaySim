from random import randint
from constants import *
from cells import *


class Creature():
    """
    The creature class represents the creature in the world including its location,
    its hunger, and eye sight.
    """
    def __init__(self, starting_location=(0, 0), starting_hunger=INIT_HUNGER):
        self.location = starting_location
        self.hunger_level = starting_hunger

    def __str__(self):
        return "Creature \n \t Location: " + str(self.get_location()) + " \n \t Hunger Level: " + str(self.hunger_level)

    #### Getters / Setters
    def get_location(self):
        return list(self.location)

    def set_location(self, loc):
        self.location = loc

    def get_hunger_level(self):
        return self.hunger_level

    def set_hunger_level(self, hunger_level):
        """
        Sets the hunger, but restricts it to legal values - i.e., [0, LEVEL_MAX]
        """
        self.hunger_level = hunger_level
        if self.hunger_level > LEVEL_MAX:
            self.hunger_level = LEVEL_MAX
        elif self.hunger_level < 0:
            self.hunger_level = 0

    def legal_move(self, loc, world):
        """
        legal_move(list, world) -> Boolean
        Returns True if a given location is within the world and if that location doesn't
        have any water in it.
        """
        loc_row = loc[ROW_INDEX]
        loc_col = loc[COL_INDEX]
        if (loc_row >= 0) and (loc_row < world.get_dim()) and (loc_col >= 0) and (loc_col < world.get_dim()):
            cell = world.get_cell(loc_row, loc_col)
            if cell.get_water_level() <= 0:
                return True
        else:
            return False

    def sign(self, x):
        """
        sign(int) -> int
        Utility function - feel free to use it if is useful.
        Returns 1 if the argument is positive, -1 if the argument is negative,
        and 0 if the argument is 0.
        """
        if x > 0:
            return 1
        elif x < 0:
            return -1
        else:
            return 0

    def get_random_direction(self, world):
        """
        get_random_directio(world) -> list
        Randomly determins a location to move
        the creature one cell north, east, south or west.
        It must confirm that the chosen direction results in a valid
        location (i.e., that the moved to cell would still be in the world).
        If not, it must keep looking until it finds a random direction that
        will result in moving to a cell within the bounds of the world.
        Note that this does not actually move the creature, but instead
        returns a location for the creature to move to.
        """
        neighbor_dirs = DIRECTION_DELTAS.values()
        keep_looking = True
        loc = None
        creature_loc = self.get_location()
        while keep_looking:
            direction = neighbor_dirs[randint(0, 3)]
            loc = [creature_loc[0] + direction[0], creature_loc[1] + direction[1]]
            keep_looking = not self.legal_move(loc, world)
        return loc

    def find_best_nearby_cell(self, world):
        loc = self.get_random_direction(world)

        return loc

    def eat(self, world):
        """
        eat(world) -> Boolean
        If the creature is at an ArableLandCell cell, and the creature is hungry, then it will
        eat all the food at that cell, reducing its hunger by the amount of food it ate.
        The cell's food level will be reset through the cell.reset_food_level() call.

        Note: Be sure to call cell.reset_food_level() if the food is eaten - do not simply
        set the cell's food level to 0.

        It returns True if it did in fact eat.
        """
        row = self.location[ROW_INDEX]
        col = self.location[COL_INDEX]
        cell = world.get_cell(row, col)
        hunger = self.get_hunger_level()
        if hunger > 0 and isinstance(cell, ArableLandCell):         # Confirm food and hunger
            food_level = world.get_food_level(row, col)
            if food_level > self.hunger_level:
                self.hunger_level = 0
            else:
                self.hunger_level -= food_level
            cell.reset_food_level()
            return True

    def move(self, direction, world):
        """
        move(string, world) -> list
        This moves the creature in the specified direction if that results in a legal position.
        The direction can be the string 'Left', 'Right', 'Up' or 'Down'. It returns True if the
        creature does in fact move or False otherwise.

        This must be implemented using the DIRECTION_DELTAS dictionary. using the direction
        argument as a key to look up the associated delta in the dictionary. Do not simply use
        4 if/elif statement.
        """
        loc = self.get_location()
        loc[ROW_INDEX] += DIRECTION_DELTAS[direction][ROW_INDEX]
        loc[COL_INDEX] += DIRECTION_DELTAS[direction][COL_INDEX]
        if self.legal_move(loc, world):
            self.set_location(loc)
            return loc
        else:
            return False