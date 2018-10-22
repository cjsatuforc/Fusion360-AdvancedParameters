# TODO: Need to handle errors while getting/setting parameters
import adsk.core
import adsk.fusion
import adsk.cam
import traceback
import threading
import time
import json
# from datetime import datetime
from queue import Queue
import ctypes

from .modules.Parameters import get_parameters_data, set_parameters
from .modules.FusionAdvancedParametersUtilities import show_message

_eventList = {}
_app = adsk.core.Application.cast(None)
_ui = adsk.core.UserInterface.cast(None)
_cmdDef = adsk.core.CommandDefinition.cast(None)
_passApCommandThread = None
_passApCommandThreadQueue = Queue()
_customApCommandEvent = None

_advancedParametersPalette = None

PROCESSAPCOMMANDEVENT = 'ProcessApCommandEvent'
ADVANCEDPARAMETERSPALETTE = 'advancedParametersPalette'
SHOWAPCOMMAND = 'ShowApPalette'
HTMLFILE = 'ui/FusionAdvancedParameters.html'


class ProcessApCommandEventHandler(adsk.core.CustomEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, eventArgs):
        try:
            args = adsk.core.CustomEventArgs.cast(eventArgs)
            command = json.loads(args.additionalInfo)
            action = command['action']
            commands = {
                'parameters': {
                    'get': get_parameters_data,
                    'set': set_parameters
                }
            }

            func = commands[action['item']][action['command']]

            arguments = action['arguments'] if 'arguments' \
                in action else []

            returnValues = func(arguments)
            returnDict = {
                'total': len(returnValues),
                'status': 'success',
                'records': returnValues
            }

            _advancedParametersPalette.sendInfoToHTML(json.dumps(action), json.dumps(returnDict))
        except:
            show_message('Failed to process the command:\n{}{}', (traceback.format_exc(), ''))


# worker thread
class PassHTMLCommandThread(threading.Thread):
    def __init__(self, queue):
        super(PassHTMLCommandThread, self).__init__()
        self.isStopped = False
        self.isPaused = False
        self.queue = queue

    def run(self):
        queue = self.queue
        try:
            while not self.isStopped:
                args = queue.get()

                if (not args == 'paused'):
                    time.sleep(.5)
                    print(dir(args))
                    _app.fireCustomEvent(PROCESSAPCOMMANDEVENT, args)

                while self.isPaused:
                    time.sleep(.25)

            if self.isStopped:
                ctypes.windll.user32.MessageBoxW(0, 'Stopped!', "Stopped!!", 1)

        except:
            ctypes.windll.user32.MessageBoxW(0, 'Failed:\n{}'.format(traceback.format_exc()), "Failed", 1)

    def stop(self):
        self.isStopped = True

    def pause(self):
        self.isPaused = True
        self.queue.put('paused')

    def resume(self):
        self.isPaused = False


# Event handler that is called when the add-in is destroyed.
# The custom event is unregistered here and the thread is stopped.
class MyDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        pass


# Event handler for the commandExecuted event.
class ShowApCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            if (not _passApCommandThread):
                initAdvancedParameters()
            else:
                _passApCommandThread.resume()
                _advancedParametersPalette.isVisible = True

        except:
            show_message('Failed to init Parameter Manager:\n{}', (traceback.format_exc()))


# Event handler for the commandCreated event.
class ShowApCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            command = args.command
            onExecute = ShowApCommandExecuteHandler()
            command.execute.add(onExecute)

            addEventReference(self.__class__.__name__, command, onExecute)
        except:
            show_message('Failed while trying to assign the execute handler:\n{}', (traceback.format_exc()))


