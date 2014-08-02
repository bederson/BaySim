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
        self.water_delta = []
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
        """
        step_water() -> None
        Performs one step of the water simulation. This includes having each water source generate
        a bit of water, flowing all the water down hill one step, and evaporating the water a bit.
        """
        self.add_water_to_sources()
        self.flow_water()
        self.evaporate_water()
        self.apply_water_delta()

    def add_water_to_sources(self):
        """
        add_water_to_sources() -> None
        This has each water source in the world generate a bit of water. Specifically,
        the water level at WaterSourceCell is increased by the constant WATER_SOURCE_FLOW.
        """
        for row_num, row in enumerate(self.grid):
            for col_num, cell in enumerate(row):
                if isinstance(cell, WaterSourceCell):
                    cell.add_to_water_level(WATER_SOURCE_FLOW)

    def flow_water(self):
        """
        flow_water() -> None
        This performs one step of the water flow algorithm, flowing water a bit from
        every cell that has water to neighboring cells that have lower water levels.
        Rather than directly modifying the cells' water levels, this calculates how
        each cell's water level changes and stores that change in an instance variable
        called self.water_delta which is a 2D grid of floats.  Later on, the
        apply_water_delta() method is called for you which actually modifies the cell's
        water level by adding or subtracting the calculated delta to the cell's
        water level, so you should not do step #2 of the algorithm in the spec ("Apply deltas").

        Note that the self.water_delta grid is guaranteed to have every value
        initialized to 0 before this method is called and that you do not have
        to do that initialization yourself.

        Note that you must store the changes in the self.water_delta grid
        instance variable. Do not make your own water_delta variable.

        See the assignment for complete details.
        """
        for row_num, row in enumerate(self.grid):
            for col_num, cell in enumerate(row):
                water_flowed_from_cell = 0
                for neighbor in cell.neighbors(include_water=True):
                    avail_water_to_move = cell.water_level - water_flowed_from_cell
                    if avail_water_to_move >= 0:
                        neighbor_row = neighbor.get_location()[ROW_INDEX]
                        neighbor_col = neighbor.get_location()[COL_INDEX]
                        cell_height_with_water = cell.elevation + avail_water_to_move
                        neighbor_height_with_water = neighbor.get_elevation() + neighbor.get_water_level() + self.water_delta[neighbor_row][neighbor_col]
                        if cell_height_with_water > neighbor_height_with_water:
                            amount_water_to_move = (cell_height_with_water - neighbor_height_with_water) / 2.0
                            if amount_water_to_move > avail_water_to_move:
                                amount_water_to_move = avail_water_to_move
                            if amount_water_to_move > WATER_MAX_FLOW:
                                amount_water_to_move = WATER_MAX_FLOW
                            self.water_delta[row_num][col_num] -= amount_water_to_move
                            self.water_delta[neighbor_row][neighbor_col] += amount_water_to_move
                            water_flowed_from_cell += amount_water_to_move

    def evaporate_water(self):
        """
        evaporate_water() -> None
        Every cell that has water is evaporated a little bit.
        Specifically, every cell that has water is reduced by EVAPORATION_RATE.
        This method doesn't actually reduce the water level in the cells, but
        rather modifies the <water_delta> table that is used later to actually
        reduce the cells' water level.
        """
        for row_num, row in enumerate(self.grid):
            for col_num, cell in enumerate(row):
                if cell.water_level > 0:
                    self.water_delta[row_num][col_num] -= EVAPORATION_RATE

    def apply_water_delta(self):
        """
        apply_water_delta() -> None
        This applies the <water_delta> table to the water level at every cell.
        Specifically, for each cell in the world, this adds (or subtracts) the
        amount of water in the <water_delta> table corresponding to that cell,
        ensuring that the water level never goes below 0.
        """
        for row_num, row in enumerate(self.grid):
            for col_num, cell in enumerate(row):
                cell.add_to_water_level(self.water_delta[row_num][col_num])
                self.water_delta[row_num][col_num] = 0.0

    def generate_world(self, num_foods, num_water_sources):
        """
        generate_world(int, int) -> None
        Initializes the world grid to a grid of cells with smoothly varying
        height and the specified number of randomly placed foods and water sources.
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
            delta_row_list = []
            for col_num in range(self.world_dim):
                # Uses Perlin noise to generate elevation
                # https://pypi.python.org/pypi/noise
                elev = (1.0 + noise.noise2(col_num / TERRAIN_SMOOTHNESS, row_num / TERRAIN_SMOOTHNESS)) * ELEVATION_MAX / 2
                if index in food_indices:
                    cell = ArableLandCell(self, [row_num, col_num], elev)
                elif index in water_indices:
                    cell = WaterSourceCell(self, [row_num, col_num], elev, WATER_SOURCE_FLOW)
                else:
                    cell = LandCell(self, [row_num, col_num], elev)
                row_list.append(cell)
                delta_row_list.append(0.0)
                index += 1
            self.grid.append(row_list)
            self.water_delta.append(delta_row_list)