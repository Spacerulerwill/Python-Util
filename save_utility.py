# class for a save file

from json import dump as jsondump
from os import remove
from os.path import realpath
from typing import Any

class Save:
    '''
    A class used to create a save file to load and store data
    '''
    def __init__(self, fileName):
        fileName += ".json"
        self._fileName = fileName
        self._data = {}
        self._unsaved_changes = False
        open(fileName, "w+").close()

    def save(self) -> None:
        '''
        Save changes in data to file
        '''
        with open(self._fileName, 'w+') as outfile:
            jsondump(self._data, outfile, indent=4)

    def reset(self) -> None:
        '''
        Reset save file
        '''
        if not self._unsaved_changes:
            self._unsaved_changes = True
        self._data = {}
        self.save()

    def delete(self) -> None:
        '''
        Delete the save file
        '''
        remove(self._fileName)

    def getPath(self) -> str:
        return realpath(self._fileName)

    def __del__(self) -> None:
        self.delete()

    def __setitem__(self, name, data) -> None:
        if not self._unsaved_changes:
            self._unsaved_changes = True
        self._data[name] = data

    def __getitem__(self, name) -> Any:
        return self._data[name]

    def __delitem__(self, name) -> None:
        if not self._unsaved_changes:
            self._unsaved_changes = True
        del self._data[name]

    def hasUnsavedChanges(self) -> bool:
        '''
        Check if there is any unsaved changes
        '''
        return self._unsaved_changes