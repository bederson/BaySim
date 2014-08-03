from perlin import SimplexNoise
from crab import *
from cells import *
import random


class World():
    def __init__(self, world_width=WORLD_WIDTH, world_height=WORLD_HEIGHT, num_foods=NUM_FOODS):
        """
        __init__(int, int, int) -> None
        Constructor initializes the world with the dimensions of the world, and then generates
        a world grid with the specified number of foods, and number of water sources.
        """
        self.world_width = world_width
        self.world_height = world_height
        self.grid = []
        self.elevation_min = 0
        self.elevation_max = 0
        self.num_crabs = 0
        self.generate_world(num_foods)
        self.crab_handlers = []

    def add_crab_handler(self, handler):
        self.crab_handlers.append(handler)

    def fire_crab_handlers(self, cell):
        for handler in self.crab_handlers:
            handler(cell)

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
                # If cell has or generates water, then flow water into neighbors
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

                # If cell has or generates pollution, then flow pollution into neighbors
                if cell.pollution > 0 or isinstance(cell, BuildingCell):
                    for neighbor in cell.neighbors(include_water=True):
                        if neighbor.get_elevation() < cell.get_elevation():
                            if isinstance(cell, BuildingCell):
                                neighbor.pollution = cell.runoff_gen
                            else:
                                amount_pollution_to_move = cell.pollution / 4
                                neighbor.pollution += amount_pollution_to_move
                                if neighbor.pollution > MAX_POLLUTION:
                                    neighbor.pollution = MAX_POLLUTION
                                cell.pollution -= amount_pollution_to_move
                                if cell.pollution < 0:
                                    cell.pollution = 0

                # Evaporate water
                if cell.water_level > 0:
                    cell.water_level -= EVAPORATION_RATE

                # Grow plants
                if isinstance(cell, ArableLandCell):
                    cell.grow()

                # Process crabs
                crab = cell.get_crab()
                if crab:
                    crab.step(cell, self)

    def generate_world(self, num_foods):
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
        if False:
            for row_num in range(self.world_height):
                row_list = []
                for col_num in range(self.world_width):
                    # Uses Perlin noise to generate elevation
                    # https://pypi.python.org/pypi/noise
                    elev = (1.0 + noise.noise2(col_num / TERRAIN_SMOOTHNESS, row_num / TERRAIN_SMOOTHNESS)) * 5.0 / 2
                    cell = LandCell(self, [row_num, col_num], elev)
                    row_list.append(cell)
                    index += 1
                self.grid.append(row_list)
        else:
            lines = open(DATA_FILE).readlines()
            nxy = self.world_height*self.world_width
            if len(lines) != nxy:
                print "bad file ",nxy,len(lines)
            for row_num in range(self.world_height):
                row_list = []
                for col_num in range(self.world_width):
                    # lines have X,Y,ELEV, for now we ignore X,Y and assume listed in the right order
                    elev = float(lines[index].strip().split()[2])
                    cell = LandCell(self, [row_num, col_num], elev)
                    row_list.append(cell)
                    index += 1
                self.grid.append(row_list)

        # Calculate elevation extrema
        for row_num in range(self.world_height):
            for col_num in range(self.world_width):
                c = self.grid[row_num][col_num]
                if c.elevation < self.elevation_min:
                    self.elevation_min = c.elevation
                if c.elevation > self.elevation_max:
                    self.elevation_max = c.elevation

        # write to a dump file
        if False:
            for row_num in range(self.world_height):
                for col_num in range(self.world_width):
                    c = self.grid[row_num][col_num]
                    print row_num, col_num, c.elevation

        # Add some buildings (replace some cells with buildings)
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

        # Add some plants (replace some cells with plants)
        while num_foods > 0:
            row_num = random.randint(0, self.world_height - 1)
            col_num = random.randint(0, self.world_width - 1)
            cell = self.grid[row_num][col_num]
            elevation = cell.get_elevation()
            if INIT_WATER_LEVEL < elevation < self.elevation_max - 1:
                plant_cell = ArableLandCell(self, [row_num, col_num], elevation)
                self.grid[row_num][col_num] = plant_cell
                num_foods -= 1

        # Add water sources (replace some cells with water)
        for water_source_loc in WATER_SOURCES:
            row_num = water_source_loc[ROW_INDEX]
            col_num = water_source_loc[COL_INDEX]
            cell = self.grid[row_num][col_num]
            elevation = cell.get_elevation()
            if INIT_WATER_LEVEL < elevation:
                water_cell = WaterSourceCell(self, [row_num, col_num], elevation)
                self.grid[row_num][col_num] = water_cell

        # Add the crabs (replace some water cells with creatures)
        num_crabs = NUM_CRABS
        while num_crabs > 0:
            row_num = random.randint(0, self.world_height - 1)
            col_num = random.randint(0, self.world_width - 1)
            cell = self.grid[row_num][col_num]
            elevation = cell.get_elevation()
            if elevation < INIT_WATER_LEVEL - 1:
                crab = Crab([row_num, col_num])
                cell.crab = crab
                self.num_crabs += 1
                num_crabs -= 1
