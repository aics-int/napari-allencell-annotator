from typing import Set
from qtpy.QtWidgets import QListWidget
from qtpy.QtCore import Signal
from pathlib import Path

from napari_allencell_annotator.model.annotation_model import AnnotatorModel
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

    Methods
    -------
    set_shuffled(shuffled : bool)
        Sets the list shuffled property.
    unhide_all()
        Displays the file names on all files in the list.
    clear_all()
        Clears all image data in the file widget.
    clear_for_shuff()
        Clears the list display.
    get_curr_row() -> int
        Returns current image row.
    add_item(file: Path, hidden: bool)
        Adds a file to the file widget.
    remove_item(item: ListItem)
        Removes the item from the file widget.
    """

    files_selected: Signal = Signal(bool)
    files_added: Signal = Signal(bool)

    def __init__(self, annotator_model: AnnotatorModel):
        QListWidget.__init__(self)
        self.checked: Set[FileItem] = set()
        # files_dict holds all image info file path -> [file name, FMS]
        # also holds the original insertion order in .keys()
        self.setCurrentItem(None)
        self._shuffled: bool = False
        self._annotator_model = annotator_model

        self._annotator_model.image_changed.connect(lambda: self.setCurrentItem(self.item(self._annotator_model.get_curr_img_index())))

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

        """
        self._shuffled = True
        self.setCurrentItem(None)
        self.checked = set()
        self.clear()

    def add_item(self, file: Path, hidden: bool = False) -> None:
        """
        Add a file to the file widget.

        Optional hidden parameter toggles file name visibility.

        Params
        -------
        file: Path
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

    def unhide_item_at(self, idx: int) -> None:
        self.unhide_item_at(idx)
