from typing import Dict

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QMainWindow,
    QListWidget,
    QWidget,
    QLabel,
    QGridLayout,
    QPushButton,
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
    QScrollArea,
    QHBoxLayout,
)
from psygnal._signal import Signal

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

    valid_annots_made = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Create Annotations")
        self.setMinimumSize(700, 500)

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
        self.cancel = QPushButton("Cancel")
        self.apply = QPushButton("Apply")
        self.btns = QWidget()
        self.new_annot_dict: Dict[str, Dict] = None
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
        self.cancel.clicked.connect(self.reject)
        self.apply.clicked.connect(self.get_annots)
        self.valid_annots_made.connect(self.accept)

    def add_clicked(self):
        self.list.add_new_item()
        if self.list.count() > 9:
            self.add.hide()

    def get_annots(self):
        dct: Dict[str, Dict] = {}
        valid = True
        items = [self.list.item(x) for x in range(self.list.count())]
        for i in items:
            valid, name, sub_dct = i.get_data()
            dct[name] = sub_dct
            if not valid:
                valid = False
        if valid:
            self.new_annot_dict = dct
            self.valid_annots_made.emit()
        else:
            self.new_annot_dict = None
