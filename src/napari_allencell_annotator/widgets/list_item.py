import os

from PyQt5.QtWidgets import QListWidgetItem, QListWidget


class ListItem(QListWidgetItem):
    """
    A class used to create custom QListWidgetItems.

    Attributes
    ----------

    Methods
    -------
    """
    def __init__(self, file_path: str, parent:QListWidget):
        QListWidgetItem.__init__(self, parent)
        self.setText(os.path.basename(file_path))
        self.file_path = file_path

        #TODO: TRASH, SELECT