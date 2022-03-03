import datetime
import json
import os
import re

JSON_TIMESTAMP_NAME = "timestamp"
JSON_EVENT_NAME = "event"


class Journals():
    def __init__(self):
        super().__init__()
        self.user_home_dir = os.path.expanduser("~")
        self.file_hold = []
        self.events = []

    def read_journal(self, filename: str) -> list[dict]:
        with open(filename, "r") as file_:
            for line in file_:
                ed_event_dict = json.loads(line)
                self.events.append(ed_event_dict)

        return self.events

    def acquire_active_journal(self) -> str:
        res = max([(x['timestamp'], x) for x in self.file_hold])[1]

        return res['filename']

    def acquire_journals(self):
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
