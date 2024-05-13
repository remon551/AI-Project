import tkinter as tk
from enum import Enum
from PIL import Image, ImageTk

blackTurn = True

class Disk:
    def __init__(self, color=None):
        self.color = color

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, new_color):
        self._color = new_color

    def flip(self):
        if self.color == "Black":
            self.color = "White"
        elif self.color == "White":
            self.color = "Black"

class Color(Enum):
    BLACK = 0
    WHITE = 1

class OthelloTileWeights(Enum):
    GRID00 = 16.16
    GRID01 = -3.03
    GRID02 = 0.99
    GRID03 = 0.43
    GRID10 = -4.12
    GRID11 = -1.81
    GRID12 = -0.08
    GRID13 = -0.27
    GRID20 = 1.33
    GRID21 = -0.04
    GRID22 = 0.51
    GRID23 = 0.07
    GRID30 = 0.63
    GRID31 = -0.18
    GRID32 = -0.04
    GRID33 = -0.01

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


class GameManager:
    def __init__(self, root):
        self.root = root
        self.board = Board(8, 8)
        self.num_of_disks = 0
        self.buttons = []
    
        grid_idx = 7
        
        for i in range(4):
            for j in range(4):
                weight_row = OthelloTileWeights[f"GRID{i}{j}"].value
                self.board.set_weight(i, j, weight_row)
                self.board.set_weight(grid_idx - i, j, weight_row)
                self.board.set_weight(i, grid_idx - j, weight_row)
                self.board.set_weight(grid_idx - i, grid_idx - j, weight_row)

                # elif i == 1:
                #     weight_row = OthelloTileWeights[f"GRID1{j}"].value
                #     self.board.set_weight(i, j, weight_row)
                #     self.board.set_weight(grid_idx - i, j, weight_row)
                #     self.board.set_weight(i, j + grid_idx, weight_row)
                #     self.board.set_weight(grid_idx - i, grid_idx - j, weight_row)
                # elif i == 2:
                #     weight_row = OthelloTileWeights[f"GRID2{j}"].value
                #     self.board.set_weight(i, j, weight_row)
                #     self.board.set_weight(grid_idx - i, j, weight_row)
                #     self.board.set_weight(i, grid_idx - j, weight_row)
                #     self.board.set_weight(grid_idx - i, grid_idx - j, weight_row)






                        
        # grid_idx = 7
        # for i in range(4):
        #     for j in range(4):
        #         if i == 0:
        #             weight_row = OthelloTileWeights[f"GRID0{j}"].value
        #             self.board.set_weight(i, j, weight_row)
        #             self.board.set_weight(i + grid_idx, j, weight_row)
        #             self.board.set_weight(i, grid_idx - j, weight_row)
        #             self.board.set_weight(i + grid_idx, grid_idx - j, weight_row)
        #         elif i == grid_idx:
        #             weight_row = OthelloTileWeights[f"GRID3{j}"].value
        #             self.board.set_weight(i, j, weight_row)
        #             self.board.set_weight(i + grid_idx, j, weight_row)
        #             self.board.set_weight(i, grid_idx - j, weight_row)
        #             self.board.set_weight(i + grid_idx, grid_idx - j, weight_row)
        #         else:
        #             # For other rows, set the weight based on the corresponding column index
        #             weight = OthelloTileWeights[f"GRID{i % 4}{j}"].value
        #             self.board.set_weight(i, j, weight)
        #             self.board.set_weight(i + grid_idx, j, weight)
        #             self.board.set_weight(i, grid_idx - j, weight)
        #             self.board.set_weight(i + grid_idx, grid_idx - j, weight)

        black_disk1 = Disk(Color.BLACK)
        black_disk2 = Disk(Color.BLACK)
        white_disk1 = Disk(Color.WHITE)
        white_disk2 = Disk(Color.WHITE)

        self.board.grid[3][3] = black_disk1
        self.board.grid[4][4] = black_disk2
        self.board.grid[3][4] = white_disk1
        self.board.grid[4][3] = white_disk2
        self.num_of_disks += 4


        for i in range(self.board.rows):
            buttons_row = []
            for j in range(self.board.columns):
                button = tk.Canvas(root, width=30, height=30, bg='green', highlightthickness=1,
                                    highlightbackground='black')
                button.grid(row=i, column=j, sticky="nsew")  # Use sticky to expand cells
                button.bind('<Button-1>', lambda event, r=i, c=j: self.play_at(r, c))
                buttons_row.append(button)
            self.buttons.append(buttons_row)

        # Configure rows and columns to expand with window resizing
        for i in range(self.board.rows):
            self.root.grid_rowconfigure(i, weight=1, minsize=30)  # Set minimum size for each row
        for j in range(self.board.columns):
            self.root.grid_columnconfigure(j, weight=1, minsize=30)  # Set minimum size for each column
        self.update_ui()

    def play_at(self, row, column):
        if not self.board.is_valid(row, column):
            return False
        

        global blackTurn
        # me ==> player1
        # opp ==> palyer2
        player1 = Color.BLACK if blackTurn else Color.WHITE
        player2 = Color.WHITE if blackTurn else Color.BLACK

        self.board.get_disk(row, column).color(player1)

        directions = [
            (-1, 0),  # Up
            (1, 0),  # Down
            (0, -1),  # Left
            (0, 1),  # Right
            (-1, -1),  # Top-left
            (-1, 1),  # Top-right
            (1, -1),  # Bottom-left
            (1, 1)  # Bottom-right
        ]

        # Check each direction for possible flips
        for di, dj in directions:
            x, y = row + di, column + dj
            to_flip = []

            # Move in the current direction until out of bounds or an empty cell is encountered
            while 0 <= x < self.board.rows and 0 <= y < self.board.columns:
                if self.board.get_disk(x, y).color == player2:
                    to_flip.append((x, y))
                elif self.board.get_disk(x, y).color == player1:
                    if to_flip:
                        # Flip opponent's tiles to current player's tiles
                        for flip_row, flip_col in to_flip:
                            self.board.get_disk(flip_row, flip_col).color(player1)
                    break
                else:
                    break

                x += di
                y += dj

        blackTurn = not blackTurn
        print(f"You clicked on {row} and {column}")
        self.update_ui()

    def check_if_valid_move(self, i, j):
        if self.board.is_empty(i, j):
            return False
        
        current_player = Color.BLACK if blackTurn else Color.WHITE
        opponent_player = Color.WHITE if blackTurn else Color.BLACK

        directions = [
            (-1, 0),  # Up
            (1, 0),  # Down
            (0, -1),  # Left
            (0, 1),  # Right
            (-1, -1),  # Top-left
            (-1, 1),  # Top-right
            (1, -1),  # Bottom-left
            (1, 1)  # Bottom-right
        ]

        valid_move = False

        # Check each direction for potential flips
        for di, dj in directions:
            x, y = i + di, j + dj
            found_opponent = False
            flip_candidates = []

            # Move in the current direction until out of bounds or an empty cell is encountered
            while 0 <= x < self.board.rows and 0 <= y < self.board.columns:
                if self.board.get_disk(i, j).color == opponent_player:
                    found_opponent = True
                    flip_candidates.append((x, y))
                elif self.board.get_disk(i, j).color == current_player:
                    if found_opponent and len(flip_candidates) > 0:
                        valid_move = True
                        break
                    else:
                        break
                else:
                    break

                x += di
                y += dj

            if valid_move:
                break

        return valid_move

    def calc_winner(self):
        black = 0
        white = 0
        for i in range(0, self.board.rows):
            for j in range(0, self.board.columns):
                if not self.board.is_empty(i, j):
                    if self.board.get_disk(i, j).color == Color.BLACK:
                        black = black+1
                    elif self.board.get_disk(i, j).color == Color.WHITE:
                        white = white+1
        if black > white:
            return "Black"
        elif white > black:
            return "White"
        else:
            return "Draw"

    def update_ui(self):
        found_valid_moves = False
        for i in range(self.board.rows):
            for j in range(self.board.columns):
                # to remove any cell that was valid before, maybe now it won't
                if self.board.is_valid(i, j):
                    self.board.set_disk(i, j, Disk())
                img_path = ""
                if not self.board.is_empty(i, j):
                    if self.board.get_disk(i, j).color == Color.BLACK:
                        img_path = "black.png"
                    elif self.board.get_disk(i, j).color == Color.WHITE:
                        img_path = "white.png"
                    else:
                        valid = self.check_if_valid_move(i, j)
                        if valid:
                            found_valid_moves = True
                            self.board.set_to_valid(i, j)
                            img_path = "dotted.png"

                if img_path != "":
                    img = Image.open(img_path)
                else:
                    img = Image.new("RGBA", (30, 30))  # Create empty image for Tile.EMPTY

                img = img.resize((28, 28))  # Resize image to fit button
                photo = ImageTk.PhotoImage(img)

                # Update button with the image
                canvas = self.buttons[i][j]
                canvas.delete("image")  # Delete existing image
                canvas.create_image(2, 2, anchor=tk.NW, image=photo, tags="image")
                canvas.image = photo  # Keep reference to prevent garbage collection
        if not found_valid_moves:
            winner = self.calc_winner()
            if winner == "Draw":
                print(winner)
            print(f'winner is {winner}')
    
    # def alpha_beta_prune(position, depth, alpha, beta, maximizing_player):
    #     if depth == 0 or game over in position:
    #         return static evaluation of position
    #     if maximizing_player:
    #         max_evaluation = -infinity
    #         for each child of position:
    #             eval = alpha_beta_prune(child, depth - 1, alpha, beta False)
    #             max_evaluation = max(max_evaluation, eval)
    #             alpha = max(alpha, eval)
    #             if beta <= alpha
    #                 break
    #         return max_evaluation
    #     else
    #         min_evaluation = +infinity
    #         for each child of position
    #             eval = alpha_beta_prune(chile, depth - 1,alpha, beta, True)
    #             min_evaluation = min(min_evaluation, eval)
    #             beta = min(beta, eval)
    #             if beta <= alpha
    #                 break
    #         return min_evaluation

def main():
    root = tk.Tk()
    root.title("Grid of Buttons with Images")

    manager = GameManager(root)

    # Set minimum size of root window to prevent resizing to less than desired grid size
    root.update_idletasks()  # Update to get correct window size after widgets are laid out
    root.minsize(root.winfo_reqwidth(), root.winfo_reqheight())

    root.mainloop()


if __name__ == "__main__":
    main()

    
