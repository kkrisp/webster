try:
    # python 3.x
    import tkinter as tk
    from tkinter import ttk
    print("TK Inter imported (python 3.x)")
except ImportError:
    # python 2.x
    import Tkinter as tk
    import ttk
    print("TK Inter imported (python 2.x)")

def shutdown_procedure(root):
    """Called, when the GUI is closed, a place to save config, shutdown properly"""
    #printer.save_config()
    print("Shutdown procedure...")
    root.destroy()

print("Program started...")
    
root = tk.Tk()
root.title("Webster")
root.geometry("700x350")

root.protocol("WM_DELETE_WINDOW", lambda: shutdown_procedure(root))
root.mainloop()