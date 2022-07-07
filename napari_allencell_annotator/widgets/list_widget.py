from PyQt5.QtWidgets import QListWidget, QAbstractItemView
from typing import Set, List

from qtpy.QtCore import Signal

from napari_allencell_annotator.widgets.list_item import ListItem


class ListWidget(QListWidget):
    """
    A class used to create a QListWidget for files.

    Attributes
    ----------
    checked : Set[ListItem]
        a set of items that are currently checked
    files : Set[str]
        a set of all file paths that have been added
    file_order : List[str]
        a list of file paths in the original order added

    Methods
    -------
    clear_all()
        Clears all image data.
    clear_for_shuff() -> List[str]
        Clears the list display and returns the file_order.
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
        self.files: Set[str] = set()
        self.file_order: List[str] = []
        self.setCurrentItem(None)
        self._shuffled: bool = False


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
        self.checked= set()
        self.files = set()
        self.file_order = []
        self.setCurrentItem(None)
        self.clear()

    def clear_for_shuff(self) -> List[str]:
        """
        Clear the list display and return the file_order.

        This function clears all displayed, checked, and current items, but keeps the file_order.

        Returns
        -------
        List[str]
            file_order.
        """
        self._shuffled = not self._shuffled
        self.setCurrentItem(None)
        self.checked = set()
        self.clear()
        return self.file_order

    def add_new_item(self, file: str):
        """
        Adds a new file to the list and file_order.

        This function emits a files_added signal when this is the first file added.

        Params
        -------
        file: str
            a file path.
        """
        if file not in self.files:
            self.file_order.append(file)
            if len(self.files) == 0:
                self.files_added.emit(True)
            self.add_item(file)

    def add_item(self, file: str, hidden: bool = False):
        """
        Add a file to the list, but not to the file_order.

        Optional hidden parameter toggles file name visibility.

        Params
        -------
        file: str
            a file path.
        hidden: bool
            file name visibility.
        """
        self.files.add(file)
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
        if item.file_path in self.files:
            if item == self.currentItem():
                self.setCurrentItem(None)
            self.takeItem(self.row(item))
            self.files.remove(item.file_path)
            self.file_order.remove(item.file_path)
            if len(self.files) == 0:
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
