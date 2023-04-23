from enum import Enum
from typing import Literal, Optional, TypedDict

from typing_extensions import NotRequired, Self


class Workflow_Type(Enum):
    url='url'
    application='application'
    query='query'
    file='file'
    directory='directory'
    keyword='keyword'
    search='search'

class Argument_Type(Enum):
    folder='folder'
    file='file'
    query='query'

class Bookmark(TypedDict):
    date_added: str
    date_last_used: str
    guid: str
    id: str
    meta_info: dict[str, str]
    name: str
    type: str
    children: NotRequired[list[Self]]
    url: str

class Colors(TypedDict):
    background: str
    background_listbox: str
    text: str
    scrollbar: str
    background_highlight: str
    text_selected: str
    trough: str

class NodeInternal(TypedDict):
    full_path: Optional[str]
    name: str
    description: str
    type: Literal['url', 'application', 'query', 'keyword', 'directory', 'search']
    argument_type: Optional[Literal['folder', 'file', 'query']]
    requires_args: Literal[0, 1]
    count: int

class Workflow(TypedDict):
    name: str
    key: str
    icon: str
    text: Optional[str]
    full_path: Optional[str]
    type: Literal['url', 'application', 'query', 'keyword', 'directory', 'search']
    description: str
    counter: NotRequired[int]
    requires_args: Literal[0, 1]
    argument_type: Optional[Literal['folder', 'file', 'query']]

class FileExplorereItem(TypedDict):
    full_path: str
    children: Optional[list[str]]
    basename: str

class StickyNoteRow(TypedDict):
    Text: str
    WindowPosition: str
    IsOpen: str
    IsAlwaysOnTop: str
    CreationNoteIdAnchor: str
    Theme: str
    IsFutureNote: str
    RemoteId:str
    ChangeKey: str
    LastServerVersion: str
    RemoteSchemeVersion: str
    IsRemoteDataInvalid: str
    Type: str
    Id: str
    ParentId: str
    CreatedAt: str
    DeletedAt: str
    UpdatedAt: str
