class PathSearch():
    """
    A class that implements the path search algorithm. To use this, you first must make
    an instance of the class, and then you call its search() method.
    """
    def __init__(self, neighbors_cb):
        """
        __init__(callback) -> None
        Constructor that stores a "neighbors_db" callback method. This callback method takes
        a node as a parameter and returns a list of the node's neighbors.
        """
        self.neighbors_cb = neighbors_cb

    def search(self, start, goal):
        """
        search(node, node) -> list
        The path search method that generates a path from the specified start node to the
        specified goal node. Note that this should return the full path including the
        start node and the end node.
        This relies on the neighbors_cb callback method having been set
        in the constructor when the class was instantiated.

        While this method is used in the simulation of this project specifically to
        find the path between cells in the world, you must implement this method
        without any dependencies on the simulation, the world, or the cells. That is,
        you must implement this in a generic fashion using only:
          * The starting node which is specified by the <start> argument.
          * The goal node which is specified by the <goal> argument. You know
            you have found a path to your goal when you have discovered node
            on your path that is equal to <goal>.
          * The neighbors_cb callback method. This is crucial because for any
            given node, this tells you the node's neighbors. It is used to determine
            additional nodes to consider adding to the frontier - which will be used
            to generate paths to the goal.
        """
        frontier = [[start]]    # Frontier contains list of paths
        visited = []            # List of visited paths
        while frontier:
            path = frontier.pop(0)
            last_node = path[-1]
            if last_node == goal:
                return path
            else:
                for neighbor in self.neighbors_cb(last_node):
                    # TODO: Don't add neighbors to path if they are not traversable  (add traversable to cells)
                    if not neighbor in path:
                        new_path = list(path)
                        new_path.append(neighbor)
                        if (new_path not in frontier) and (new_path not in visited):
                            frontier.append(new_path)
                visited.append(path)
#            self.debug_path_search(path, frontier, visited)

    def debug_path_search(self, path, frontier, visited):
        """
        Utility function that you can choose to use if you like to help debug your
        path_search code. Given three variables holding the path, frontier and visited,
        this prints out those 3 data structures in a reasonably pretty format. It
        assumes that the 3 variables are as follows:
          - path: A list of nodes
          - frontier: A list of paths (i.e., a list of list of nodes)
          - visited: A list of paths (i.e., a list of list of nodes)
        This assumes that nodes have instance variables named <row> and <col>,
        as defined in the PathSearchTest class below.  That is, this is useful
        during development when you are testing with PathSearchTest, but not
        when you are using the simulation since the simulation nodes don't have
        instance variables named <row> and <col>.
        """
        print "Path: "
        print "    ",
        for p in path:
            print "(" + str(p.row) + ", " + str(p.col) + ") | ",
        print ""
        print "Frontier: "
        for f in frontier:
            print "    ",
            for n in f:
                print "(" + str(n.row) + ", " + str(n.col) + ") | ",
            print ""
        print "Visited: "
        for v in visited:
            print "    ",
            for n in v:
                print "(" + str(n.row) + ", " + str(n.col) + ") | ",
            print ""
        print ""

from random import randint


class PathSearchTest():
    """
    A testing function to help test PathSearch.
    It uses a simple grid of cells with the following
    cell values:
      - empty cells will be a "."
      - start cell will be a "s",
      - goal cell will be a "g",
      - blocked cells that aren't allowed to be moved through are an "*"
      - cells along the path are a "-"
    """
    class TestCell():
        def __init__(self, row, col):
            self.value = "."
            self.row = row
            self.col = col

        def __str__(self):
            return self.value

    def __init__(self, size=10, blocked_cells=20):
        """
        Constructor sets up the class with a 2D grid of TestCell's.
        The cells in the grid are all empty (i.e., a ".") except for
        <blocked_cells> of them that will be set to "*"s.
        In addition, a stard and goal cell will be set and stored.
        """
        self.grid = []
        self.start_node = None
        self.goal_node = None

        # First set up empty grid
        for row_num in range(size):
            row = []
            for col_num in range(size):
                cell = self.TestCell(row_num, col_num)
                row.append(cell)
            self.grid.append(row)

        # Then set up the specified number of blocked cells
        # Define test grid
        num_rows = len(self.grid)
        num_cols = len(self.grid[0])

        for i in range(blocked_cells):
            blocked_row = randint(0, num_rows-1)
            blocked_col = randint(0, num_cols-1)
            self.grid[blocked_row][blocked_col].value = "*"

        # Finally, set up start and goal cells
        # Note that the start and goal cells might replace the blocked
        # cells in which case there will be fewer blocked cells than requested.
        start_row = randint(0, num_rows-1)
        start_col = randint(0, num_cols-1)
        self.start_node = self.grid[start_row][start_col]
        self.start_node.value = "s"

        goal_row = start_row
        goal_col = start_col
        while goal_row == start_row and goal_col == start_col:
            goal_row = randint(0, num_rows-1)
            goal_col = randint(0, num_cols-1)
            self.goal_node = self.grid[goal_row][goal_col]
            self.goal_node.value = "g"

    def __str__(self):
        result = ""
        for row in self.grid:
            for cell in row:
                result += str(cell) + " "
            result += "\n"
        return result

    def neighbors_cb(self, cell):
        """
        Returns the neighbors of a cell that are within the grid
        and that are not blocked.
        """
        neighbors = []
        row = cell.row
        col = cell.col
        if row > 0:
            north_cell = self.grid[row-1][col]
            if north_cell.value != "*":
                neighbors.append(north_cell)
        if row < len(self.grid) - 1:
            south_cell = self.grid[row+1][col]
            if south_cell.value != "*":
                neighbors.append(south_cell)
        if col > 0:
            west_cell = self.grid[row][col-1]
            if west_cell.value != "*":
                neighbors.append(west_cell)
        if col < len(self.grid[0]) - 1:
            east_cell = self.grid[row][col+1]
            if east_cell.value != "*":
                neighbors.append(east_cell)
        return neighbors

    def test(self):
        """
        Test the path search algorithm and print the original,
        randomy generated grid along with the solution.
        """
        print "Original Grid:"
        print self

        path_search = PathSearch(self.neighbors_cb)
        path = path_search.search(self.start_node, self.goal_node)
        for node in path[1:-1]:
            node.value = "-"

        print "Path:"
        print self

"""
The following code will test the PathSearch class, uncomment it out to test
but be sure to leave it commented before you submit your code to the submit server.
"""
# path_search_test = PathSearchTest()
# path_search_test.test()