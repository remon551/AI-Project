import tkinter as tk
from enum import Enum
from board import Board
from disk import Disk
from color import Color
from select_diff_window import SelectDifficultyWindow
from PIL import Image, ImageTk
import global_variables as gv


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


class GameManager:
    def __init__(self, root):
        print(gv.diff)
        self.root = root
        self.board = Board(8, 8)
        self.num_of_disks = 0
        self.buttons = []

        self.turn_label = tk.Label(root, height=1, width=20, )
        self.turn_label.configure(text="Black Turn")
        self.turn_label.grid(row=self.board.rows, columnspan=self.board.columns)

        for i in range(self.board.rows):
            buttons_row = []
            for j in range(self.board.columns):
                button = tk.Canvas(root, width=30, height=30, bg='green', highlightthickness=1,
                                   highlightbackground='black')
                button.grid(row=i, column=j, sticky="nsew")  # Use sticky to expand cells
                button.bind('<Button-1>', lambda event, r=i, c=j: self.play_at(r, c))
                buttons_row.append(button)
            self.buttons.append(buttons_row)

        grid_idx = 7
        for i in range(4):
            for j in range(4):
                weight_row = OthelloTileWeights[f"GRID{i}{j}"].value
                self.board.set_weight(i, j, weight_row)
                self.board.set_weight(grid_idx - i, j, weight_row)
                self.board.set_weight(i, grid_idx - j, weight_row)
                self.board.set_weight(grid_idx - i, grid_idx - j, weight_row)

        black_disk1 = Disk(Color.BLACK)
        black_disk2 = Disk(Color.BLACK)
        white_disk1 = Disk(Color.WHITE)
        white_disk2 = Disk(Color.WHITE)

        self.board.grid[3][3] = black_disk1
        self.board.grid[4][4] = black_disk2
        self.board.grid[3][4] = white_disk1
        self.board.grid[4][3] = white_disk2
        self.update_ui()
        self.num_of_disks += 4

        # Configure rows and columns to expand with window resizing
        for i in range(self.board.rows):
            self.root.grid_rowconfigure(i, weight=1, minsize=40)  # Set minimum size for each row
        for j in range(self.board.columns):
            self.root.grid_columnconfigure(j, weight=1, minsize=2)  # Set minimum size for each column
        self.update_ui()
        SelectDifficultyWindow(root)

    def play_at(self, row, column):
        if not self.board.is_valid(row, column):
            return False

        # me ==> player1
        # opp ==> player2
        player1 = Color.BLACK if gv.blackTurn else Color.WHITE
        player2 = Color.WHITE if gv.blackTurn else Color.BLACK

        self.board.set_disk(row, column, player1)
        self.num_of_disks += 1

        directions = [
            (-1, 0),  # Up
            (1, 0),  # Down
            (0, -1),  # Left
            (0, 1),  # Right
        ]

        # Check each direction for possible flips
        for di, dj in directions:
            x, y = row + di, column + dj
            to_flip = []

            # Move in the current direction until out of bounds or an empty cell is encountered
            while 0 <= x < self.board.rows and 0 <= y < self.board.columns:
                if not self.board.is_empty(x, y):
                    if self.board.get_disk(x, y).color == player2:
                        to_flip.append((x, y))
                    elif self.board.get_disk(x, y).color == player1:
                        if to_flip:
                            # Flip opponent's tiles to current player's tiles
                            for flip_row, flip_col in to_flip:
                                self.board.get_disk(flip_row, flip_col).flip()
                        break
                    else:
                        break

                x += di
                y += dj

        gv.blackTurn = not gv.blackTurn

        if not gv.blackTurn:
            self.turn_label.configure(text="White Turn")
        else:
            self.turn_label.configure(text="Black Turn")

        print(f"You clicked on {row} and {column}")
        self.update_ui()

    def check_if_valid_move(self, i, j):
        if not self.board.is_empty(i, j):
            return False

        current_player = Color.BLACK if gv.blackTurn else Color.WHITE
        opponent_player = Color.WHITE if gv.blackTurn else Color.BLACK

        directions = [
            (-1, 0),  # Up
            (1, 0),  # Down
            (0, -1),  # Left
            (0, 1),  # Right
        ]

        valid_move = False

        # Check each direction for potential flips
        for di, dj in directions:
            x, y = i + di, j + dj
            found_opponent = False
            flip_candidates = []

            # Move in the current direction until out of bounds or an empty cell is encountered
            while 0 <= x < self.board.rows and 0 <= y < self.board.columns:
                if not self.board.is_empty(x, y):
                    if self.board.get_disk(x, y).color == opponent_player:
                        found_opponent = True
                        flip_candidates.append((x, y))
                    elif self.board.get_disk(x, y).color == current_player:
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
                        black = black + 1
                    elif self.board.get_disk(i, j).color == Color.WHITE:
                        white = white + 1
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
                    self.board.set_to_not_valid(i, j)
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
                    img = Image.new("RGBA", (70, 70))  # Create empty image for Tile.EMPTY

                img = img.resize((70, 70))  # Resize image to fit button
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

    def alpha_beta_prune(self, position, depth, alpha, beta, maximizing_player):
        if depth == 0: # or calc winner
            return self.static_evaluation(position)

        if maximizing_player:
            max_evaluation = float('-inf')
            for child in self.generate_moves(position):
                eval = self.alpha_beta_prune(child, depth - 1, alpha, beta, False)
                max_evaluation = max(max_evaluation, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_evaluation
        else:
            min_evaluation = float('inf')
            for child in self.generate_moves(position):
                eval = self.alpha_beta_prune(child, depth - 1, alpha, beta, True)
                min_evaluation = min(min_evaluation, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_evaluation

    def generate_moves(self, position):
        # Generate all possible moves from the current position
        moves = []
        for i in range(self.board.rows):
            for j in range(self.board.columns):
                if self.check_if_valid_move(i, j):
                    # Create a copy of the current position and apply the move
                    new_position = position.copy()
                    new_position.set_disk(i, j, position.current_player)
                    moves.append(new_position)
        return moves

    def static_evaluation(self, position):
        black_score = 0
        white_score = 0

        for i in range(position.rows):
            for j in range(position.columns):
                disk = position.get_disk(i, j)
                if disk.color == Color.BLACK:
                    black_score += position.weights[i][j]
                elif disk.color == Color.WHITE:
                    white_score += position.weights[i][j]

        return black_score - white_score

    def find_best_move(self, position, depth):
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        maximizing_player = True

        for move in self.generate_moves(position):
            score = self.alpha_beta_prune(move, depth - 1, alpha, beta, maximizing_player)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move


