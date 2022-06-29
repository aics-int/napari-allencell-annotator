from PyQt5.QtWidgets import QWidget, QVBoxLayout

from controller.images_controller import ImagesController

from controller.annotator_controller import AnnotatorController
import napari


class MainController(QWidget):
    def __init__(self):
        super().__init__()
        self.napari = napari.Viewer()
        layout = QVBoxLayout()
        images = ImagesController(self.napari)
        annotations = AnnotatorController(self.napari)
        layout.addWidget(images.view, stretch=1)
        layout.addWidget(annotations.view, stretch=2)
        self.setLayout(layout)
        self.show()
        self.napari.window.add_dock_widget(self, area="right")
