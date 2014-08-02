from perlin import SimplexNoise
from creature import *
import random


class World():
    def __init__(self, world_width=WORLD_WIDTH, world_height=WORLD_HEIGHT, num_foods=NUM_FOODS, num_water_sources=NUM_WATER_SOURCES):
        """
        __init__(int, int, int) -> None
        Constructor initializes the world with the dimensions of the world, and then generates
        a world grid with the specified number of foods, and number of water sources.
        """
        self.world_width = world_width
        self.world_height = world_height
        self.grid = []
        self.creature = None
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
        get_dim() -> (int, int)
        Returns the dimensions of the world as a tuple.
        """
        return (self.world_width, self.world_height)

    def step(self):
        # Iterate over cells
        for row_num, row in enumerate(self.grid):
            for col_num, cell in enumerate(row):
                if cell.water_level > 0 or isinstance(cell, WaterSourceCell):
                    # If cell has water, then iterate over neighbors
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

                # Evaporate water
                if cell.water_level > 0:
                    cell.water_level -= EVAPORATION_RATE

                # Grow plants
                if isinstance(cell, ArableLandCell):
                    cell.grow()

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

        # First generate world full of plain land cells
        index = 0
        for row_num in range(self.world_height):
            row_list = []
            for col_num in range(self.world_width):
                # Uses Perlin noise to generate elevation
                # https://pypi.python.org/pypi/noise
                elev = (1.0 + noise.noise2(col_num / TERRAIN_SMOOTHNESS, row_num / TERRAIN_SMOOTHNESS)) * ELEVATION_MAX / 2
                cell = LandCell(self, [row_num, col_num], elev)
                row_list.append(cell)
                index += 1
            self.grid.append(row_list)

        # write to a dump file
        for row_num in range(self.world_height):
            for col_num in range(self.world_width):
                c = self.grid[row_num][col_num]
                print row_num, col_num, c.elevation

        # Replace some cells with buildings
        num_buildings = NUM_BUILDINGS
        while num_buildings > 0:
            row_num = random.randint(0, self.world_height - 1)
            col_num = random.randint(0, self.world_width - 1)
            cell = self.grid[row_num][col_num]
            elevation = cell.get_elevation()
            if INIT_WATER_LEVEL < elevation < INIT_WATER_LEVEL + 1:
                building_cell = BuildingCell(self, [row_num, col_num], elevation)
                self.grid[row_num][col_num] = building_cell
                num_buildings -= 1

        # Replace some cells with plants
        while num_foods > 0:
            row_num = random.randint(0, self.world_height - 1)
            col_num = random.randint(0, self.world_width - 1)
            cell = self.grid[row_num][col_num]
            elevation = cell.get_elevation()
            if INIT_WATER_LEVEL < elevation:
                plant_cell = ArableLandCell(self, [row_num, col_num], elevation)
                self.grid[row_num][col_num] = plant_cell
                num_foods -= 1

        # Replace some cells with water
        while num_water_sources > 0:
            row_num = random.randint(0, self.world_height - 1)
            col_num = random.randint(0, self.world_width - 1)
            cell = self.grid[row_num][col_num]
            elevation = cell.get_elevation()
            if INIT_WATER_LEVEL < elevation:
                water_cell = WaterSourceCell(self, [row_num, col_num], elevation)
                self.grid[row_num][col_num] = water_cell
                num_water_sources -= 1

        # Add the creature
        num_creatures = 1
        while num_creatures > 0:
            row_num = random.randint(0, self.world_height - 1)
            col_num = random.randint(0, self.world_width - 1)
            cell = self.grid[row_num][col_num]
            elevation = cell.get_elevation()
            if INIT_WATER_LEVEL < elevation:
                self.creature = Creature([row_num, col_num], INIT_HUNGER)
                num_creatures -= 1
