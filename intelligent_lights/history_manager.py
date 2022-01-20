class HistoryManager:
    def __init__(self):
        self.grid = [[0] * 50 for _ in range(100)]

    def update(self, visible):
        for position in visible:
            self.grid[position[0]][position[1]] += 5