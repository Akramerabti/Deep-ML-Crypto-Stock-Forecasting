import tkinter as tk
from win32api import GetSystemMetrics
from gui import MainWindow

predictions_tab = None  # Define predictions_tab as a top-level attribute

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Stock Market Analysis")

    # Set the window size to the screen size (for Windows)
    if tk.TkVersion >= 8.6 or GetSystemMetrics is not None:
        screen_width = GetSystemMetrics(0)
        screen_height = GetSystemMetrics(1)
        window.geometry(f"{screen_width}x{screen_height}")
    else:
        # Fallback size if GetSystemMetrics is not available
        window.geometry("800x600")

    app = MainWindow(window)
    predictions_tab = app.predictions_tab  # Update predictions_tab from the instance
    window.mainloop()