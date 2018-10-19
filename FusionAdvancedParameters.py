import adsk.core, adsk.fusion, adsk.cam # pylint: disable=import-error
import traceback
import threading, time, json
from datetime import datetime
from queue import Queue
import ctypes

# global set of event handlers to keep them referenced for the duration of the command
# handlers = []
# customHandlers = []
# htmlHandler = []
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
            # global ADVANCEDPARAMETERSPALETTE
            # action = command.action
            # data = json.loads(command.data)
            # data['requestId'] = action['requestId']

            jsonData = {
                "total": 45,
                "status": "success",
                "records": [
                    {
                        "ID": 1538197593990,
                        "Group": "Group 1",
                        "Name": "Name 1",
                        "Unit": "Unit 1",
                        "Expression": "Expression 1 is extra long, let's make it even longer so it wraps to account for those crazy expressions I write sometimes",
                        "Value": "Value 1",
                        "Comments": "Comment 1"
                    },
                    {
                        "ID": 1538197593991,
                        "Group": "Group 2",
                        "Name": "Name 2",
                        "Unit": "Unit 2",
                        "Expression": "Expression 2",
                        "Value": "Value 2",
                        "Comments": "Comment 2"
                    },
                    {
                        "ID": 1538197593992,
                        "Group": "Group 3",
                        "Name": "Name 3",
                        "Unit": "Unit 3",
                        "Expression": "Expression 3",
                        "Value": "Value 3",
                        "Comments": "Comment 3"
                    },
                    {
                        "ID": 1538197593993,
                        "Group": "Group 4",
                        "Name": "Name 4",
                        "Unit": "Unit 4",
                        "Expression": "Expression 4",
                        "Value": "Value 4",
                        "Comments": "Comment 4"
                    },
                    {
                        "ID": 1538197593994,
                        "Group": "Group 5",
                        "Name": "Name 5",
                        "Unit": "Unit 5",
                        "Expression": "Expression 5",
                        "Value": "Value 5",
                        "Comments": "Comment 5"
                    },
                    {
                        "ID": 1538197593995,
                        "Group": "Group 6",
                        "Name": "Name 6",
                        "Unit": "Unit 6",
                        "Expression": "Expression 6",
                        "Value": "Value 6",
                        "Comments": "Comment 6"
                    },
                    {
                        "ID": 1538197593996,
                        "Group": "Group 7",
                        "Name": "Name 7",
                        "Unit": "Unit 7",
                        "Expression": "Expression 7",
                        "Value": "Value 7",
                        "Comments": "Comment 7"
                    },
                    {
                        "ID": 1538197593997,
                        "Group": "Group 8",
                        "Name": "Name 8",
                        "Unit": "Unit 8",
                        "Expression": "Expression 8",
                        "Value": "Value 8",
                        "Comments": "Comment 8"
                    },
                    {
                        "ID": 1538197593998,
                        "Group": "Group 9",
                        "Name": "Name 9",
                        "Unit": "Unit 9",
                        "Expression": "Expression 9",
                        "Value": "Value 9",
                        "Comments": "Comment 9"
                    },
                    {
                        "ID": 1538197593999,
                        "Group": "Group 10",
                        "Name": "Name 10",
                        "Unit": "Unit 10",
                        "Expression": "Expression 10",
                        "Value": "Value 10",
                        "Comments": "Comment 10"
                    },
                    {
                        "ID": 1538197594000,
                        "Group": "Group 11",
                        "Name": "Name 11",
                        "Unit": "Unit 11",
                        "Expression": "Expression 11",
                        "Value": "Value 11",
                        "Comments": "Comment 11"
                    },
                    {
                        "ID": 1538197594001,
                        "Group": "Group 12",
                        "Name": "Name 12",
                        "Unit": "Unit 12",
                        "Expression": "Expression 12",
                        "Value": "Value 12",
                        "Comments": "Comment 12"
                    },
                    {
                        "ID": 1538197594002,
                        "Group": "Group 13",
                        "Name": "Name 13",
                        "Unit": "Unit 13",
                        "Expression": "Expression 13",
                        "Value": "Value 13",
                        "Comments": "Comment 13"
                    },
                    {
                        "ID": 1538197594003,
                        "Group": "Group 14",
                        "Name": "Name 14",
                        "Unit": "Unit 14",
                        "Expression": "Expression 14",
                        "Value": "Value 14",
                        "Comments": "Comment 14"
                    },
                    {
                        "ID": 1538197594004,
                        "Group": "Group 15",
                        "Name": "Name 15",
                        "Unit": "Unit 15",
                        "Expression": "Expression 15",
                        "Value": "Value 15",
                        "Comments": "Comment 15"
                    },
                    {
                        "ID": 1538197593990,
                        "Group": "Group 1",
                        "Name": "Name 1",
                        "Unit": "Unit 1",
                        "Expression": "Expression 1 is extra long",
                        "Value": "Value 1",
                        "Comments": "Comment 1"
                    },
                    {
                        "ID": 1538197593991,
                        "Group": "Group 2",
                        "Name": "Name 2",
                        "Unit": "Unit 2",
                        "Expression": "Expression 2",
                        "Value": "Value 2",
                        "Comments": "Comment 2"
                    },
                    {
                        "ID": 1538197593992,
                        "Group": "Group 3",
                        "Name": "Name 3",
                        "Unit": "Unit 3",
                        "Expression": "Expression 3",
                        "Value": "Value 3",
                        "Comments": "Comment 3"
                    },
                    {
                        "ID": 1538197593993,
                        "Group": "Group 4",
                        "Name": "Name 4",
                        "Unit": "Unit 4",
                        "Expression": "Expression 4",
                        "Value": "Value 4",
                        "Comments": "Comment 4"
                    },
                    {
                        "ID": 1538197593994,
                        "Group": "Group 5",
                        "Name": "Name 5",
                        "Unit": "Unit 5",
                        "Expression": "Expression 5",
                        "Value": "Value 5",
                        "Comments": "Comment 5"
                    },
                    {
                        "ID": 1538197593995,
                        "Group": "Group 6",
                        "Name": "Name 6",
                        "Unit": "Unit 6",
                        "Expression": "Expression 6",
                        "Value": "Value 6",
                        "Comments": "Comment 6"
                    },
                    {
                        "ID": 1538197593996,
                        "Group": "Group 7",
                        "Name": "Name 7",
                        "Unit": "Unit 7",
                        "Expression": "Expression 7",
                        "Value": "Value 7",
                        "Comments": "Comment 7"
                    },
                    {
                        "ID": 1538197593997,
                        "Group": "Group 8",
                        "Name": "Name 8",
                        "Unit": "Unit 8",
                        "Expression": "Expression 8",
                        "Value": "Value 8",
                        "Comments": "Comment 8"
                    },
                    {
                        "ID": 1538197593998,
                        "Group": "Group 9",
                        "Name": "Name 9",
                        "Unit": "Unit 9",
                        "Expression": "Expression 9",
                        "Value": "Value 9",
                        "Comments": "Comment 9"
                    },
                    {
                        "ID": 1538197593999,
                        "Group": "Group 10",
                        "Name": "Name 10",
                        "Unit": "Unit 10",
                        "Expression": "Expression 10",
                        "Value": "Value 10",
                        "Comments": "Comment 10"
                    },
                    {
                        "ID": 1538197594000,
                        "Group": "Group 11",
                        "Name": "Name 11",
                        "Unit": "Unit 11",
                        "Expression": "Expression 11",
                        "Value": "Value 11",
                        "Comments": "Comment 11"
                    },
                    {
                        "ID": 1538197594001,
                        "Group": "Group 12",
                        "Name": "Name 12",
                        "Unit": "Unit 12",
                        "Expression": "Expression 12",
                        "Value": "Value 12",
                        "Comments": "Comment 12"
                    },
                    {
                        "ID": 1538197594002,
                        "Group": "Group 13",
                        "Name": "Name 13",
                        "Unit": "Unit 13",
                        "Expression": "Expression 13",
                        "Value": "Value 13",
                        "Comments": "Comment 13"
                    },
                    {
                        "ID": 1538197594003,
                        "Group": "Group 14",
                        "Name": "Name 14",
                        "Unit": "Unit 14",
                        "Expression": "Expression 14",
                        "Value": "Value 14",
                        "Comments": "Comment 14"
                    },
                    {
                        "ID": 1538197594004,
                        "Group": "Group 15",
                        "Name": "Name 15",
                        "Unit": "Unit 15",
                        "Expression": "Expression 15",
                        "Value": "Value 15",
                        "Comments": "Comment 15"
                    },
                    {
                        "ID": 1538197593990,
                        "Group": "Group 1",
                        "Name": "Name 1",
                        "Unit": "Unit 1",
                        "Expression": "Expression 1 is extra long",
                        "Value": "Value 1",
                        "Comments": "Comment 1"
                    },
                    {
                        "ID": 1538197593991,
                        "Group": "Group 2",
                        "Name": "Name 2",
                        "Unit": "Unit 2",
                        "Expression": "Expression 2",
                        "Value": "Value 2",
                        "Comments": "Comment 2"
                    },
                    {
                        "ID": 1538197593992,
                        "Group": "Group 3",
                        "Name": "Name 3",
                        "Unit": "Unit 3",
                        "Expression": "Expression 3",
                        "Value": "Value 3",
                        "Comments": "Comment 3"
                    },
                    {
                        "ID": 1538197593993,
                        "Group": "Group 4",
                        "Name": "Name 4",
                        "Unit": "Unit 4",
                        "Expression": "Expression 4",
                        "Value": "Value 4",
                        "Comments": "Comment 4"
                    },
                    {
                        "ID": 1538197593994,
                        "Group": "Group 5",
                        "Name": "Name 5",
                        "Unit": "Unit 5",
                        "Expression": "Expression 5",
                        "Value": "Value 5",
                        "Comments": "Comment 5"
                    },
                    {
                        "ID": 1538197593995,
                        "Group": "Group 6",
                        "Name": "Name 6",
                        "Unit": "Unit 6",
                        "Expression": "Expression 6",
                        "Value": "Value 6",
                        "Comments": "Comment 6"
                    },
                    {
                        "ID": 1538197593996,
                        "Group": "Group 7",
                        "Name": "Name 7",
                        "Unit": "Unit 7",
                        "Expression": "Expression 7",
                        "Value": "Value 7",
                        "Comments": "Comment 7"
                    },
                    {
                        "ID": 1538197593997,
                        "Group": "Group 8",
                        "Name": "Name 8",
                        "Unit": "Unit 8",
                        "Expression": "Expression 8",
                        "Value": "Value 8",
                        "Comments": "Comment 8"
                    },
                    {
                        "ID": 1538197593998,
                        "Group": "Group 9",
                        "Name": "Name 9",
                        "Unit": "Unit 9",
                        "Expression": "Expression 9",
                        "Value": "Value 9",
                        "Comments": "Comment 9"
                    },
                    {
                        "ID": 1538197593999,
                        "Group": "Group 10",
                        "Name": "Name 10",
                        "Unit": "Unit 10",
                        "Expression": "Expression 10",
                        "Value": "Value 10",
                        "Comments": "Comment 10"
                    },
                    {
                        "ID": 1538197594000,
                        "Group": "Group 11",
                        "Name": "Name 11",
                        "Unit": "Unit 11",
                        "Expression": "Expression 11",
                        "Value": "Value 11",
                        "Comments": "Comment 11"
                    },
                    {
                        "ID": 1538197594001,
                        "Group": "Group 12",
                        "Name": "Name 12",
                        "Unit": "Unit 12",
                        "Expression": "Expression 12",
                        "Value": "Value 12",
                        "Comments": "Comment 12"
                    },
                    {
                        "ID": 1538197594002,
                        "Group": "Group 13",
                        "Name": "Name 13",
                        "Unit": "Unit 13",
                        "Expression": "Expression 13",
                        "Value": "Value 13",
                        "Comments": "Comment 13"
                    },
                    {
                        "ID": 1538197594003,
                        "Group": "Group 14",
                        "Name": "Name 14",
                        "Unit": "Unit 14",
                        "Expression": "Expression 14",
                        "Value": "Value 14",
                        "Comments": "Comment 14"
                    },
                    {
                        "ID": 1538197594004,
                        "Group": "Group 15",
                        "Name": "Name 15",
                        "Unit": "Unit 15",
                        "Expression": "Expression 15",
                        "Value": "Value 15",
                        "Comments": "Comment 15"
                    }
                ]
            }

            _advancedParametersPalette.sendInfoToHTML(json.dumps(command['action']), json.dumps(jsonData))
        except:
            if _ui:
                _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# worker thread
