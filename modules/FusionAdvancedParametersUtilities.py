import adsk.core
import adsk.fusion
import adsk.cam

_app = adsk.core.Application.get()
_ui = _app.userInterface


def show_message(message: str, subs: tuple):
    msg = message.format(*subs)
    _ui.messageBox(msg)
