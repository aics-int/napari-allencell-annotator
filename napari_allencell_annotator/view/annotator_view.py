from typing import Dict

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QCheckBox, QComboBox
import napari


class AnnotatorView(QWidget):
    def __init__(self, napari: napari.Viewer, annot_data: Dict):
        super().__init__()
        self.layout = QVBoxLayout()
        self.read_data(annot_data)

        self.setLayout(self.layout)
        self.napari = napari.Viewer()
        self.napari.window.add_dock_widget(self, area="right")
        self.napari = napari
        self.napari.window.add_dock_widget(self, area="right")
        self.show()

    def read_data(self, annot_data):
        for name in annot_data.keys:
            self.create_annot(name, annot_data[name])

    def create_annot(self, name: str, dict: Dict):
        layout = QHBoxLayout()
        label = QLabel(name)
        layout.addWidget(label)
        if (dict['type'] == "string"):
            type = QLineEdit()
        elif (dict['type'] == "number"):
            type = QSpinBox()
        elif (dict['type'] == "bool"):
            type = QCheckBox()
        elif (dict['type'] == "list"):
            type = QComboBox()
        layout.addWidget(type)
