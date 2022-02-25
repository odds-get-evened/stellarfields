from threading import Thread
from tkinter import Tk, Frame, Scrollbar, NW, BOTH, CENTER, VERTICAL, Y, RIGHT, TOP
from tkinter.ttk import Treeview

from org.white5moke.journals import Journals


class StellarWindow:
    def __init__(self):
        self.journals_t = None
        self.journal_list = None
        self.event_items = list()
        self.event_table: Treeview = None
        self.event_scroll = None
        self.maine_frame = None

        self.journals = Journals()

        self.root = Tk()
        self.root.title("stellarfields")
        self.width = 400
        self.height = 640
        self.x = int(self.root.winfo_screenwidth() / 2 - self.width)
        self.y = int(self.root.winfo_screenheight() / 2 - self.height)
        self.root.geometry("{}x{}+{}+{}".format(self.width, self.height, self.x, self.y))

        self.start_journals_thread()

        self.build()

        self.root.mainloop()

    def start_journals_thread(self):
        print("spinning up journal thread...")
        self.journals_t = Thread(target=self.journals_thread)
        self.journals_t.start()
        self.root.after(200, self.check_journals_ready, self.journals_t)

    def journals_thread(self):
        self.journal_list = self.journals.acquire_journals()

    def check_journals_ready(self, thread: Thread):
        if thread.is_alive():
            self.root.after(200, self.check_journals_ready, self.journals_t)
        else:
            print("journals are ready.")
            """always retrieve most recently modified journal log"""
            the_files = sorted(self.journal_list, key=lambda j: j['timestamp'], reverse=True)[0]
            self.setup_journal(the_files['filename'])

    def setup_journal(self, filename):
        events: list[dict] = self.journals.read_journal(filename)
        for event in events:
            print(event)

    def build(self):
        self.maine_frame = Frame(self.root)
        self.event_scroll = Scrollbar(self.maine_frame)
        self.event_scroll.configure(orient=VERTICAL)
        self.event_scroll.pack(fill=Y, side=RIGHT)
        self.event_table = Treeview(self.maine_frame)
        event_table_columns = ("timestamp", "event",)
        [print(col) for col in event_table_columns]
        self.event_table['show'] = 'headings'
        self.event_table.pack(anchor=NW, expand=True, fill=BOTH, side=TOP)
        self.maine_frame.pack(expand=True, fill=BOTH, padx=10, pady=10, side=TOP)
