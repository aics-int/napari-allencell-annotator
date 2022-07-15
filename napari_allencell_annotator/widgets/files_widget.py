from PyQt5.QtWidgets import QListWidget, QAbstractItemView
from typing import Set, List, Optional, Dict

from qtpy.QtCore import Signal

from napari_allencell_annotator.widgets.file_item import FileItem


class FilesWidget(QListWidget):
    """
    A class used to create a QListWidget for files.

    Attributes
    ----------
    checked : Set[FileItem]
        a set of items that are currently checked
    files_dict : Dict[str , List[str]]
        a dictionary of file path -> [File Name, FMS]

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
        self.checked: Set[FileItem] = set()
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        # files_dict holds all image info file path -> [file name, FMS]
        # also holds the original insertion order in .keys()
        self.files_dict: Dict[str, List[str]] = {}
        self.setCurrentItem(None)
        self._shuffled: bool = False
        # shuffle order holds the same file path -> [file name, FMS] as files_dict
        # only filled when the images have been shuffled
        # holds a new shuffled order in .keys()
        # when annotation starts if images are shuffled this order is given to annotation view
        self.shuffled_files_dict: Dict[str, List[str]] = {}

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
        self.files_dict = {}
        self.shuffled_files_dict = {}
        self.setCurrentItem(None)
        self.clear()

    def set_shuff_order(self, dct: Optional[Dict[str, List[str]]] = {}):
        """Set shuffled order."""
        self.shuffled_files_dict = dct

    def clear_for_shuff(self) -> Dict[str, List[str]]:
        """
        Clear the list display and return the files_dict.

        This function clears all displayed, checked, and current items, but keeps the files_dict.

        Returns
        -------
        List[str]
            file_order.
        """
        self._shuffled = not self._shuffled
        self.shuffled_files_dict = {}
        self.setCurrentItem(None)
        self.checked = set()
        self.clear()
        return self.files_dict

    def add_new_item(self, file: str):
        """
        Adds a new file to the list and files_dict.

        This function emits a files_added signal when this is the first file added.

        Params
        -------
        file: str
            a file path.
        """
        if file not in self.files_dict.keys():
            item = FileItem(file, self, False)
            item.check.stateChanged.connect(lambda: self._check_evt(item))
            self.files_dict[file] = [item.get_name(), ""]
            if len(self.files_dict) == 1:
                self.files_added.emit(True)

    def add_item(self, file: str, hidden: bool = False):
        """
        Add a file to the list, but not to the files_dict.

        Optional hidden parameter toggles file name visibility.

        Params
        -------
        file: str
            a file path.
        hidden: bool
            file name visibility.
        """
        item = FileItem(file, self, hidden)
        item.check.stateChanged.connect(lambda: self._check_evt(item))

    def remove_item(self, item: FileItem):
        """
        Remove the item from all attributes.

        This function emits a files_added signal when the item to remove is the only item.

        Params
        -------
        item: FileItem
            an item to remove.
        """
        if item.file_path in self.files_dict.keys():
            if item == self.currentItem():
                self.setCurrentItem(None)
            self.takeItem(self.row(item))
            del self.files_dict[item.file_path]
            if len(self.files_dict) == 0:
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

    def _check_evt(self, item: FileItem):
        """
        Update checked set and emit files_selected signal.

        Params
        -------
        item: FileItem
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
