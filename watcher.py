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

    def getParameters(parameterMap, defaults, arguments):
        def parseArgs(args):
            index = 0
            parameters = {}
            while args[index][0] == '-':
                parameters[parameterMap[args[index]]] = args[index+1]
                index += 2

            parameters['rest'] = ' '.join(args[index:])
            return parameters

        suppliedParameters = parseArgs(arguments)
        parameters = {
            'rest': suppliedParameters['rest']
        }

        for (key, value) in defaultParameters.items():
            parameters[key] = suppliedParameters[key] if key in suppliedParameters else defaultParameters[key]

        return parameters

    parameterMap = {
        '-d': 'path',
        '-w': 'watch',
        '-i': 'ignore'
    }

    defaultParameters = {
        'path': basePath,
        'watch': '*',
        'ignore': [
            os.path.join(basePath, '.git', '*'),
            os.path.join(basePath, '.#*'),
            os.path.join(basePath, '*', '.#*')
        ]
    }

    parameters = getParameters(parameterMap, defaultParameters, sys.argv[1:])
    command = getRunCommand(parameters['rest'])
    doCommandSoon = debounce(command, 0.05)

    print "Watching path ", parameters['path'], ", Ignoring patterns", parameters['ignore']
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
