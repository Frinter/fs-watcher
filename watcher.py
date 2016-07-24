import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from debounce import debounce

class FSCommandRunningEventHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command

    def on_any_event(self, event):
        print event
        command()

def getRunCommand(command):
    def internalRun():
        os.system(command)
    return internalRun

if __name__ == '__main__':
    index = 1
    command = getRunCommand(' '.join(sys.argv[index:]))
    doCommandSoon = debounce(command, 0.01)
    eventHandler = FSCommandRunningEventHandler(doCommandSoon)

    observer = Observer()
    observer.schedule(eventHandler, '.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
