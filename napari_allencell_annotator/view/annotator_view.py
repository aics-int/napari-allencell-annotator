from enum import Enum
from typing import Dict

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QCheckBox, QComboBox, \
    QGridLayout, QListWidget, QScrollArea, QListWidgetItem, QPushButton
import napari


class AnnotatorViewMode(Enum):
    ADD = "add"
    VIEW = "view"
    ANNOTATE = "annotate"


class AnnotatorView(QWidget):
    def __init__(self, viewer: napari.Viewer, annot_data: Dict = None, mode: AnnotatorViewMode = AnnotatorViewMode.ADD):
        super().__init__()
        self._mode = mode
        label = QLabel("Annotations")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 15))
        self.layout = QGridLayout()
        self.layout.addWidget(label, 0, 0, 1, 4)

        self.annot_widget = QListWidget()

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.annot_widget)
        self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll, 1, 0, 10, 4)

        self._render_gui(annot_data)

        self.setLayout(self.layout)
        self.viewer = viewer

        self.show()

    @property
    def mode(self) -> AnnotatorViewMode:
        return self._mode

    def _render_gui(self, annot_data):
        #TODO: refactor to have two buttons with different modes? if this design is good
        if self.mode == AnnotatorViewMode.ADD:
            self.create_btn = QPushButton("Create Annotations")
            self.create_btn.setEnabled(True)
            self.import_btn = QPushButton("Import Existing Annotations")
            self.import_btn.setEnabled(True)

            self.layout.addWidget(self.create_btn, 12, 0, 1, 2)
            self.layout.addWidget(self.import_btn, 12, 2, 1, 2)
        else:
            self.read_data(annot_data)
            if self.mode == AnnotatorViewMode.VIEW:
                self.cancel_btn = QPushButton("Cancel")
                self.cancel_btn.setEnabled(True)
                self.start_btn = QPushButton("Start Annotating")
                self.start_btn.setEnabled(True)

                self.layout.addWidget(self.cancel_btn, 12, 0, 1, 1)
                self.layout.addWidget(self.start_btn, 12, 1, 1, 3)

            elif self.mode == AnnotatorViewMode.VIEW:
                self.back_btn = QPushButton("< Previous")
                self.back_btn.setEnabled(True)
                self.next_btn = QPushButton("Next >")
                self.next_btn.setEnabled(True)

                self.layout.addWidget(self.back_btn, 12, 0, 1, 2)
                self.layout.addWidget(self.back_btn, 12, 2, 1, 2)

    def read_data(self, annot_data):
        for name in annot_data.keys():
            self.create_annot(name, annot_data[name])

    def create_annot(self, name: str, dict: Dict):
        widget = QWidget()
        layout = QHBoxLayout()
        label = QLabel(name)
        layout.addWidget(label, stretch=1)
        annot_type: str = dict['type']
        if annot_type == "string":
            item = QLineEdit(dict['default'])
        elif annot_type == "number":
            item = QSpinBox()
            item.setValue(dict['default'])
        elif annot_type == "bool":
            item = QCheckBox()
            if dict['default'] == 'true' or dict['default']:
                item.setChecked(True)
        elif annot_type == "list":
            item = QComboBox()
            for opt in dict['options']:
                item.addItem(opt)
            item.setCurrentText(dict['default'])
        layout.addWidget(item, stretch=2)
        layout.addStretch()
        layout.setSpacing(10)
        widget.setLayout(layout)
        list_item = QListWidgetItem(self.annot_widget)
        list_item.setSizeHint(widget.sizeHint())
        self.annot_widget.setItemWidget(list_item, widget)
