class PathSearch():
    def __init__(self, neighbors_cb):
        self.neighbors_cb = neighbors_cb

    def search(self, start, goal):
        frontier = [[start]]    # Frontier contains list of paths
        visited = []            # List of visited paths
        while frontier:
            path = frontier[0]
            frontier = frontier[1:]
            visited.append(path)
            last_node = path[-1:][0]
            if last_node == goal:
                return path
            else:
                for neighbor in self.neighbors_cb(last_node):
                    if not neighbor in path:
                        new_path = list(path)
                        new_path.append(neighbor)
                        if not new_path in visited:
                            frontier.append(new_path)