
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication

from napari_allencell_annotator.view.annotator_view import AnnotatorMenu
from napari_allencell_annotator.view.images_view import ImageViewer


class MainWindow(QMainWindow):
    def __init__(self, view, model, controller):
        super().__init__()
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.central_layout = QVBoxLayout()
        self.viewer = view
        self.layer = None
        self.drag_drop = ImageViewer(self.viewer)
        #self.annotator = AnnotatorMenu(self.viewer)
        self.central_layout.addWidget(self.drag_drop, stretch=2)
        #self.central_layout.addWidget(self.annotator, stretch=5)

        self.central.setLayout(self.central_layout)



