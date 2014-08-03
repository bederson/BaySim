from random import random

from constants import *


class LandCell(object):
    """
    The base class for all cells. This includes a cell's elevation amd water level
    as well as its location in the world and a reference to the world as well.
    """
    def __init__(self, world, location, elevation):
        """
        __init__(world, list, float) -> None
        Constructor that sets up the instance variables world, location and elevation.
          - world is a reference to an instance of World
          - location specifies where this cell is in the world. It is a list containing [row_num, col_num]
          - elevation is a floating point number specified how high this cell is.
        The water is initialized to 0
        """
        self.world = world
        self.location = location     # (row, col)
        self.elevation = elevation
        if elevation < 0:
            self.water_level = -elevation
        else:
            self.water_level = 0
        self.pollution = 0
        self.crab = None

    #### Getters / Setters
    def get_location(self):
        """
        get_location -> list
        Returns the location of this cell
        """
        return self.location

    def get_elevation(self):
        """
        get_elevation -> float
        Returns the elevation of this cell
        """
        return self.elevation

    def get_water_level(self):
        """
        get_water_level -> float
        Returns the water level of this cell
        """
        return self.water_level

    def get_pollution_level(self):
        return self.pollution

    def get_crab(self):
        return self.crab

    def add_to_water_level(self, amount):
        """
        add_to_water_level(float) -> None
        Adds the specified amount of water to this cell's water level. Insures that water
        is never negative (i.e., adding a negative amount can bring the water level down
        to 0, but never below 0.)
        """
        self.water_level += amount
        if self.water_level < 0:
            self.water_level = 0.0

    def neighbors(self, include_water=False):
        """
        neighbors(Boolean) -> list
        Returns a list of cells that are (valid) "manhattan" neighbors of this cell. For inner cells
        in the world, this will return a list containing references to 4 cells - those that are north,
        east, south and west of the current cell. However, for cells that are on the edge of the world,
        this will not include cells that are beyond the edge of the world (because that would be
        impossible since they do not exist.)

        If the <include_water> argument is False, then neighboring cells will only be included
        if they do not have any water. If <include_water> is True, then neighboring cells will
        be included whether or not they have water.
        """
        cells = []
        for delta in DIRECTION_DELTAS.values():
            row = self.location[ROW_INDEX] + delta[ROW_INDEX]
            col = self.location[COL_INDEX] + delta[COL_INDEX]
            if (col >= 0) and (col < self.world.get_dim()[0]) and (row >= 0) and (row < self.world.get_dim()[1]):
                cell = self.world.get_cell(row, col)
                if include_water or cell.get_water_level() == 0:
                    cells.append(cell)
        return cells


class ArableLandCell(LandCell):
    """
    A subclass of LandCell, this defines a cell that can grow food. It includes a single
    instance variable called plant that represents how much food this cell currently has.
    """
    def __init__(self, world, location, elevation):
        """
        __init__(world, list, float) -> None
        Constructor for this class. It initializes the world, location and elevation
        instance variables by calling the super class constructor.
        It initializes the plant instance variable by calling the reset_food_level() method.
        """
        LandCell.__init__(self, world, location, elevation)
        self.plant = 0
        self.reset_food_level()

    def desc(self):
        """
        desc() -> String
        Utility used by __str__ in generating the string description of this cell.
        """
        return LandCell.desc(self) + "; plant=" + str(self.plant)

    def reset_food_level(self):
        """
        Sets the plant instance variable (i.e., food level) to a randomized value somewhere
        between 0.0 and the FOOD_DEFAULT constant. Use the random() function which must
        be imported.
        """
        food_level = random() * FOOD_DEFAULT
        self.plant = food_level

    def get_food_level(self):
        """
        get_food_level() -> float
        Returns this cell's current food level
        """
        return self.plant

    def set_food_level(self, amount):
        """
        set_food_level(float) -> None
        Sets this cell's food level to the specified amount.
        """
        self.plant = amount

    def add_to_water_level(self, amount):
        """
        add_to_water_level(float) -> None
        Adds the specified amount of water to this cell's water level. Insures that water
        is never negative. If the resulting water level is positive, then the food is reset
        (by alling reset_food_level()) because food can not grow in a cell with water.
        """
        LandCell.add_to_water_level(self, amount)
        if self.water_level > 0:
            self.reset_food_level()

    def grow(self):
        """
        grow() -> None
        If there is no water in this cell, then the plant at this cell grows.
        If there is water in this cell, then this method does nothing.

        If the plant is to grow, then this method grows the plant (i.e., food level)
        at this cell by the amount FOOD_GROWTH.
        The plant level must never exceed the constant LEVEL_MAX
        """
        if self.water_level == 0:
            self.plant += FOOD_GROWTH * random()
            if self.plant > LEVEL_MAX:
                self.plant = LEVEL_MAX


class WaterSourceCell(LandCell):
    """
    A subclass of LandCell, this defines a cell that generates water. That is, these cells
    produce water which then flows into neighboring cells.
    """
    def __init__(self, world, location, elevation):
        """
        __init__(world, list, float, float) -> None
        Constructor for this class. It initializes the world, location and elevation
        instance variables by calling the super class constructor.
        It initializes the water_level instance variable with the specified argument.
        """
        LandCell.__init__(self, world, location, elevation)


class BuildingCell(LandCell):
    """
    Buildings are bad, then can produce runoff
    """
    def __init__(self, world, location, elevation):
        LandCell.__init__(self, world, location, elevation)
        self.runoff_gen = random() / 2
