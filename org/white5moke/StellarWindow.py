from threading import Thread
from tkinter import Tk, BOTH, TOP
from tkinter.ttk import Treeview, Label, Frame, Progressbar
from org.white5moke.journals import Journals, JSON_TIMESTAMP_NAME, JSON_EVENT_NAME
import json


class StellarWindow:
    def __init__(self):
        self.journal_tree: Treeview = None
        self.journal_progress: Progressbar = None
        self.event_scroll = None
        self.maine_frame: Frame = None

        self.active_journal = None

        self.journals: Journals = Journals()

        self.root = Tk()
        self.root.title("stellarfields")
        self.width = 400
        self.height = 640
        self.x = int(self.root.winfo_screenwidth() / 2 - self.width)
        self.y = int(self.root.winfo_screenheight() / 2 - self.height)
        self.root.geometry("{}x{}+{}+{}".format(self.width, self.height, self.x, self.y))
        self.build()
        self.root.mainloop()

    def get_journal_thread(self):
        print("starting to acquire journals...")
        journals = self.journals.acquire_journals()
        filename = self.journals.acquire_active_journal()
        active = self.journals.read_journal(filename)
        self.journal_progress.stop()
        # print(json.dumps(active, indent=4))
        print("journals got got.")
        self.provide_events_to_table(json.dumps(active))
        self.active_journal = active

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
        self.journal_progress.start(5)
        thread1 = Thread(target=self.get_journal_thread)
        thread1.start()

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
        self.get_journal()

        self.maine_frame.pack(expand=True, fill=BOTH, padx=10, pady=10, side=TOP)
