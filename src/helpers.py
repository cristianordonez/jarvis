from sqlite3 import Cursor
from subprocess import Popen
from typing import Any

import PySimpleGui as sg

from my_types import Colors
from TreeDataNode import TreeDataNode


def create_window() -> sg.Window:
    colors = get_color_theme()
    layout = [
        [create_input()],
        [create_tree()]]
    window= sg.Window("Window Title", layout, use_default_focus=False, no_titlebar=True, keep_on_top=True, finalize=True, element_padding=0, background_color=colors['background'], return_keyboard_events=True, margins=(12, 12), font=("Segoe UI", 20, "normal"))
    window['-INPUT-'].set_focus()
    window['-TREE-'].Widget.configure(show='tree')
    window.bind('<Down>', '-DOWN-')
    window.bind('<Up>', '-UP-')
    window.bind('<Escape>', '-ESCAPE-')
    window.bind('<Return>', '-ENTER-')
    window['-INPUT-'].bind('<Control-a>', handle_ctrl_a)
    return window

def create_input() -> sg.Input:
    colors = get_color_theme()
    input = sg.Input(
        focus=True, expand_x=True, text_color=colors['text'],
        enable_events=True, key='-INPUT-', background_color=colors['background'],border_width=0, justification='left'
    )
    return input

def create_tree() -> sg.Tree:
    treedata = sg.TreeData()
    colors = get_color_theme()
    tree = sg.Tree(treedata, headings=[], text_color=colors['text'], sbar_trough_color=colors['trough'], sbar_background_color=colors['scrollbar'], background_color=colors['background'], font=('Segoe UI', 10, 'normal'), sbar_width=2, sbar_arrow_width=4, key='-TREE-', visible=False, expand_y=True, expand_x=True, enable_events=True)

    return tree

def split_input_into_keyword_query(input: str) -> tuple[str, str]:
    keyword = input.split(' ')[0]
    query = input.split(' ')[1:]
    if len(query) != 0:
        query = ' '.join(query).lower()

    else:
        query = ''
    return (keyword, query)

def treedatanode_factory(cursor: Cursor, row):
    fields = [column[0] for column in cursor.description]
    dict = {key: value for key, value in zip(fields, row)}
    return TreeDataNode(
        internal={'description': dict['description'], 'type': dict['type'], 'count': dict['count'], 'full_path': dict['full_path'], 'name': dict['name'], 'requires_args': dict['requires_args'], 'argument_type': dict['argument_type']},
        icon=dict['icon'], key=dict['key'], text=dict['text']
    )

def handle_ctrl_a(window: Any, event: str, values: Any) -> None:
    if event == 'a' and values['-INPUT-']:
        window['-INPUT-'].Widget.tag_add('sel', '1.0', 'end')

def should_close(events) -> bool:
    return len(events) > 2 and events[-1] == ' ' and events[-2] == 'Alt_L:18'

def get_color_theme() -> Colors:
    return {
        'background': '#141414',
        'background_listbox': '#141414',
        'background_highlight': '#3d3d3d',
        'text': '#e4e6eb',
        'trough': '#141414',
        'text_selected': '#e4e6eb',
        'scrollbar': '#320064'
    }

def toggle_sticky_notes() -> None:
    Popen(r'explorer.exe shell:appsFolder\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe!App')



    