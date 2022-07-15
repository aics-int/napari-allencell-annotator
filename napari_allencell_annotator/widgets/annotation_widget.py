from PyQt5.QtWidgets import QListWidget, QAbstractItemView

from napari_allencell_annotator.widgets.annotation_item import AnnotationItem


class AnnotationWidget(QListWidget):
    """
    A class used to create a QListWidget for annotations.

    """

    def __init__(self):
        QListWidget.__init__(self)
        # allow drag and drop rearrangement
        self.setDragDropMode(QAbstractItemView.InternalMove)
        # TODO: styling https://blog.actorsfit.com/a?ID=01450-929cf741-2d80-418c-8a55-a52395053369

    def clear_all(self):
        """Clear all image data."""

        self.clear()

    def add_new_item(self):
        """
        Adds a new Annotation Item to the list. .

        Only allows 10 items to be added.
        """
        if self.count() < 10:
            item = AnnotationItem(self)
            h = item.sizeHint().height()
            self.setMaximumHeight(h * self.count())

    def remove_item(self, item: AnnotationItem):
        """
        Remove the item.

        Params
        -------
        item: AnnotationItem
            an item to remove.
        """
        self.takeItem(self.row(item))
