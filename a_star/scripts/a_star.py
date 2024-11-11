import heapq

class AStarPathFinding:
    def __init__(self, maze, start_pos, target_pos):
        self.maze = maze
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.open_list = []
        self.closed_list = set()
        self.came_from = {}

    def heuristic(self, a,b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def get_neighbors(self,pos):
        neighbors = []
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        for d in directions:
            neighbor = (pos[0] + d[0], pos[1] + d[1])
            if self.is_valid(neighbor):
                neighbors.append(neighbor)
        return neighbors
    
    def is_valid(self, pos):
        row, col = pos
        return 0 <= row < len(self.maze) and 0 <= col < len(self.maze[0]) and self.maze[row][col] == 1
    
    def find_path(self):
        heapq.heappush(self.open_list, (0, self.start_pos))

        g_score = {self.start_pos: 0}
        f_score = {self.start_pos: self.heuristic(self.start_pos, self.target_pos)}

        while self.open_list:
            _, current = heapq.heappop(self.open_list)

            if current == self.target_pos:
                return self.reconstruct_path(current)

            self.closed_list.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor in self.closed_list:
                    continue
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    self.came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, self.target_pos)
                    heapq.heappush(self.open_list, (f_score[neighbor], neighbor))

        return None
            
    def reconstruct_path(self, current):
        path = [current]

        while current in self.came_from:
            current = self.came_from[current]
            path.append(current)

        path.reverse()
        return path

if __name__ == "__main__":

    maze = [
        [1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 1],
        [0, 1, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1]
    ]

    start_pos = (0,0)
    target_pos = (7,7)

    path_finder = AStarPathFinding(maze, start_pos, target_pos)
    path = path_finder.find_path()

    if path:
        print("Path found: ", path)
    else:
        print("No path found")
