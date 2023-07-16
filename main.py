import tkinter as tk
from ui import ui_principal
import config

def main():
    root = tk.Tk()
    # root.geometry("500x500+500+200")
    root.minsize(400, 450)
    root.maxsize(500, 500)
    #root.iconbitmap(default=config.ico)
    root.iconbitmap()
    root.title("Recetario")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    ui_principal.Principal(root).grid(sticky=tk.NSEW)
    root.mainloop()

if __name__ == "__main__":
    main()