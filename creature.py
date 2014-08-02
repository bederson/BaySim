from random import randint
from constants import *
from cells import *


class Creature():
    """
    The creature class represents the creature in the world including its location,
    its hunger, and eye sight.
    """
    def __init__(self, starting_location=(0, 0), starting_hunger=INIT_HUNGER, eye_sight=EYE_SIGHT):
        self.location = starting_location
        self.hunger_level = starting_hunger
        self.eye_sight = eye_sight

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

    def get_food_metric(self, world, target_location):
        """
        get_food_metric(world, list) -> float
        Determines a movement metric based on how much food is at the target location
        and the creature's hunger - where bigger numbers are better.
        That is, given the creature's current hunger and possible target location,
        this function returns an integer that is proportional to the quality of the move
        such that it will return larger numbers for possible destinations that are better.

        The specific metric that this function should implement multiplies
        the creature's hunger level by the food level at the target location. If there is
        no food at the target (either because the target is not an ArableLandCell, or because
        it's food level is 0), then this should return 0.

        Examples:
        If the creature's hunger level is 1, and the target location has food of 2, then this will return 2.
        If the creature's hunger level is 2, and the target location has food of 2, then this will return 4.
        If the creature's hunger level is 2, and the target location has food of 1, then this will return 1.
        If the creature is not hungry, then it would return 0 no matter what parameters are passed in.
        If the target location has food of 0, then it would return 0 no matter what the creature's hunger level.
        """
        food_level = 0
        target_cell = world.get_cell(target_location[ROW_INDEX], target_location[COL_INDEX])
        if type(target_cell) is ArableLandCell:
            food_level = target_cell.get_food_level()
        return self.hunger_level * food_level

    def get_distance_metric(self, target_location):
        """
        get_distance_metric(list) -> int
        Determines a movement metric based on distance where bigger numbers are better.
        That is, given the creature's current location and possible target location,
        this function returns an integer that is proportional to the quality of the move
        such that it will return larger numbers for possible destinations that are better.

        The specific metric that this function should implement is one where shorter
        distances are better. In particular, this should
        count the total number of horizontal steps plus the number of vertical steps
        it would take to go from the current location to the target location, and return
        -1 multiplied by the total number of steps. This way, further distances will
        result in negatively larger numbers. The highest number this can return is 0
        (which would happen if the target_location was at the creature's current location.)

        Example:
        get_distance_metric([0, 0], [2, 1]) => -3
        get_distance_metric([0, 0], [1, 1]) => -2
        get_distance_metric([3, 3], [4, 3]) => -1
        """
        row_delta = abs(target_location[ROW_INDEX] - self.location[ROW_INDEX])
        col_delta = abs(target_location[COL_INDEX] - self.location[COL_INDEX])
        distance = row_delta + col_delta
        return -1 * distance

    def get_elevation_metric(self, world, target_location):
        """
        get_elevation_metric(world, list) -> float
        Determines a movement metric based on how high the target location is
        compared to the creature's current location - where bigger numbers are better.
        That is, given the creature's current location and possible target location,
        this function returns an integer that is proportional to the quality of the move
        such that it will return larger numbers for possible destinations that are better.

        The specific metric that this function should implement is the difference
        in elevation between the current location and the target location where going
        down results in larger numbers.

        Examples:
        If the current elevation is 3 and the target elevation is 5, this should return -2.
        If the current elevation is 5 and the target elevation is 3, this should return 2.
        If the current elevation is 2 and the target elevation is 2, this should return 0.
        If the current elevation is 0 and the target elevation is 4, this should return -4.
        """
        current_cell = world.get_cell(self.location[ROW_INDEX], self.location[COL_INDEX])
        target_cell = world.get_cell(target_location[ROW_INDEX], target_location[COL_INDEX])
        elevation_delta = target_cell.get_elevation() - current_cell.get_elevation()
        return -1 * elevation_delta

    def get_combined_metric(self, world, target_location):
        """
        get_combined_metric(world, list) -> float
        Determines a movement metric based a combination of the food, distance and
        elevation of the target location - where bigger numbers are better.

        The specific metric that this function should implement is a weighted sum of the three
        metrics defined by get_food_metric(), get_distance_metric() and get_elevation_metric().
        In particular, food should count most, so give that a weight of 10, elevation should
        count moderately so give that a weight of 3, and distance shouldn't count that much
        so only give that a weight of 1.

        More specifically, calculate the three individual metricx, and then combine them like this:
        combined_metric = 10 * food_metric + 1 * distance_metric + 3 * elevation_metric
        """
        food_metric = self.get_food_metric(world, target_location)
        distance_metric = self.get_distance_metric(target_location)
        elevation_metric = self.get_elevation_metric(world, target_location)
        metric = 10 * food_metric + 1 * distance_metric + 3 * elevation_metric
        return metric

    def get_metric(self, world, target_location, metric_type):
        """
        get_metric(world, list, int) -> float
        Calculates the metric specified by metric_type which can be one of METRIC_FOOD,
        METRIC_DISTANCE, METRIC_ELEVATION, or METRIC_COMBINED. Each of those constants
        are defined in constants.py.

        Depending on what metric_type is, this function should return the result of
        one of get_food_metric(), get_distance_metric(), get_elevation_metric(), or
        get_combined_metric(), respectively.
        """
        metric = 0
        if metric_type == METRIC_FOOD:
            metric = self.get_food_metric(world, target_location)
        elif metric_type == METRIC_DISTANCE:
            metric = self.get_distance_metric(target_location)
        elif metric_type == METRIC_ELEVATION:
            metric = self.get_elevation_metric(world, target_location)
        elif metric_type == METRIC_COMBINED:
            metric = self.get_combined_metric(world, target_location)
        return metric

    def find_best_nearby_cell(self, world, metric_type):
        """
        find_best_nearby_cell(world, int) -> list
        This function determines which nearby cell the creature should move towards next
        and returns that location in [row, col] form. It makes that decision by calculating
        the specified metric for each cell within the creature's eyesight and moves in
        the direction of the highest ranked cell as long as moving in that direction is legal.
        Otherwise, it moves in a random location.

        Note that this method is different than the find_best_neighbor() method of HW7 because
        this returns the location of a cell that may be distant from the creature rather
        than always returning a cell that is an immediate neighbor of the creature.
        """
        # Find goal (i.e., best cell within eyesight)
        best_metric = None
        best_location = None
        current_row = self.location[ROW_INDEX]
        current_col = self.location[COL_INDEX]
        for row_num in range(current_row - self.eye_sight, current_row + self.eye_sight + 1):
            for col_num in range(current_col - self.eye_sight, current_col + self.eye_sight + 1):
                target_location = [row_num, col_num]
                if self.legal_move(target_location, world):
                    metric = self.get_metric(world, target_location, metric_type)
                    if not best_metric or metric > best_metric:
                        best_metric = metric
                        best_location = [row_num, col_num]

        # If no legal move legal, then try random direction
        loc = best_location
        if not self.legal_move(loc, world):
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