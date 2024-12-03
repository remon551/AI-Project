import sys
import tkinter as tk
from color import Color
from disk import Disk
import global_variables as gv


def on_window_close():
    print("Exiting...")
    sys.exit(0)  # Exit the application gracefully


class RestartWindow:
    def __init__(self, root, gm, winner):
        self.gm = gm
        self.root = root
        self.selection_window = tk.Toplevel(root)
        self.selection_window.title("Select Difficulty")

        # Calculate the position to center the window
        window_width = 200  # Width of the difficulty selection window
        window_height = 150  # Height of the difficulty selection window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)

        # Set the geometry of the window to center it on the screen
        self.selection_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Make the window modal (grab the focus)
        self.selection_window.grab_set()

        # Create a text widget to display instructions
        text_widget = tk.Label(self.selection_window, height=3, width=30)
        message = ""
        if winner == "Draw":
            message = winner
        else:
            message = f"winner is {winner}"
        text_widget.configure(text=f"{message}\nClick 'Restart' to start a new game.")

        text_widget.config(state=tk.DISABLED)  # Make the text widget read-only
        text_widget.pack(pady=10)

        # Create a restart button
        restart_button = tk.Button(self.selection_window, text="Restart", command=lambda: self.restart())
        restart_button.pack(pady=10)

        # Configure window close event to exit gracefully
        self.selection_window.protocol("WM_DELETE_WINDOW", on_window_close)

    def restart(self):
        self.gm.board.grid = [[' ' for _ in range(self.gm.board.columns)] for _ in range(self.gm.board.rows)]
        self.gm.board.valid = [[False for _ in range(self.gm.board.columns)] for _ in range(self.gm.board.rows)]

        black_disk1 = Disk(Color.BLACK)
        black_disk2 = Disk(Color.BLACK)
        white_disk1 = Disk(Color.WHITE)
        white_disk2 = Disk(Color.WHITE)
        self.gm.board.grid[3][3] = black_disk1
        self.gm.board.grid[4][4] = black_disk2
        self.gm.board.grid[3][4] = white_disk1
        self.gm.board.grid[4][3] = white_disk2
        self.gm.update_ui()
        self.gm.num_of_disks = 4
        gv.blackTurn = True
        self.gm.turn_label.configure(text=f"Black Turn\nBlack Score: {gv.blackScore}\nWhite Score: {gv.whiteScore}")

        self.selection_window.destroy()