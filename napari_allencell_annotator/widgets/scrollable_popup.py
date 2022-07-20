from typing import List

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QScrollArea,  QLabel, QListWidget, QListWidgetItem, QDialog, \
    QDialogButtonBox


class ScrollablePopup(QDialog):
    def __init__(self, question: str, lst: List[str], parent=None):
        super().__init__(parent)
        self.setMinimumSize(500, 500)

        self.label = QLabel(question)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.content = QListWidget()
        self.scroll.setWidget(self.content)

        for str in lst:
            widget = QLabel(str)
            item = QListWidgetItem(self.content)
            item.setSizeHint(widget.minimumSizeHint())
            self.content.setItemWidget(item, widget)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.scroll)
        self.layout.addWidget(self.buttons)

        self.setLayout(self.layout)


