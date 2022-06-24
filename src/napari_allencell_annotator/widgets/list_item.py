import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem, QListWidget, QStyle, QWidget, QHBoxLayout, QLabel, QCheckBox
from PyQt5.uic.properties import QtWidgets
from qtpy import QtGui


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
        self._file_path = file_path
        self.setText(" ")
        self.widget = QWidget()
        self.layout = QHBoxLayout()
        self.label = QLabel(os.path.basename(file_path))
        self.layout.addWidget(self.label,stretch=19)
        self.check = QCheckBox()
        self.check.setCheckState(False)
        self.layout.addWidget(self.check,stretch=1)
        self.layout.addStretch()
        self.layout.setContentsMargins(2,2,0,2)


        self.widget.setLayout(self.layout)
        self.setSizeHint(self.widget.sizeHint())
        parent.setItemWidget(self, self.widget)

    @property
    def file_path(self):
        return self._file_path

    def __hash__(self):
        return hash((self.file_path))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.file_path == other.file_path

