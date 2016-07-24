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
    parameterMap = {
        'd': 'path'
    }

    def parseArgs(args):
        index = 0
        parameters = {}
        while args[index][0] == '-':
            parameters[parameterMap[args[index][1]]] = args[index+1]
            index += 2

        parameters['command'] = ' '.join(args[index:])
        return parameters

    parameters = parseArgs(sys.argv[1:])
    path = parameters['path'] if 'path' in parameters else '.'
    command = getRunCommand(parameters['command'])
    doCommandSoon = debounce(command, 0.01)

    print "Watching path ", path
    eventHandler = FSCommandRunningEventHandler(doCommandSoon)

    observer = Observer()
    observer.schedule(eventHandler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
