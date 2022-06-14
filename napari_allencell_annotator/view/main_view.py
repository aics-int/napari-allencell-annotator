import sys

import napari
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import * #TODO import formatting
from skimage import data
from PIL import Image
import numpy
import imageio
from aicsimageio import AICSImage
from annotator_view import AnnotatorMenu
from images_view import ImageViewer

class MainWindow(QMainWindow):
    def __init__(self, napari_viewer):
        super().__init__()
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.central_layout = QVBoxLayout()
        self.viewer = napari_viewer
        self.drag_drop= ImageViewer(self.viewer)
        self.annotator = AnnotatorMenu(self.viewer)
        self.central_layout.addWidget(self.drag_drop, stretch=2)
        self.central_layout.addWidget(self.annotator,stretch=5)

        self.central.setLayout(self.central_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = napari.Viewer()
    win = MainWindow(view)
    view.window.add_dock_widget(win, area='right')
    sys.exit(app.exec_())