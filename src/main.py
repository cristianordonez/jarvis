from helpers import treedatanode_factory, toggly_sticky_notes
from pynput.keyboard import Key
from Workflows import Workflows
import os
from Autosuggest import Autosuggest
import sqlite3
import sys
from PyWindow import PyWindow
from pynput import pynput
from Hotkeys import Hotkeys

def toggle_jarvis(autosuggest: Autosuggest, listener: keyboard.Listener) -> None:
    listener.stop()
    pywindow = PyWindow(autosuggest = autosuggest)
    pywindow.run()

def initialize_hotkeys(keys: Hotkeys, autosuggest: Autosuggest, listener, keyboard.Listener) -> None:
    keys.register_hotkey(hotkeys = [Key.alt_l, Key.space], action=lambda arg=autosuggest: toggle_jarvis(autosuggest=arg, listener=listener))
    keys.register_hotkey(hotkeys = [Key.alt_gr, Key.space], action=lambda arg=autosuggest: toggle_jarvis(autosuggest=arg, listener=listener))
    keys.register_hotkey(hotkeys = [Key.alt_l, "`"], action=lambda toggle_sticky_notes())

def toggle_listener(connection: Connection, autosuggest: Autosuggest) -> None: 
    keys = Hotkeys()
    with keyboard.Events() as events:
        listener = keyboard.Listener()
        initialize_hotkeys(keys=keys, autosuggest=autosuggest, listener=listener)
        listener.start()
        while listener.is_alive():
            event = events.get()
            if event is not None:
                event_name = event.__class__.__name__
                if event.key == keyboard.Key.caps_lock:
                    connection.close()
                    sys.exit()
                elif event_name == "Press": 
                    keys.reset()
                else:
                    keys.add(key=event.key)
                    keys.call_hotkey()
            listener.join()

def main():
    connection = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'workflows.db'))
    connection.row_factory = treedatanode_factory
    cursor = connection.cursor()
    workflows = Workflows(cursor=cursor, connection=connection)
    autosuggest = Autosuggest(cursor=cursor)
    while True:
        toggle_listener(connection=connection, autosuggest=autosuggest)

if __name__ == "__main__":
    main()