import tkinter as tk
from gui import MonitorGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorGUI(root)
    root.mainloop()