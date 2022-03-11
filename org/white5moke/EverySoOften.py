from threading import Thread
import time


class EverySoOften(Thread):
    def __init__(self, seconds: int):
        '''
        note that when you override __init__, you must use
        super() to call __init__() in the base class so you'll
        get all  the goodness of threading or it won't work.
        '''
        super().__init__()
        self.delay = seconds
        self.is_done = False

    def done(self):
        self.is_done = True

    def run(self) -> None:
        while not self.is_done:
            time.sleep(self.delay)
            print('do the thing you want to do every so often')
        print('thread is done')


t = EverySoOften(5)
t.start()

for count in range(100_000_000):
    prod = count * count
    if count % 10_000_000 == 0:
        print('multiplied up to ', count)
t.done()
