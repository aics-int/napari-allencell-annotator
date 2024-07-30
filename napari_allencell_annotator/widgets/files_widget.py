from typing import Set

from PyQt5.QtCore import QSignalBlocker
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
        self._annotator_model = annotator_model

        self._annotator_model.image_changed.connect(self._handle_image_changed)
        self._annotator_model.images_shuffled.connect(self._handle_shuffle)
        self._annotator_model.image_set_added.connect(
            lambda: self._handle_shuffle(self._annotator_model.is_images_shuffled())
        )
        self._annotator_model.image_count_changed.connect(self._handle_image_count_change)
        self.currentItemChanged.connect(self._handle_file_item_changed)

    def _handle_image_changed(self):
        with QSignalBlocker(self):
            self.setCurrentItem(self.item(self._annotator_model.get_curr_img_index()))

            previous = self.item(self._annotator_model.get_previous_image_index())
            if previous is not None:
                previous.unhighlight()

            current = self.item(self._annotator_model.get_curr_img_index())
            if current is not None:
                current.highlight()

    def _handle_file_item_changed(self, curr_item: FileItem, prev_item: FileItem) -> None:
        """
        Update the model when the current item in the file widget is changed if it has not been updated.

        Parameters
        ----------
        curr_item:
            the current file item
        prev_item:
            the previous file item
        """
        self._annotator_model.set_previous_image_index(self.row(prev_item))
        self._annotator_model.set_curr_img_index(self.row(curr_item))

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

    def _handle_shuffle(self, shuffled: bool) -> None:
        self._reset_list()
        if shuffled:
            # readd shuffled images to list
            for shuffled_img in self._annotator_model.get_shuffled_images():
                self.add_item(shuffled_img, hidden=True)  # add hidden when items shuffled.
        else:
            # readd unshuffled images to list
            for img in self._annotator_model.get_all_images():
                self.add_item(img)

    def _reset_list(self) -> None:
        """
        Reset the list of files
        """
        self.setCurrentItem(None)
        self.checked = set()
        self.clear()  # clear list

    def _handle_image_count_change(self, count: int) -> None:
        if count == 0:
            self._reset_list()

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
