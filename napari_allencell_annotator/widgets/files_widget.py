from typing import Set, List, Dict
from qtpy.QtWidgets import QListWidget
from qtpy.QtCore import Signal

from napari_allencell_annotator.widgets.file_item import FileItem


class FilesWidget(QListWidget):
    """
    A class used to create a QListWidget for files.

    Attributes
    ----------
    shuffled : bool
        a boolean, True if list is currently shuffled
    checked : Set[FileItem]
        a set of items that are currently checked
    files_dict : Dict[str , List[str]]
        a dictionary of file path -> [File Name, FMS]
        stores file order in insertion order of keys

    Methods
    -------
    set_shuffled(shuffled : bool)
        Sets the list shuffled property.
    unhide_all()
        Displays the file names on all files in the list.
    clear_all()
        Clears all image data in the file widget.
    clear_for_shuff() -> List[str]
        Clears the list display.
    get_curr_row() -> int
        Returns current image row.
    add_item(file: str, hidden: bool)
        Adds a file to the file widget.
    remove_item(item: ListItem)
        Removes the item from the file widget.
    """

    files_selected: Signal = Signal(bool)
    files_added: Signal = Signal(bool)

    def __init__(self):
        QListWidget.__init__(self)
        self.checked: Set[FileItem] = set()
        # files_dict holds all image info file path -> [file name, FMS]
        # also holds the original insertion order in .keys()
        self.setCurrentItem(None)
        self._shuffled: bool = False

    @property
    def shuffled(self) -> bool:
        """
        Current shuffle state of the list.

        Returns
        -------
        bool
            the shuffled property.
        """
        return self._shuffled

    def set_shuffled(self, shuffled: bool) -> None:
        """
        Set the shuffled property to shuffled or unshuffled.

        Parameters
        ----------
        shuffled : bool
        """
        self._shuffled = shuffled

    def unhide_all(self) -> None:
        """Display the file names on all files in the list."""
        for i in range(self.count()):
            self.item(i).unhide()

    def get_curr_row(self) -> int:
        """
        Get the row of the currently selected image

        Returns
        -------
        int
            the current row.
        """
        if self.currentItem() is not None:
            return self.row(self.currentItem())
        else:
            return -1

    def clear_all(self) -> None:
        """Clear all image data in the file widget."""
        self._shuffled = False
        self.checked = set()

        self.setCurrentItem(None)
        self.clear()

    def clear_for_shuff(self) -> None:
        """
        Clear the list display.

        This function clears all displayed, checked, and current items, but keeps the files_dict.

        Returns
        -------
         Dict[str, List[str]]
            file dictionary file path -> [file name, fms].
        """
        self._shuffled = True
        self.setCurrentItem(None)
        self.checked = set()
        self.clear()

    def add_item(self, file: str, hidden: bool = False) -> None:
        """
        Add a file to the file widget.

        Optional hidden parameter toggles file name visibility.

        Params
        -------
        file: str
            a file path.
        hidden: bool
            file name visibility.
        """
        item: FileItem = FileItem(file, self, hidden)
        item.check.stateChanged.connect(lambda: self._check_evt(item))

    def remove_item(self, item: FileItem) -> None:
        """
        Remove the item from the file widget.

        Params
        -------
        item: FileItem
            an item to remove.
        """
        if item == self.currentItem():
            self.setCurrentItem(None)
        self.takeItem(self.row(item))

    def _check_evt(self, item: FileItem) -> None:
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