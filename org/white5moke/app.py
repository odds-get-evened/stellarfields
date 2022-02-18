import threading
from tkinter import Tk

from org.white5moke.journals import Journals
from org.white5moke.win import Win


def journals_startup():
    return Journals()


class App:
    def __init__(self):
        journal_process = threading.Thread(target=journals_startup)
        journal_process.daemon = True
        # journal_process.start()

        root = Tk()
        tk_width = 480
        tk_height = 640
        tk_x = int(root.winfo_screenwidth() / 2 - tk_width)
        tk_y = int(root.winfo_screenheight() / 2 - tk_height)
        root.geometry("{}x{}+{}+{}".format(tk_width, tk_height, tk_x, tk_y))

        app = Win(root)
        app.pack()
        # displays the window
        root.mainloop()

        journal_process.join()
