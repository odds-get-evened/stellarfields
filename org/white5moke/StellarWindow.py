import json
import os.path
import re
import tkinter.constants
from tkinter import Tk, BOTH, TOP, X, Scrollbar, RIGHT, LEFT, NW, Y
from tkinter.ttk import Treeview, Frame, Progressbar


class StellarWindow:
    def __init__(self):
        self.journal_tree_scroll: Scrollbar = None
        self.user_home_dir = None
        self.events = None
        self.current_journal = None
        self.journal_progress: Progressbar = None
        self.journal_tree: Treeview = None
        self.maine_frame = None

        self.root = Tk()
        #
        self.root.title("stellarfields")
        self.width = 400
        self.height = 640
        self.x = int(self.root.winfo_screenwidth() / 2 - self.width)
        self.y = int(self.root.winfo_screenheight() / 2 - self.height)
        self.root.geometry("{}x{}+{}+{}".format(self.width, self.height, self.x, self.y))

        self.bootup()

        self.build()
        self.root.mainloop()

    def bootup(self):
        self.user_home_dir = os.path.expanduser("~")
        if os.name == 'nt':  # Windows
            self.windows_boot()
        elif os.name == 'posix':
            # TODO : add Mac OS support
            pass
        else:
            pass
        
    def windows_boot(self):
        saved_games_path = [os.path.join(self.user_home_dir, i) for i in os.listdir(self.user_home_dir) if i == 'Saved Games'][0]
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
        with open(self.current_journal, 'r') as f:
            self.events = [json.loads(line) for line in f.readlines()]
        f.close()
        # print(self.events)

    def update_events_table(self, events):
        for i, event in enumerate(events):
            # print(event['event'])
            self.journal_tree.insert('', index=i, values=(event['timestamp'], event['event']))

    def build(self):
        self.maine_frame = Frame(self.root)

        self.journal_tree = Treeview(self.maine_frame)
        self.journal_tree.pack(side=LEFT, fill=BOTH)

        self.journal_tree_scroll = Scrollbar(self.maine_frame, orient='vertical', command=self.journal_tree.yview)
        self.journal_tree_scroll.pack(side=RIGHT, fill=Y)
        self.journal_tree.configure(xscrollcommand=self.journal_tree_scroll.set)

        self.journal_tree['show'] = 'headings'
        self.journal_tree['columns'] = (1, 2)
        self.journal_tree.heading(1, text="time")
        self.journal_tree.heading(2, text="type")

        self.update_events_table(self.events)

        self.journal_progress = Progressbar(self.maine_frame,
                                            mode="indeterminate",
                                            orient="horizontal")
        # self.journal_progress.pack(expand=False, fill=X, pady=10)

        self.maine_frame.pack(expand=True, fill=BOTH, padx=10, pady=10, side=TOP)
