import uuid

from org.white5moke.StellarWindow import StellarWindow

"""
creates a unique 64-bit integer (not truly random!)
"""


def random_int64() -> int:
    return uuid.uuid4().int >> 64


class App:
    def __init__(self):
        print(str(random_int64()))
        self.main_window = StellarWindow()
