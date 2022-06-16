import napari
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from napari_allencell_annotator.view.annotator_view import AnnotatorMenu
from napari_allencell_annotator.view.images_view import ImageViewer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.central_layout = QVBoxLayout()
        self.napari = napari.Viewer()
        self.images = ImageViewer(self.napari)
        #self.annotator = AnnotatorMenu(self.view)
        self.central_layout.addWidget(self.images, stretch=2)
        #self.central_layout.addWidget(self.annotator, stretch=5)

        self.central.setLayout(self.central_layout)

        self.napari.window.add_dock_widget(self, area="right")

