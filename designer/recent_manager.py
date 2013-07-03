import os
from functools import partial

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.listview import ListView, ListItemButton
from kivy.properties import ObjectProperty
from kivy.adapters.listadapter import ListAdapter

def get_kivy_designer_dir():
    return os.path.join(os.path.expanduser('~'), '.kivy-designer')

RECENT_FILES_NAME = 'recent_files'
MAX_RECENT_FILES = 10
recent_file_path = os.path.join(get_kivy_designer_dir(), RECENT_FILES_NAME)

class RecentManager(object):
    
    def __init__(self):
        super(RecentManager, self).__init__()
        self.list_files = []
        self.load_files()

    def add_file(self, _file):
        _file_index = 0
        try:
            _file_index = self.list_files.index(_file)
        except:
            _file_index = -1

        if _file_index != -1:
            #If _file is already present in list_files, then move it to 0 index
            self.list_files.remove(_file)

        self.list_files.insert(0, _file)
        
        #Recent files should not be greater than MAX_RECENT_FILES
        while len(self.list_files) > MAX_RECENT_FILES:
            self.list_files.pop()

        self.store_files()

    def store_files(self):
        _string = ''
        for _file in self.list_files:
            _string += _file + '\n'
        
        f = open(recent_file_path, 'w')
        f.write(_string)
        f.close()
    
    def load_files(self):
        if not os.path.exists(recent_file_path):
            return

        f = open(recent_file_path, 'r')
        _file = f.readline()

        while _file != '':
            self.list_files.append(_file.strip())
            _file = f.readline()
        
        f.close()


class RecentDialog(BoxLayout):
    
    listview = ObjectProperty(None)
    select_button = ObjectProperty(None)
    cancel_button = ObjectProperty(None)
    adapter = ObjectProperty(None)

    __events__=('on_select', 'on_cancel')

    def __init__(self, file_list, **kwargs):
        super(RecentDialog, self).__init__(**kwargs)
        item_strings = file_list
        adapter = ListAdapter(cls=ListItemButton, data=item_strings,\
                              selection_mode='single',\
                              allow_empty_selection=False)

        self.listview = ListView(adapter=adapter)
        self.add_widget(self.listview, 1)

    def on_select_button(self, *args):
        self.select_button.bind(on_press=partial(self.dispatch, 'on_select'))
    
    def on_cancel_button(self, *args):
        self.cancel_button.bind(on_press=partial(self.dispatch, 'on_cancel'))
        
    def on_select(self, *args):
        pass
    
    def on_cancel(self, *args):
        pass