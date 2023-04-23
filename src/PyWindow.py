import PySimpleGUI as sg
from StickyNotes import StickyNotes
from subprocess import CREATE_NEW_CONSOLE, Popen
import webbrowser
import os 
from Autosuggest import Autosuggest 
from TreeDataNode import TreeDataNode
from typing import Optional, Any, Callable
from helpers import create_window, should_close, split_input_into_keyword_query


class PyWindow():

    def __init__(self, autosuggest: Autosuggest) -> None:

        self.autosuggest = autosuggest
        self.stickynotes = StickyNotes()
        self.window : sg.Window = create_window()
        self.current_index = 0
        self.events = []
        self.current_matches: dict[str, TreeDataNode] = {}
        self.tree = self.window["-TREE-"]
        self.keep_running = True
        self.tree_element = self.tree.Widget

    def run(self) -> None:
        self.keep_running = True
        while self.keep_running:
            event, values = self.window.read()
            self.events.append(event)
            input_text = values['-INPUT-']
            keyword, query = split_input_into_keyword_query(input_text)
            selected_treedatanode_key: Optional[list[str]] = None if len(input_text) == 0 else values['-TREE-']
            if event in ['-DOWN-', '-UP-']:
                self.__change_current_selection(event=event):
            elif should_close(events=self.events) or event in (sg.WINDOW_CLOSED, '-ESCAPE-'):
                self.__close()
            elif event == '-INPUT-':
                self.__update_tree(input=input_text, keyword=keyword, query=query)
            elif event == "-ENTER-" and selected_treedatanode_key is not None:
                selected_node = self.current_matches[selected_treedatanode_key[0]]
                self.activate(node=selected_node, keyword=keyword, query=query)

    def __close(self) -> None:
        self.window.close()
        self.__hide_tree()
        self.keep_running = False

    def activate(self, node: TreeDataNode, keyword: str, query: str) -> None:
        current_type = node.type
        actions: dict[str, Callable] = {
            'url': lambda arg=node.full_path: webbrowser.open_new(arg),
            'application': lambda arg=node.full_path: os.startfile(arg),
            'search': lambda arg=query: webbrowser.open_new(f"{node.full_path}{arg}"),
            'file': lambda arg=node.full_path: os.startfile(arg),
            'folder': lambda arg=node.full_path: os.startfile(arg),
            'keyword': lambda arg=keyword: self.__handle_keyword_workflow(node=node, keyword=arg)
        }
        if self.autosuggest.active_match is not None:
            self.__handle_arguments(node=node, active_match=self.autosuggest.active_match, query=query)
        else:
            if node.type == 'keyword':
                self.__hide_tree()
            else:
                self.__close()
            self.autosuggest.update_workflow_count(node=node)


    def __handle_arguments(self, node: TreeDataNode, active_match: TreeDataNode, query: str):
        actions: dict[str, Callable] = {
            'code': lambda arg= node.full_path: self.__open_with_vscode(dir_path=arg), 
            'cd': lambda arg=node.full_path: self.__open_terminal(dir_path=arg), 
            'project': lambda arg=node.full_path: self.__open_project(full_path=arg),
            'find': lambda arg=node.full_path: self__open_with_file_explorer(full_path=arg),
            'r': lambda arg=query: self.__create_stickynote(query=arg)
        }
        try: 
            actions[active_match.name]()
            self.autosuggest.update_workflow_count(node=active_match)
            self.__close()
        
        except KeyError as err:
            print(err)

    def __create_sticynote(self, query: str) -> None:
        self.stickynotes.create(text=query)

    def __open_with_file_explorer(self, full_path: str) -> None:
        Popen(f"explorer /select, '{full_path}")

    def __handle_keyword_workflow(self, node: TreeDataNode, keyword: str):
        if node.requires_args == 1:
            self.window['-INPUT-'].update(value=node.name + ' ')
            self.autosuggest.active_match = node
            self.autosuggest.expect_arguments = True

    def __open_project(self, full_path):
        self.__open_terminal(dir_path=full_path)
        self.__open_with_vscode(dir_path=full_path)

    @staticmethod
    def __open_terminal(dir_path) -> None:
        app_path = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
        cmd = [app_path]
        Popen(cmd, creationflags=CREATE_NEW_CONSOLE, cwd=dir_path)

    @staticmethod
    def __open_with_vscode(dir_path: str) -> None:
        app_path = "C:\\Program files\\Microsoft VS Code\\Code.exe"
        Popen([app_path, dir_path])

    
    def __update_tree(self, input: str, keyword: str, query: str) -> None:
        autosuggest_matches: list[TreeDataNode] = self.autosuggest.search(keyword=keyword, query=query)
        treedata, current_matches = self.__get_updated_treedata_nodes(autosuggest_matches=autosuggest_matches)
        if len(keyword) == 0 or len(current_matches) == 0:
            self.__hide_tree()
        else:
            self.current_index = 0
            self.current_matches = current_matches
            self.__show_tree(treedata=treedata)

    def __hide_tree(self) -> None:
        self.tree.update(visible=False)
        self.tree.hide_row()
        self.window.refresh()

    def __show_tree(self, treedata: sg.TreeData) -> None:
        self.tree.expand(expand_x=True)
        self.tree.unhide_row()
        self.tree.update(treedata, visible=True)
        updated_children = self.tree_element.get_children("")
        self.tree_element.selection_set(updated_children[0])
        self.window.refresh()

    @staticmethod
    def __get_updated_treedata_nodes(autosuggest_matches: list[TreeDataNode]) -> tuple[sg.TreeData, dict[str, TreeDataNode]]:
        treedata = sg.TreeData()
        current_matches : dict[str, TreeDataNode] = {}
        for node in autosuggest_matches:
            current_matches[node.key] = node
            treedata.insert(parent=node.parent, key=node.key, text=node.text, values=node.values, icon=node.icon)
        return (treedata, current_matches)

    def __change_current_selection(self, event):
        children = self.tree_element.get_children("")
        updated_index = self.__get_current_index(event=event, children=children, current_index=self.current_index)
        self.tree_element.selection_set(children[updated_index])
        self.tree_element.see(children[updated_index])
        self.current_index = updated_index
        self.window.refresh()

    @staticmethod
    def __get_current_index(event: str, children: tuple[str], current_index: int) -> int:
        result = current_index
        if event == "-DOWN-" and result < len(children) - 1:
            result += 1
        elif '-UP-' in event and result != 0:
            result -= 1

        return result
    


