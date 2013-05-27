
file_dir  = '~/Wine Files/drive_c/Program Files/Profiforex MT4/experts/files/'
file_name = 'TradeCopy.csv'

file = '{0}/{1}'.format(file_dir, file_name)

import csv
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileModifiedEvent
from watchdog.tricks import LoggerTrick

class Trades(object):

    def __init__(self):
        self.trades = dict()

    def action_to_option(self, action):
        if action:
            return 'sell'
        else:
            return 'buy'

    def register_trades(self):
        new_trade
        f = open(file_name, 'r')
        f.readline() # skip transaction count
        for line in f:
            (trade_id, symbol, action) = line.split(',')
            if not (action == 0 or action == 1):
                continue
            if trade_id in self.trades:
                continue
            else:
                self.trades[trade_id] = [self.action_to_option(action), symbol]
                return self.trades[trade_id]

        return None




class MyEventHandler(LoggerTrick):

    def on_modified(self, event):
        r = self.trades.register_trades()
        if r:
            print "Placing {0}".format(r)

if __name__ == "__main__":

    t = Trades()

    event_handler = MyEventHandler(patterns='*.csv')
    event_handler.trades = t

    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print "hello. how are you?"
