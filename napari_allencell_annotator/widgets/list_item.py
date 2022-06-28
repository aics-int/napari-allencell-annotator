import os

from PyQt5.QtWidgets import QListWidgetItem, QListWidget, QWidget, QHBoxLayout, QLabel, QCheckBox

class ListItem(QListWidgetItem):
    """
    A class used to create custom QListWidgetItems.

    Attributes
    ----------
    file_path: str
        a path to the file.

    Methods
    -------
    """
    def __init__(self, file_path: str, parent:QListWidget, hidden: bool = False):
        QListWidgetItem.__init__(self, parent)
        self._file_path = file_path
        self.widget = QWidget()
        self.layout = QHBoxLayout()
        if hidden:
            self.label = QLabel("Image")
        else:
            self.label = QLabel(os.path.basename(file_path))
        self.layout.addWidget(self.label,stretch=19)
        self.check = QCheckBox()
        self.check.setCheckState(False)
        self.check.setCheckable(not hidden)
        self.layout.addWidget(self.check,stretch=1)
        self.layout.addStretch()

        self.layout.setContentsMargins(2,2,0,2)

        self.widget.setLayout(self.layout)
        self.setSizeHint(self.widget.sizeHint())
        if parent is not None:
            parent.setItemWidget(self, self.widget)

    @property
    def file_path(self) -> str:
        return self._file_path

    def __hash__(self) :
        return hash(self.file_path)

    def __eq__(self, other):
        """ Compares two ListItems file_path attributes"""
        if not isinstance(other, type(self)): return NotImplemented
        return self.file_path == other.file_path

