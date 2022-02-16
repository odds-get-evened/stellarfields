from tkinter import Menu, Frame, N, W, E, S, BOTH
from tkinter.ttk import Style


class Win(Frame):
    def __init__(self, container):
        super().__init__(container)

        self.init_ui()

    def init_ui(self):
        self.master.title("stellarfields")

        menu = Menu(self.master)
        self.master.configure(menu=menu)

        file_menu = Menu(menu)
        file_menu.add_command(label="Exit", command=self.exit_app)
        menu.add_cascade(label="File", menu=file_menu)

        self.pack(fill=BOTH, expand=1)

        Style().configure("TFrame", background="#333")

        base_frame = Frame(self)
        base_frame.grid(column=0, row=0, sticky=(N, W, E, S))

    def exit_app(self):
        exit(0)