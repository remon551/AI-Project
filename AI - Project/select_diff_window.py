import tkinter as tk
import global_variables as gv


class SelectDifficultyWindow:
    def __init__(self, root):
        self.root = root
        self.selection_window = tk.Toplevel(root)
        self.selection_window.title("Select Difficulty")

        # Calculate the position to center the window
        window_width = 300  # Width of the difficulty selection window
        window_height = 200  # Height of the difficulty selection window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)

        # Set the geometry of the window to center it on the screen
        self.selection_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Make the window modal (grab the focus)
        self.selection_window.grab_set()

        # Create buttons in the selection window
        easy_button = tk.Button(self.selection_window, text="Easy", command=lambda: self.set_difficulty(1))
        medium_button = tk.Button(self.selection_window, text="Medium", command=lambda: self.set_difficulty(3))
        hard_button = tk.Button(self.selection_window, text="Hard", command=lambda: self.set_difficulty(5))

        easy_button.pack(pady=10)
        medium_button.pack(pady=10)
        hard_button.pack(pady=10)

    def set_difficulty(self, difficulty):
        gv.diff = difficulty
        self.selection_window.destroy()  # Destroy the window after setting the difficulty
