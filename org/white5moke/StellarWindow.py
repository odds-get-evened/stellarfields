import json
import os.path
import re
import tkinter
import tkinter.constants
from datetime import datetime
from tkinter import Tk, BOTH, Scrollbar, RIGHT, LEFT, Y, Label, StringVar
from tkinter.ttk import Treeview, Frame, Progressbar


class StellarWindow:
    def __init__(self):
        self.events_we_need = [
            'Scan', 'FSSAllBodiesFound', 'FSSDiscoveryScan',
            'FSDJump', 'ApproachBody'
        ]

        self.last_load_label: Label = None
        self.last_update = None
        self.journal_tree_scroll: Scrollbar = None
        self.user_home_dir = None
        self.events = None
        self.current_journal = None
        self.journal_progress: Progressbar = None
        self.journal_tree: Treeview = None
        self.maine_frame = None
        self.scheduler = None

        self.root = Tk()
        #
        self.root.title("stellarfields")
        self.width = 480
        self.height = 640
        self.root.minsize(self.width, self.height)
        self.x = int(self.root.winfo_screenwidth() / 2 - self.width)
        self.y = int(self.root.winfo_screenheight() / 2 - self.height)
        self.root.geometry("{}x{}+{}+{}".format(self.width, self.height, self.x, self.y))

        self.boot_up()

        self.build()

        self.post_build()

        self.root.mainloop()

    def boot_up(self):
        self.user_home_dir = os.path.expanduser("~")
        if os.name == 'nt':  # Windows
            self.windows_boot()
        elif os.name == 'posix':
            # TODO : add Mac OS support
            pass
        else:
            pass

        self.last_update = StringVar()
        self.last_update.set(datetime.now().strftime("%H:%M.%S"))

    def windows_boot(self):
        saved_games_path = [
            os.path.join(self.user_home_dir, i)
            for i in os.listdir(self.user_home_dir)
            if i == 'Saved Games'
        ][0]
        ed_journals_path = os.path.join(saved_games_path, 'Frontier Developments', 'Elite Dangerous')
        pattern = re.compile("Journal\..*\.log")
        young_journal_filename = max(
            [
                (
                    os.path.getmtime(os.path.join(ed_journals_path, fname)),
                    os.path.join(ed_journals_path, fname)
                ) for fname in os.listdir(ed_journals_path) if pattern.search(fname)
            ]
        )[1]
        self.current_journal = young_journal_filename
        with open(self.current_journal, 'r', encoding='utf8') as f:
            self.events = [json.loads(line) for line in f.readlines()]
        f.close()

    def build(self):
        self.maine_frame = Frame(self.root)

        self.journal_tree = Treeview(self.maine_frame, selectmode='browse')
        self.journal_tree.pack(expand=True, fill=BOTH, side=LEFT)
        self.journal_tree['show'] = 'headings'
        self.journal_tree['columns'] = (1, 2)
        self.journal_tree.heading(1, text="time")
        self.journal_tree.heading(2, text="type")
        self.journal_tree.bind('<ButtonRelease-1>', self.event_item_selection)

        self.journal_tree_scroll = Scrollbar(self.maine_frame, orient=tkinter.VERTICAL, command=self.journal_tree.yview)
        self.journal_tree.configure(yscrollcommand=self.journal_tree_scroll.set)
        self.journal_tree_scroll.pack(side=RIGHT, expand=False, fill=Y)

        some_stuff_frame: Frame = Frame(self.root)
        placeholder = Label(some_stuff_frame, text="placeholder")
        placeholder.pack()
        self.last_load_label = Label(some_stuff_frame, textvariable=self.last_update)
        self.last_load_label.pack()
        some_stuff_frame.pack(fill=BOTH, side=tkinter.BOTTOM)

        self.maine_frame.pack(expand=True, fill=BOTH)

    def post_build(self):
        self.timed_update_events()

    def timed_update_events(self):
        self.update_events()
        self.last_update.set(datetime.now().strftime("%H:%M.%S"))
        print("updated: " + datetime.now().strftime("%H:%M.%S"))

    def update_events(self):
        self.clear_journal_tree()
        [self.journal_tree.insert('', tkinter.END, values=(e['timestamp'], e['event'])) for e in
         self.events if any([j == e['event'] for j in self.events_we_need])]

    def clear_journal_tree(self):
        [self.journal_tree.delete(e) for e in self.journal_tree.get_children()]

    def event_item_selection(self, e):
        selected_item = self.journal_tree.selection()[0]
