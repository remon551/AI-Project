from disk import Disk


class Board:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]
        self.weights = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        self.valid = [[False for _ in range(self.columns)] for _ in range(self.rows)]

    def set_disk(self, i, j, color):
        if 0 <= i < self.rows and 0 <= j < self.columns:
            self.grid[i][j] = Disk(color)
        else:
            print(f"set_disk{i}, {j}: ")
            print("Invalid position.")

    def is_empty(self, i, j):
        if 0 <= i < self.rows and 0 <= j < self.columns:
            return self.grid[i][j] == ' '  # ' ' represents an empty cell
        else:
            print(f"is_empty{i}, {j}: ")
            print("Invalid position.")

    def get_disk(self, i, j):
        if 0 <= i < self.rows and 0 <= j < self.columns:
            return self.grid[i][j]
        else:
            print(f"get_disk{i}, {j}: ")
            print("Invalid position.")

    def set_weight(self, i, j, weight):
        if 0 <= i < self.rows and 0 <= j < self.columns:
            self.weights[i][j] = weight
        else:
            print(f"set_weight{i}, {j}: ")
            print("Invalid position.")

    def is_valid(self, i, j):
        if 0 <= i < self.rows and 0 <= j < self.columns:
            return self.valid[i][j]
        else:
            print(f"is_valid{i}, {j}: ")
            print("Invalid position.")

    def set_to_valid(self, i, j):
        if 0 <= i < self.rows and 0 <= j < self.columns:
            self.valid[i][j] = True
        else:
            print(f"set_to_valid{i}, {j}: ")
            print("Invalid position.")

    def set_to_not_valid(self, i, j):
        if 0 <= i < self.rows and 0 <= j < self.columns:
            self.valid[i][j] = False
        else:
            print(f"set_to_not_valid{i}, {j}: ")
            print("Invalid position.")

