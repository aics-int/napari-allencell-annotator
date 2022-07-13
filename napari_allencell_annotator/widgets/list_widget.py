from PyQt5.QtWidgets import QListWidget, QAbstractItemView
from typing import Set, List, Optional, Dict

from qtpy.QtCore import Signal

from napari_allencell_annotator.widgets.list_item import ListItem


class ListWidget(QListWidget):
    """
    A class used to create a QListWidget for files.

    Attributes
    ----------
    checked : Set[ListItem]
        a set of items that are currently checked
    file_dict : Dict[str , Dict[str, str]]
        a dictionary of file path -> {"File Name": _, "FMS" : _}

    Methods
    -------
    clear_all()
        Clears all image data.
    clear_for_shuff() -> List[str]
        Clears the list display and returns the file_order.
    set_shuff_order(lst : List[str]
        Sets the shuffle order list.
    add_new_item(file:str)
        Adds a new file to the list and file_order.
    add_item(file: str, hidden: bool)
        Adds a file to the list, but not to the file_order.
    remove_item(item: ListItem)
        Removes the item from all attributes.
    delete_checked()
        Removes all items in checked.
    """

    files_selected = Signal(bool)
    files_added = Signal(bool)

    def __init__(self):
        QListWidget.__init__(self)
        self.checked: Set[ListItem] = set()
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.file_dict: Dict[str, List[str]] = {}
        self.setCurrentItem(None)
        self._shuffled: bool = False
        self.shuffle_order: Dict[str, Dict[str, str]] = {}


    @property
    def shuffled(self) -> bool:
        return self._shuffled

    def get_curr_row(self) -> int:
        if self.currentItem() is not None:
            return self.row(self.currentItem())
        else:
            return -1

    def clear_all(self):
        """Clear all image data."""
        self._shuffled = False
        self.checked = set()
        self.file_dict = {}
        self.shuffle_order = {}
        self.setCurrentItem(None)
        self.clear()

    def set_shuff_order(self, dct: Optional[Dict[str, Dict[str,str]]] = {}):
        """Set shuffled order."""
        self.shuffle_order = dct

    def clear_for_shuff(self) -> Dict[str, Dict[str,str]]:
        """
        Clear the list display and return the file_dict.

        This function clears all displayed, checked, and current items, but keeps the file_dict.

        Returns
        -------
        List[str]
            file_order.
        """
        self._shuffled = not self._shuffled
        self.shuffle_order = {}
        self.setCurrentItem(None)
        self.checked = set()
        self.clear()
        return self.file_dict

    def add_new_item(self, file: str):
        """
        Adds a new file to the list and file_dict.

        This function emits a files_added signal when this is the first file added.

        Params
        -------
        file: str
            a file path.
        """
        if file not in self.file_dict.keys():
            item = ListItem(file, self, False)
            item.check.stateChanged.connect(lambda: self._check_evt(item))
            self.file_dict[file] = [item.get_name(), ""]
            if len(self.file_dict) == 1:
                self.files_added.emit(True)

    def add_item(self, file: str, hidden: bool = False):
        """
        Add a file to the list, but not to the file_dict.

        Optional hidden parameter toggles file name visibility.

        Params
        -------
        file: str
            a file path.
        hidden: bool
            file name visibility.
        """
        item = ListItem(file, self, hidden)
        item.check.stateChanged.connect(lambda: self._check_evt(item))

    def remove_item(self, item: ListItem):
        """
        Remove the item from all attributes.

        This function emits a files_added signal when the item to remove is the only item.

        Params
        -------
        item: ListItem
            an item to remove.
        """
        if item.file_path in self.file_dict.keys():
            if item == self.currentItem():
                self.setCurrentItem(None)
            self.takeItem(self.row(item))
            del self.file_dict[item.file_path]
            if len(self.file_dict) == 0:
                self.files_added.emit(False)

    def delete_checked(self):
        """
        Delete the checked items.

        This function emits a files_selected signal.
        """
        for item in self.checked:
            self.remove_item(item)
        self.checked.clear()
        self.files_selected.emit(False)

    def _check_evt(self, item: ListItem):
        """
        Update checked set and emit files_selected signal.

        Params
        -------
        item: ListItem
            the item that has been checked or unchecked.
        """
        if item.check.isChecked() and item not in self.checked:
            self.checked.add(item)
            if len(self.checked) == 1:
                self.files_selected.emit(True)
        elif not item.check.isChecked() and item in self.checked:
            self.checked.remove(item)
            if len(self.checked) == 0:
                self.files_selected.emit(False)
