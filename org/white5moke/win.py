from tkinter import Menu, Frame, N, W, E, S, BOTH, VERTICAL, RIGHT, Y, NO, CENTER, YES, X, TOP, NW
from tkinter.ttk import Style, Label, Button, LabelFrame, PanedWindow, Treeview, Scrollbar


class Win(Frame):
    def __init__(self, container):
        super().__init__(container)

        self.table = None
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

        base_frame = Frame(self, bg="red")
        base_frame.pack(anchor=NW, fill=BOTH)

        self.status_table(base_frame)

    def status_table(self, container: Frame):
        scrollbar = Scrollbar(container)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.table = Treeview(container, yscrollcommand=scrollbar.set)
        self.table.pack(anchor=NW, fill=BOTH)
        self.table['show'] = 'headings'

        scrollbar.config(command=self.table.yview)

        self.table['columns'] = ('events')
        self.table.column("events", anchor=CENTER, stretch=True)
        self.table.heading("events", text="events", anchor=CENTER)

    def exit_app(self):
        exit(0)
