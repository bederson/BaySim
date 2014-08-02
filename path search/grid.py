from random import randint

from system import *
from path_search import PathSearch


class Cell(object):
    def __str__(self):
        return "-"

    def move_into(self):
        pass


class Food(Cell):
    def __init__(self, level):
        self.level = level

    def __str__(self):
        return str(self.level)

    def has_food(self):
        return self.level > 0

    def eat(self):
        if self.level > 0:
            self.level -= 1

    def move_into(self):
        if self.has_food():
            self.eat()
            print "Chomp!"


class SimpleGrid():
    DIM = 5                 # Member variable
    NUM_FOOD = 5
    DIRECTION_DELTAS = {    # Dictionary
        'left':  [0, -1],
        'right': [0, 1],
        'up':    [-1, 0],
        'down':  [1, 0]
    }

    def __init__(self):
        self.grid = self.gen_grid()
        self.me = [2, 2]
        self.system = System()
        self.system.add_callback(self.callback)

    def __str__(self):
        result = ""
        for row in range(SimpleGrid.DIM):
            for col in range(SimpleGrid.DIM):
                if self.me == [row, col]:
                    result += "* "
                else:
                    result += self.grid[row][col].__str__() + " "
            result += "\n"
        return result

    def gen_grid(self):
        # First generate black grid
        self.grid = []
        for row in range(SimpleGrid.DIM):
            row = []
            for col in range(SimpleGrid.DIM):
                row.append(Cell())
            self.grid.append(row)

        # Then insert some food
        for foodNum in range(SimpleGrid.NUM_FOOD):
            row = randint(0, SimpleGrid.DIM-1)
            col = randint(0, SimpleGrid.DIM-1)
            food = Food(randint(1, 5))
            self.grid[row][col] = food

        return self.grid

    def callback(self, event):
        if event == "go":
            self.go()
        elif event in SimpleGrid.DIRECTION_DELTAS:
            delta = SimpleGrid.DIRECTION_DELTAS[event]
            self.move(delta)
            print self

    def move(self, delta):
        new_row = self.me[0] + delta[0]
        new_col = self.me[1] + delta[1]
        if (0 <= new_row < SimpleGrid.DIM) and (0 <= new_col < SimpleGrid.DIM):     # Note simpler condition
            self.me = [new_row, new_col]
            cell = self.grid[new_row][new_col]
            cell.move_into()

    def neighbors(self, loc):
        locs = []
        for direction in SimpleGrid.DIRECTION_DELTAS:
            row = loc[0] + SimpleGrid.DIRECTION_DELTAS[direction][0]
            col = loc[1] + SimpleGrid.DIRECTION_DELTAS[direction][1]
            if (0 <= row < SimpleGrid.DIM) and (0 <= col < SimpleGrid.DIM):
                locs.append([row, col])
        return locs

    def find_most_food(self):
        max_food = 0
        food_row = None
        food_col = None
        for row_num, row in enumerate(self.grid):
            for col_num, cell in enumerate(row):
                if type(cell) is Food:
                    if cell.level > max_food:
                        max_food = cell.level
                        food_row = row_num
                        food_col = col_num
        if max_food > 0:
            return [food_row, food_col]
        else:
            return None

    def go(self):
        # First identify goal by finding cell with most food
        goal = self.find_most_food()

        # Then find path to that goal (if there is one)
        if goal:
            search = PathSearch(self.neighbors)
            path = search.search(self.me, goal)
            for loc in path:
                delta = [loc[0] - self.me[0], loc[1] - self.me[1]]
                self.move(delta)
                print world


world = SimpleGrid()
print world
world.system.main_loop()