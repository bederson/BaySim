# List indices for locations
ROW_INDEX = 0
COL_INDEX = 1

# Initial values
WORLD_DIM = 100
CELL_SIZE = 8
NUM_FOODS = 10
NUMBER_OF_WATER_SOURCES = 2
INIT_HUNGER = 0
START_LOCATION = [50, 50]

# Debugging constants (only set one to True at a time)
DEBUG_ELEVATION = False
DEBUG_WATER_LEVEL = False

# Simulation constants
TERRAIN_SMOOTHNESS = 50.0           # Bigger values makes the terrain smoother
HUNGER_GROWTH = 0.01
FOOD_DEFAULT = -1.0
FOOD_GROWTH = 0.01        # Amount food grows per step
LEVEL_MAX = 4
STEP_TIME = 100           # In milliseconds
DEFAULT_NUM_CREATURE_STEPS_TO_SKIP = 6
NUM_CREATURE_STEPS_TO_SKIP_AFTER_MANUAL_MOVE = 30
ELEVATION_MAX = 5
EYE_SIGHT = WORLD_DIM / 6
WATER_SOURCE_FLOW = 10.0            # Amount of water generated per step at each water source
WATER_MAX_FLOW = 1.0                # Maximum amount of water that can move from one cell to another per step
EVAPORATION_RATE = 0.006
INIT_WATER_LEVEL = 2

DIRECTION_DELTAS = {
    'Left':  [0, -1],
    'Right': [0,  1],
    'Up':    [-1, 0],
    'Down':  [1,  0]
}

# Visual Display constants
TEXT_OFFSET = 3
WATER_TEXT_OFFSET = 16
METER_HEIGHT = 5

# Image filenames
IMAGE_CREATURE_UP = "images/creature_up.gif"
IMAGE_CREATURE_DOWN = "images/creature_down.gif"
IMAGE_CREATURE_LEFT = "images/creature_left.gif"
IMAGE_CREATURE_RIGHT = "images/creature_right.gif"
IMAGE_WATER_SOURCE = "images/water_source.gif"
IMAGE_LAND1 = "images/land1.gif"
IMAGE_LAND2 = "images/land2.gif"
IMAGE_LAND3 = "images/land3.gif"
IMAGE_LAND4 = "images/land4.gif"
IMAGE_LAND5 = "images/land5.gif"
IMAGE_LAND6 = "images/land6.gif"
IMAGE_LAND7 = "images/land7.gif"
IMAGE_LAND8 = "images/land8.gif"
IMAGE_LAND9 = "images/land9.gif"
IMAGE_LAND10 = "images/land10.gif"
IMAGE_ARABLE_LAND = "images/land1.gif"
IMAGE_PLANT1 = "images/plant1.gif"
IMAGE_PLANT2 = "images/plant2.gif"
IMAGE_PLANT3 = "images/plant3.gif"
IMAGE_PLANT4 = "images/plant4.gif"
IMAGE_PLANT5 = "images/plant5.gif"
IMAGE_PLANT6 = "images/plant6.gif"
IMAGE_PLANT7 = "images/plant7.gif"
IMAGE_PLANT8 = "images/plant8.gif"
IMAGE_PLANT9 = "images/plant9.gif"
IMAGE_PLANT10 = "images/plant10.gif"
IMAGE_WATER1 = "images/water1.gif"
IMAGE_WATER2 = "images/water2.gif"
IMAGE_WATER3 = "images/water3.gif"
IMAGE_WATER4 = "images/water4.gif"
IMAGE_WATER5 = "images/water5.gif"
IMAGE_WATER6 = "images/water6.gif"
IMAGE_WATER7 = "images/water7.gif"
IMAGE_WATER8 = "images/water8.gif"
IMAGE_WATER9 = "images/water9.gif"
IMAGE_WATER10 = "images/water10.gif"