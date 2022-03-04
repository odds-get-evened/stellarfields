import shutil
from threading import Thread
from tkinter import Tk, BOTH, TOP, messagebox
from tkinter.ttk import Treeview, Label, Frame, Progressbar
from org.white5moke.journals import Journals, JSON_TIMESTAMP_NAME, JSON_EVENT_NAME
import json
# from tinydb import TinyDB, Query
import os
from datetime import datetime
import re


class StellarWindow:
    def __init__(self):
        self.user_home_path: bytes = None
        self.thread_journals: Thread = None
        self.journal_tree: Treeview = None
        self.journal_progress: Progressbar = None
        self.event_scroll = None
        self.maine_frame: Frame = None

        self.active_journal = None

        self.journals: Journals = Journals()

        # self.db = TinyDB()

        self.root = Tk()
        #
        self.root.protocol("WM_DELETE_WINDOW", self.close_up_shop)
        self.root.title("stellarfields")
        self.width = 400
        self.height = 640
        self.x = int(self.root.winfo_screenwidth() / 2 - self.width)
        self.y = int(self.root.winfo_screenheight() / 2 - self.height)
        self.root.geometry("{}x{}+{}+{}".format(self.width, self.height, self.x, self.y))
        self.setup()
        self.build()
        self.root.mainloop()

    def setup(self):
        self.user_home_path = os.path.join(os.path.expanduser("~"), ".stellarfields")
        if not os.path.exists(self.user_home_path):
            os.mkdir(self.user_home_path)
        current_log_path = os.path.join(self.user_home_path, "current.log")
        pattern = re.compile("Saved\sGames.*Elite\sDangerous$")
        if not os.path.exists(current_log_path):
            for root, dirs, files in os.walk(os.path.expanduser("~")):
                dirs = [dir_ for dir_ in dirs if dir_[:1] != '.']

                for dir__ in dirs:
                    full_path = os.path.join(root, dir__)
                    if pattern.search(str(full_path)):
                        self.user_home_path = full_path
                        youngest_file = max([(os.path.getmtime(os.path.join(self.user_home_path, fname)), fname) for fname in os.listdir(self.user_home_path)])[1]
                        print(youngest_file)
                        break


    def close_up_shop(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            self.root.destroy()

    def get_journal_thread(self):
        print("starting to acquire journals...")
        journals = self.journals.acquire_journals()
        filename = self.journals.acquire_active_journal()
        print(datetime.fromtimestamp(os.path.getmtime()).strftime("%H:%M.%S %Y-%m-%d"))
        """
        active = self.journals.read_journal(filename)
        self.journal_progress.stop()
        # print(json.dumps(active, indent=4))
        print("journals got got.")
        self.provide_events_to_table(json.dumps(active))
        self.active_journal = active
        """

    def provide_events_to_table(self, json_data):
        # convert string to json objects
        json_object = json.loads(json_data)
        for idx, ed_event in enumerate(json_object):
            # load up the table FFS!
            self.journal_tree.insert(
                '',
                index=idx,
                values=(ed_event[JSON_TIMESTAMP_NAME], ed_event[JSON_EVENT_NAME])
            )

    def get_journal(self):
        """
        TODO : decide between updating current journal or using old
            user file. need a way to use old file first, but trigger
            an update if needed in the background
        """
        self.journal_progress.start(5)
        self.thread_journals = Thread(target=self.get_journal_thread)
        self.thread_journals.start()

    def build(self):
        self.maine_frame = Frame(self.root)

        self.journal_tree = Treeview(self.maine_frame)
        self.journal_tree['show'] = 'headings'
        self.journal_tree['columns'] = (1, 2)
        self.journal_tree.heading(1, text="time")
        self.journal_tree.heading(2, text="type")
        self.journal_tree.pack()

        self.journal_progress = Progressbar(self.maine_frame,
                                            mode="indeterminate",
                                            orient="horizontal")
        self.journal_progress.pack()

        self.maine_frame.pack(expand=True, fill=BOTH, padx=10, pady=10, side=TOP)
