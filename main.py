#!/usr/bin/python

# system
import csv
import time

# pypi
from blargs import Parser

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileModifiedEvent
from watchdog.tricks import Trick

# local
import empiretrader

# ------------------------------------------------------------

file_dir  = '/Users/admin/Wine Files/drive_c/Program Files/Profiforex MT4/experts/files'
file_name = 'TradeCopy.csv'

file = '{0}/{1}'.format(file_dir, file_name)


class Trades(object):

    def __init__(self):
        self.trades = dict()

    def action_to_option(self, action):
        if action == '1':
            return 'put'
        elif action == '0':
            return 'call'
        else:
            raise("action {0} not recognized".format(action))

    def register_trade(self, all=False):
        f = open(file, 'r')
        print "F", f
        l = f.readline() # skip transaction count
        print "L", l
        print self.trades
        for line in f:
            print "length", len(line)
            if len(line) < 2: continue
            (trade_id, symbol, action,lot_size,price) = line.split(',')[:5]
            print trade_id, symbol, action,lot_size,price
            if not (action == '0' or action == '1'):
                #print 'o1'
                continue
            if trade_id in self.trades:
                print '\tSkipping'
                continue
            else:
                #print 'o3'
                self.trades[trade_id] = [self.action_to_option(action), symbol]
                if not all:
                    print "\tReturning this trade"
                    return self.trades[trade_id]

        return None




class MyEventHandler(Trick):

    def __init__(self, patterns=None, ignore_patterns=None,
               ignore_directories=False):
        super(MyEventHandler, self).__init__(patterns, ignore_patterns,
                                             ignore_directories)
        print "hi there"
        self.trades = Trades()


    def on_modified(self, event):
        print "hello"
        r = self.trades.register_trade()
        if r:
            print "Placing {0}".format(r)
            empiretrader.main(r[0])

if __name__ == "__main__":

    event_handler = MyEventHandler(patterns='*TradeCopy.csv')
    event_handler.trades.register_trade(True) # load all recorded trades

    observer = Observer()
    observer.schedule(event_handler, path=file_dir, recursive=False)
    observer.start()
    print "Observer started."
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print "Observer terminating."
