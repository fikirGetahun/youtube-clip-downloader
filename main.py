import sys
import os

# Step 1: Get the current directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Step 2: Create the full path to the 'libs' folder
libs_path = os.path.join(current_dir, "libs")

# Step 3: Add the 'libs' folder to Python's module search path
sys.path.insert(0, libs_path)

import tkinter as tk
from gui.gui import VideoDownloaderGUI
from backend.threading_manager import ThreadingManager

def main():
    # Initialize the main application window
    root = tk.Tk()

    # Set up the threading manager
    thread_manager = ThreadingManager()

    # Set up the GUI for the video downloader
    app = VideoDownloaderGUI(root)

    # Start the Tkinter main loop to run the application
    root.mainloop()

if __name__ == "__main__":
    main()


