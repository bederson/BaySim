# List indices for locations
ROW_INDEX = 0
COL_INDEX = 1

# Initial values
WORLD_WIDTH = 74
WORLD_HEIGHT = 99
CELL_SIZE = 8
NUM_FOODS = 100
NUM_BUILDINGS = 100
NUM_CRABS = 20
MIN_CRAB_DEPTH = 5

# Simulation constants
TERRAIN_SMOOTHNESS = 50.0           # Bigger values makes the terrain smoother
HUNGER_GROWTH = 0.01
FOOD_DEFAULT = -1.0
FOOD_GROWTH = 0.01        # Amount food grows per step
LEVEL_MAX = 4
STEP_TIME = 10           # In milliseconds
INIT_WATER_LEVEL = 0
EVAPORATION_RATE = 0.01
MAX_HEALTH = 10
MAX_POLLUTION = 10

# Water sources
WATER_SOURCES = [
[46, 14],
[51, 15],
[55, 13],
[60, 10],
[63, 7],
[70, 3],
[76, 5],
[64, 32],
[70, 33],
[73, 37],
[77, 40],
[22, 36],
[25, 38],
[27, 41],
[8, 60],
[11, 62],
[13, 62],
[32, 56],
[35, 54],
[38, 54],
[38, 52],
[48, 53],
[45, 52],
[44, 52],
[46, 49],
[61, 64],
[62, 59],
[59, 55],
[58, 51],
[66, 49],
[64, 48],
[64, 32],
[69, 33],
[71, 35],
[78, 37],
[78, 43]
]

DIRECTION_DELTAS = {
    'Left':  [0, -1],
    'Right': [0,  1],
    'Up':    [-1, 0],
    'Down':  [1,  0]
}

# Visual Display constants
METER_HEIGHT = 5

# Image filenames
IMAGE_CRAB1 = "images/crab1.gif"
IMAGE_CRAB2 = "images/crab2.gif"
IMAGE_CRAB3 = "images/crab3.gif"
IMAGE_CRAB4 = "images/crab4.gif"
IMAGE_CRAB5 = "images/crab5.gif"
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
IMAGE_POLLUTION1 = "images/pollution1.gif"
IMAGE_POLLUTION2 = "images/pollution2.gif"
IMAGE_POLLUTION3 = "images/pollution3.gif"
IMAGE_POLLUTION4 = "images/pollution4.gif"
IMAGE_POLLUTION5 = "images/pollution5.gif"
IMAGE_POLLUTION6 = "images/pollution6.gif"
IMAGE_POLLUTION7 = "images/pollution7.gif"
IMAGE_POLLUTION8 = "images/pollution8.gif"
IMAGE_POLLUTION9 = "images/pollution9.gif"
IMAGE_POLLUTION10 = "images/pollution10.gif"
IMAGE_BUILDING = "images/building.gif"
