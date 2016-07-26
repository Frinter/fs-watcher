import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from debounce import debounce

class CommandRunningEventHandler(PatternMatchingEventHandler):
    def __init__(self, command, watchPatterns, ignorePatterns):
        super(CommandRunningEventHandler, self).__init__(
            patterns=watchPatterns,
            ignore_patterns=ignorePatterns,
            ignore_directories=True
        )
        self.command = command

    def on_any_event(self, event):
        self.command()

def getRunCommand(command):
    def internalRun():
        os.system(command)
    return internalRun

if __name__ == '__main__':
    basePath = os.getcwd()

    parameters = {
        'path': basePath,
        'watch': [
            #os.path.join(basePath, '*'),
        ],
        'ignore': [
            os.path.join(basePath, '.git', '*'),
            os.path.join(basePath, '.#*'),
            os.path.join(basePath, '*', '.#*')
        ]
    }

    def parseArgs(args):
        index = 0
        while args[index][0] == '-':
            if args[index] == '-d':
                parameters['path'] = args[index+1]
                index += 1
            elif args[index] == '-w':
                parameters['watch'].append(args[index+1])
                index += 1
            elif args[index] == '-i':
                parameters['ignore'].append(args[index+1])
                index += 1
            index += 1

        parameters['rest'] = ' '.join(args[index:])

    parseArgs(sys.argv[1:])

    command = getRunCommand(parameters['rest'])
    doCommandSoon = debounce(command, 0.05)

    print "Watching path", parameters['path']
    print "Patterns", parameters['watch']
    print "Ignoring patterns", parameters['ignore']
    print "Will run command \"" + parameters['rest'] + "\""
    eventHandler = CommandRunningEventHandler(doCommandSoon, parameters['watch'], parameters['ignore'])

    observer = Observer()
    observer.schedule(eventHandler, parameters['path'], recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
