import sys
import tkinter as tk
from game_manger import GameManager
import global_variables as gv


def main():
    root = tk.Tk()
    root.title("Othello Game")

    # Create the GameManager instance
    game_manager = GameManager(root)

    # Center the main window on the screen
    window_width = 600
    window_height = 605
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Set minimum and maximum size of the root window to prevent resizing
    root.minsize(window_width, window_height)
    root.maxsize(window_width, window_height)
    root.resizable(False, False)  # Disable resizing

    # Start the main event loop
    root.mainloop()

    # After the main loop exits (window closed), check if difficulty was set
    if gv.diff == -1:
        # User closed the difficulty selection without choosing
        print("No difficulty selected. Exiting...")
        sys.exit(0)  # Exit the application gracefully


if __name__ == "__main__":
    main()

    