class PassHTMLCommandThread(threading.Thread):
    def __init__(self, queue):
        super(PassHTMLCommandThread, self).__init__()
        self.isStopped = False
        self.isPaused = False
        self.queue = queue
    def run(self):
        try:
            while not self.isStopped:
                queue = self.queue
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

# Event handler that is called when the add-in is destroyed. The custom event is
# unregistered here and the thread is stopped.
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
                initParameterManager()
            else:
                _passApCommandThread.resume()
                _advancedParametersPalette.isVisible = True
        except:
            _ui.messageBox('Failed to init Parameter Manager: {}'.format(traceback.format_exc()))


# Event handler for the commandCreated event.
class ShowApCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            # eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
            # inputs = eventArgs.command.commandInputs

            command = args.command
            onExecute = ShowApCommandExecuteHandler()
            command.execute.add(onExecute)
            # handlers.append(onExecute)

            addEventReference(self.__class__.__name__, command, onExecute)
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# Event handler for the palette close event.
class ClosePaletteEventHandler(adsk.core.UserInterfaceGeneralEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            _passApCommandThread.pause()
            # reset()
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Event handler for the palette HTML event.
class ClientEventHandler(adsk.core.HTMLEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            htmlArgs = adsk.core.HTMLEventArgs.cast(args)
            # data = json.dumps(htmlArgs.data)

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
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def initParameterManager():
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
        _advancedParametersPalette = _ui.palettes.add(ADVANCEDPARAMETERSPALETTE, 'Parameter Manager', HTMLFILE, True, True, True, 800, 600)

        # Dock the palette to the right side of Fusion window.
        _advancedParametersPalette.dockingState = adsk.core.PaletteDockingStates.PaletteDockStateRight

        # Add handler to HTMLEvent of the palette.
        onHTMLEvent = ClientEventHandler()
        _advancedParametersPalette.incomingFromHTML.add(onHTMLEvent)
        addEventReference(ADVANCEDPARAMETERSPALETTE + 'Incoming', _advancedParametersPalette.incomingFromHTML, onHTMLEvent)

        onClosed = ClosePaletteEventHandler()
        _advancedParametersPalette.closed.add(onClosed)
        addEventReference(ADVANCEDPARAMETERSPALETTE + 'Closed', _advancedParametersPalette.closed, onClosed)

        # Allow page to init
        for i in range(30): # pylint: disable=unused-variable
            print (i)
            time.sleep(0.1)
            adsk.doEvents()

        # Tell the ui that Fusion is ready to accept commands
        _advancedParametersPalette.sendInfoToHTML('{ "command": "init", "channel": "fusion", "topic": "init" }', json.dumps({}))


def addEventReference(name, command, event):
    global _eventList
    try:
        _eventList[name] = {
            'name': name,
            'command': command,
            'event': event
        }
    except:
        if _ui:
            _ui.messageBox('Could not add event reference:\n{}'.format(traceback.format_exc()))


def run(context):
    try:
        global _ui, _app
        _app = adsk.core.Application.get()
        _ui  = _app.userInterface

        # Add a command that displays the panel.
        showPMCmdDef = _ui.commandDefinitions.itemById(SHOWAPCOMMAND)
        if not showPMCmdDef:
            showPMCmdDef = _ui.commandDefinitions.addButtonDefinition(SHOWAPCOMMAND, 'Open Parameter Manager', 'Open Parameter Manager', '')

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
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    try:

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
            if _ui:
                _ui.messageBox("Couldn't stop the thread:\n{}".format(traceback.format_exc()))

        for key, event in _eventList.items():
            try:
                if (hasattr(event['command'], 'remove')):
                    event['command'].remove(event['event'])
            except:
                if _ui:
                    _ui.messageBox('Failed to remove event from command:\n{}'.format(traceback.format_exc()))
            try:
                _app.unregisterCustomEvent(event['name'])
            except:
                if _ui:
                    _ui.messageBox('Failed to unregister custom event:\n{}'.format(traceback.format_exc()))

        _eventList.clear()

        # _ui.messageBox('Stop addin')
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))