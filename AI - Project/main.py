import tkinter as tk
from enum import Enum
from PIL import Image, ImageTk

blackTurn = True


class Tile(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    VALID = 3


class GameManager:
    def __init__(self, root):
        self.root = root
        self.rows = 8
        self.columns = 8
        self.cellsInfo = []
        self.buttons = []

        for i in range(self.rows):
            row_info = []
            for j in range(self.columns):
                if (i == 3 and j == 3) or (i == 4 and j == 4):
                    row_info.append(Tile.BLACK)
                elif (i == 3 and j == 4) or (i == 4 and j == 3):
                    row_info.append(Tile.WHITE)
                else:
                    row_info.append(Tile.EMPTY)
            self.cellsInfo.append(row_info)

        for i in range(self.rows):
            buttons_row = []
            for j in range(self.columns):
                button = tk.Canvas(root, width=30, height=30, bg='green', highlightthickness=1,
                                   highlightbackground='black')
                button.grid(row=i, column=j, sticky="nsew")  # Use sticky to expand cells
                button.bind('<Button-1>', lambda event, r=i, c=j: self.play_at(r, c))
                buttons_row.append(button)
            self.buttons.append(buttons_row)

        # Configure rows and columns to expand with window resizing
        for i in range(self.rows):
            self.root.grid_rowconfigure(i, weight=1, minsize=30)  # Set minimum size for each row
        for j in range(self.columns):
            self.root.grid_columnconfigure(j, weight=1, minsize=30)  # Set minimum size for each column
        self.update_ui()

    def play_at(self, row, column):
        if self.cellsInfo[row][column] != Tile.VALID:
            return False

        global blackTurn
        me = Tile.BLACK if blackTurn else Tile.WHITE
        opp = Tile.WHITE if blackTurn else Tile.BLACK

        self.cellsInfo[row][column] = me

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
            while 0 <= x < self.rows and 0 <= y < self.columns:
                if self.cellsInfo[x][y] == opp:
                    to_flip.append((x, y))
                elif self.cellsInfo[x][y] == me:
                    if to_flip:
                        # Flip opponent's tiles to current player's tiles
                        for flip_row, flip_col in to_flip:
                            self.cellsInfo[flip_row][flip_col] = me
                    break
                else:
                    break

                x += di
                y += dj

        blackTurn = not blackTurn
        print(f"You clicked on {row} and {column}")
        self.update_ui()

    def check_if_valid_move(self, i, j):
        if self.cellsInfo[i][j] != Tile.EMPTY:
            return False  # Cell must be empty to place a new tile

        current_player = Tile.BLACK if blackTurn else Tile.WHITE
        opponent_player = Tile.WHITE if blackTurn else Tile.BLACK

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
            while 0 <= x < self.rows and 0 <= y < self.columns:
                if self.cellsInfo[x][y] == opponent_player:
                    found_opponent = True
                    flip_candidates.append((x, y))
                elif self.cellsInfo[x][y] == current_player:
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
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                if self.cellsInfo[i][j] == Tile.BLACK:
                    black = black+1
                elif self.cellsInfo[i][j] == Tile.WHITE:
                    white = white+1
        if black > white:
            return "Black"
        elif white > black:
            return "White"
        else:
            return "Draw"

    def update_ui(self):
        found_valid_moves = False
        for i in range(self.rows):
            for j in range(self.columns):
                # to remove any cell that was valid before, maybe now it won't
                if self.cellsInfo[i][j] == Tile.VALID:
                    self.cellsInfo[i][j] = Tile.EMPTY
                img_path = ""
                if self.cellsInfo[i][j] == Tile.BLACK:
                    img_path = "black.png"
                elif self.cellsInfo[i][j] == Tile.WHITE:
                    img_path = "white.png"
                else:
                    valid = self.check_if_valid_move(i, j)
                    if valid:
                        found_valid_moves = True
                        self.cellsInfo[i][j] = Tile.VALID
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
