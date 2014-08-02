from constants import *
from cells import LandCell, WaterSourceCell, ArableLandCell
from perlin import SimplexNoise
from unique_rands import unique_rands


class World():
    def __init__(self, world_dim=WORLD_DIM, num_foods=NUM_FOODS, num_water_sources=NUMBER_OF_WATER_SOURCES):
        """
        __init__(int, int, int) -> None
        Constructor initializes the world with the dimensions of the world, and then generates
        a world grid with the specified number of foods, and number of water sources.
        """
        self.world_dim = world_dim
        self.grid = []
        self.generate_world(num_foods, num_water_sources)

    def get_food_level(self, row, col):
        """
        get_food_level(int, int) -> float
        Returns the amount of food at the cell specified at the position [row, col].
        If the cell isn't an ArableLandCell, this returns None since it can't contain any food.
        """
        cell = self.grid[row][col]
        if isinstance(cell, ArableLandCell):
            return self.grid[row][col].get_food_level()

    def grow_all_food_level(self):
        """
        grow_all_food_level() -> None
        This grows all the food in the world at all ArableLandCell's one step.
        """
        for row_num, row in enumerate(self.grid):
            for col_num, cell in enumerate(row):
                if isinstance(cell, ArableLandCell):
                    cell.grow()

    def get_cell(self, row, col):
        """
        get_cell(int, int) -> Cell
        This gets the cell at the specified location [row, col]
        """
        return self.grid[row][col]

    def set_cell(self, row, col, cell):
        """
        set_cell(int, int, Cell) -> None
        This sets the cell at the specified location [row, col]to the specified cell.
        """
        self.grid[row][col] = cell

    def get_dim(self):
        """
        get_dim() -> int
        Returns the dimensions of the world as a single integer. Since the world is square,
        the returned dimension represents both the width and height of the world.
        """
        return self.world_dim

    def step_water(self):
        for row_num, row in enumerate(self.grid):
            for col_num, cell in enumerate(row):
                if cell.water_level > 0 or isinstance(cell, WaterSourceCell):
                    for neighbor in cell.neighbors(include_water=True):
                        amount_water_to_move = 0
                        if isinstance(cell, WaterSourceCell):
                            if neighbor.get_elevation() < cell.get_elevation():
                                neighbor.water_level = cell.get_elevation() - neighbor.get_elevation()
                        else:
                            cell_height_with_water = cell.elevation + cell.water_level
                            neighbor_height_with_water = neighbor.elevation + neighbor.water_level
                            if cell_height_with_water > neighbor_height_with_water:
                                amount_water_to_move = (cell_height_with_water - neighbor_height_with_water) / 4.0
                            if amount_water_to_move > cell.water_level:
                                amount_water_to_move = cell.water_level
                            neighbor.water_level += amount_water_to_move
                            cell.water_level -= amount_water_to_move

                if cell.water_level > 0:
                    cell.water_level -= EVAPORATION_RATE

    def generate_world(self, num_foods, num_water_sources):
        """
        generate_world(int, int) -> None
        Initializes the world grid to a grid of cells with smoothly varying
        height and the specified number of randomly placed foods and water sources.
        @todo read in a real bay model (@DataBay_MD)
        """
        # Fill grid cells - picking the specified number of food and water sources
        noise = SimplexNoise()
        noise.randomize(16)
        num_special_cells = num_foods + num_water_sources
        special_cell_indices = unique_rands(num_special_cells, self.world_dim * self.world_dim - 1)
        food_indices = special_cell_indices[:num_foods]
        water_indices = special_cell_indices[num_foods:]

        index = 0
        for row_num in range(self.world_dim):
            row_list = []
            for col_num in range(self.world_dim):
                # Uses Perlin noise to generate elevation
                # https://pypi.python.org/pypi/noise
                elev = (1.0 + noise.noise2(col_num / TERRAIN_SMOOTHNESS, row_num / TERRAIN_SMOOTHNESS)) * ELEVATION_MAX / 2
                if index in food_indices:
                    cell = ArableLandCell(self, [row_num, col_num], elev)
                elif index in water_indices:
                    cell = WaterSourceCell(self, [row_num, col_num], elev)
                else:
                    cell = LandCell(self, [row_num, col_num], elev)
                row_list.append(cell)
                index += 1
            self.grid.append(row_list)