# Event handler for the palette close event.
class ClosePaletteEventHandler(adsk.core.UserInterfaceGeneralEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            _passApCommandThread.pause()
        except:
            show_message('Failed while executing the close palette handler:\n', (traceback.format_exc()))


# Event handler for the palette HTML event.
class ClientEventHandler(adsk.core.HTMLEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            htmlArgs = adsk.core.HTMLEventArgs.cast(args)

            data = json.loads(htmlArgs.data)
            action = json.loads(htmlArgs.action)
            paramObj = {
                "data": data,
                "action": action
            }
            paramJSON = json.dumps(paramObj)

            global _passApCommandThread, _passApCommandThreadQueue

            if _passApCommandThread.isAlive():
                _passApCommandThreadQueue.put(paramJSON)
        except:
            show_message('Failure while handling incoming event from the HTML palette:\n{}', (traceback.format_exc()))


def initAdvancedParameters():
        global _eventList, _advancedParametersPalette, _passApCommandThread

        # Register the custom event and connect the handler.
        _customPMCommandEvent = _app.registerCustomEvent(PROCESSAPCOMMANDEVENT)
        onProcessHtml = ProcessApCommandEventHandler()
        _customPMCommandEvent.add(onProcessHtml)

        addEventReference(PROCESSAPCOMMANDEVENT, _customPMCommandEvent, onProcessHtml)

        # handlers.append(onProcessHtml)

        _passApCommandThread = PassHTMLCommandThread(_passApCommandThreadQueue)
        _passApCommandThread.start()

        # Create and display the palette.
        _advancedParametersPalette = _ui.palettes.add(ADVANCEDPARAMETERSPALETTE, 'Parameter Manager', HTMLFILE, True,
                                                      True, True, 1024, 768)

        # Dock the palette to the right side of Fusion window.
        _advancedParametersPalette.dockingState = adsk.core.PaletteDockingStates.PaletteDockStateRight

        # Add handler to HTMLEvent of the palette.
        onHTMLEvent = ClientEventHandler()
        _advancedParametersPalette.incomingFromHTML.add(onHTMLEvent)
        addEventReference(ADVANCEDPARAMETERSPALETTE + 'Incoming',
                          _advancedParametersPalette.incomingFromHTML, onHTMLEvent)

        onClosed = ClosePaletteEventHandler()
        _advancedParametersPalette.closed.add(onClosed)
        addEventReference(ADVANCEDPARAMETERSPALETTE + 'Closed', _advancedParametersPalette.closed, onClosed)

        # Allow page to init
        for i in range(30):
            print(i)
            time.sleep(0.1)
            adsk.doEvents()

        # Tell the ui that Fusion is ready to accept commands
        _advancedParametersPalette.sendInfoToHTML('{ "command": "init", "channel": "fusion", "topic": "init" }',
                                                  json.dumps({}))


def stopAdvancedParameters():
    global _advancedParametersPalette

    # Delete the palette created by this add-in.
    if _advancedParametersPalette:
        _advancedParametersPalette.deleteMe()
        _advancedParametersPalette = None

    # Delete controls and associated command definitions created by this add-ins
    panel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
    cntrl = panel.controls.itemById(SHOWAPCOMMAND)

    if cntrl:
        cntrl.deleteMe()

    cmdDef = _ui.commandDefinitions.itemById(SHOWAPCOMMAND)

    if cmdDef:
        cmdDef.deleteMe()

    try:
        _passApCommandThread.stop()
    except:
        show_message("Couldn't stop the thread:\n{}", (traceback.format_exc()))
        # _ui.messageBox("Couldn't stop the thread:\n{}".format(traceback.format_exc()))

    for key, event in _eventList.items():
        try:
            if (hasattr(event['command'], 'remove')):
                event['command'].remove(event['event'])
        except:
            show_message('Failed to remove event from command:\n{}', (traceback.format_exc()))

        try:
            _app.unregisterCustomEvent(event['name'])
        except:
            show_message('Failed to unregister custom event:\n{}', (traceback.format_exc()))

    _eventList.clear()


def addEventReference(name, command, event):
    global _eventList
    try:
        _eventList[name] = {
            'name': name,
            'command': command,
            'event': event
        }
    except:
        show_message('Could not add event reference:\n{}', (traceback.format_exc()))


def run(context):
    try:
        global _ui, _app
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        # Add a command that displays the panel.
        showPMCmdDef = _ui.commandDefinitions.itemById(SHOWAPCOMMAND)
        if not showPMCmdDef:
            showPMCmdDef = _ui.commandDefinitions.addButtonDefinition(SHOWAPCOMMAND, 'Open Parameter Manager',
                                                                      'Open Parameter Manager', '')

            # Connect to Command Created event.
            onCommandCreated = ShowApCommandCreatedHandler()
            showPMCmdDef.commandCreated.add(onCommandCreated)

            addEventReference(SHOWAPCOMMAND, showPMCmdDef.commandCreated, onCommandCreated)

        # Add the command to the toolbar.
        panel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        cntrl = panel.controls.itemById(SHOWAPCOMMAND)
        if not cntrl:
            panel.controls.addCommand(showPMCmdDef)

    except:
        show_message('Failed to run the addin:\n{}', (traceback.format_exc()))


def stop(context):
    try:
        stopAdvancedParameters()

    except:
        show_message('Failed to fully stop the addin:\n{}', (traceback.format_exc()))
