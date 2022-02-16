import datetime
import json
import os.path
import re

from tkinter import *
from tkinter.ttk import *


# from matplotlib import pyplot as plt


class Win(Frame):
    def __init__(self, container):
        super().__init__(container)

        self.journals = Journals()

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


class Journals:
    def __init__(self):
        self.user_home_dir = os.path.expanduser("~")
        self.file_hold = []
        self.events = []

        self.acquire_journals()

    def read_journal(self, filename: str) -> list[dict]:
        with open(filename, "r") as file_:
            for line in file_:
                ed_event_dict = json.loads(line)
                self.events.append(ed_event_dict)

        return self.events

    def acquire_active_journal(self) -> str:
        res = max([(x['timestamp'], x) for x in self.file_hold])[1]

        return res['filename']

    def acquire_journals(self) -> list[dict]:
        dir_ = self.user_home_dir
        search_regex = re.compile("Journal\.(.*)\..*\.log")

        for root, dirs, files in os.walk(dir_):
            for f in files:
                match = search_regex.findall(f)
                if len(match) > 0:
                    timestamp = str(match[0]).strip()
                    journal_time = datetime.datetime.strptime(timestamp, '%y%m%d%H%M%S')
                    absolute_filename = os.path.join(root, f)
                    file_data = {'filename': absolute_filename, 'timestamp': journal_time.timestamp()}
                    self.file_hold.append(file_data)

        return self.file_hold


def main():
    root = Tk()
    root.geometry("440x480+300+300")
    app = Win(root)
    app.pack()
    # displays the window
    root.mainloop()


if __name__ == '__main__':
    main()
