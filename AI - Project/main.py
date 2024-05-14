import tkinter as tk
from game_manger import GameManager


def main():
    root = tk.Tk()
    root.title("Othello Game")

    # Create the GameManager instance
    GameManager(root)

    # Center the main window on the screen
    window_width = 600
    window_height = 620
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


if __name__ == "__main__":
    main()

    
