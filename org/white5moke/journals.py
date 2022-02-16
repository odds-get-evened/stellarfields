import datetime
import json
import os
import re


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
