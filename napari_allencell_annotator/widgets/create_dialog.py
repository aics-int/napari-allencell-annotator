from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QListWidget, QWidget, QLabel, QGridLayout, QPushButton, QDialog, \
    QDialogButtonBox, QVBoxLayout, QScrollArea, QHBoxLayout

from napari_allencell_annotator.widgets.annotation_item import AnnotationItem
from napari_allencell_annotator.widgets.annotation_widget import AnnotationWidget

class CreateDialog(QDialog):
    """
    A class that creates up to 10 annotations in a popup dialog.

    Attributes
    ----------
    Methods
    -------
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Create Annotations")
        self.setMinimumSize(700,500)

        # self.buttonBox.accepted.connect(self.accept)
        # self.buttonBox.rejected.connect(self.reject)

        self.list = AnnotationWidget()
        self.list.add_new_item()

        label = QLabel("Create Annotations")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 15))
        self.layout = QVBoxLayout()
        self.layout.addWidget(label)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.list)
        self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll, stretch=15)

        self.add = QPushButton("Add +")
        self.delete = QPushButton("Delete Selected")
        self.cancel = QPushButton('Cancel')
        self.apply = QPushButton('Apply')
        self.btns = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.add)
        layout.addWidget(self.delete)
        sp_retain = QtWidgets.QSizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.delete.setSizePolicy(sp_retain)
        self.delete.hide()
        layout.addWidget(self.cancel)
        layout.addWidget(self.apply)

        self.btns.setLayout(layout)
        self.layout.addWidget(self.btns)
        self.setLayout(self.layout)
        self.add.clicked.connect(self.add_clicked)

    def add_clicked(self):
        self.list.add_new_item()
        if self.list.count() > 9:
            self.add.hide()


