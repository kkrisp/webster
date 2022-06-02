try:
    # python 3.x
    import tkinter as tk
    from tkinter import ttk
    print("TKInter imported (python 3.x)")
except ImportError:
    # python 2.x
    import Tkinter as tk
    import ttk
    print("TKInter imported (python 2.x)")

import world

def shutdown_procedure(root):
    """Called, when the GUI is closed, a place to save config, shutdown properly"""
    #printer.save_config()
    print("Shutdown procedure...")
    root.destroy()

print("Program started...")
    
root = tk.Tk()
root.title("Webster")
root.geometry("700x350")

world = world.World(root, 500, 200, 100, 30)
world.Init()

root.protocol("WM_DELETE_WINDOW", lambda: shutdown_procedure(root))
root.mainloop()
