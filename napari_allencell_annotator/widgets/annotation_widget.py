from PyQt5.QtWidgets import QListWidget, QAbstractItemView
from typing import Set, List, Optional, Dict

from qtpy.QtCore import Signal

from napari_allencell_annotator.widgets.list_item import ListItem

from napari_allencell_annotator.widgets.annotation_item import AnnotationItem


class AnnotationWidget(QListWidget):
    """
    A class used to create a QListWidget for annotations.

    Attributes
    ----------

    Methods
    -------

    """

    def __init__(self):
        QListWidget.__init__(self)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        # TODO: styling https://blog.actorsfit.com/a?ID=01450-929cf741-2d80-418c-8a55-a52395053369

    def clear_all(self):
        """Clear all image data."""

        self.clear()

    def add_new_item(self):
        """
        Adds a new file to the list and file_dict.

        This function emits a files_added signal when this is the first file added.

        Params
        -------
        file: str
            a file path.
        """
        if self.count() < 10:
            item = AnnotationItem(self)
            h = item.sizeHint().height()
            if self.count() < 5:
                self.setMaximumHeight(h * self.count())

    def remove_item(self, item: ListItem):
        """
        Remove the item from all attributes.

        This function emits a files_added signal when the item to remove is the only item.

        Params
        -------
        item: ListItem
            an item to remove.
        """
        self.takeItem(self.row(item))



