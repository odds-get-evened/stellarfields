import threading
from tkinter import *

# from matplotlib import pyplot as plt
from org.white5moke.journals import Journals
from org.white5moke.win import Win


def journals_startup():
    return Journals()


def main():
    journal_process = threading.Thread(target=journals_startup)
    journal_process.daemon = True
    journal_process.start()

    root = Tk()
    root.geometry("480x640+300+300")
    app = Win(root)
    app.pack()
    # displays the window
    root.mainloop()

    journal_process.join()


if __name__ == '__main__':
    main()
