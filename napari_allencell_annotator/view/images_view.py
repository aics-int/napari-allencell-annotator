import sys

import napari
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import *  # TODO import formatting
from skimage import data
from PIL import Image
import numpy
import imageio
from aicsimageio import AICSImage


class ImageViewer(QWidget):
    def __init__(self, viewer):
        super().__init__()

        # creating a label
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Images")

        self.label.setFont(QFont("Arial", 15))

        self.viewer = viewer

        # set window title
        self.setWindowTitle("Image Drag and Drop ")
        # set window geometry
        self.setGeometry(500, 200, 400, 400)

        # create box layout
        self.drag_layout = QVBoxLayout()
        # add image label in box layout
        self.drag_layout.addWidget(self.label, stretch=1)

        self.file_widget = QListWidget()
        self.file_widget.setSelectionMode(QAbstractItemView.SingleSelection)

        self.file_widget.setSelectionRectVisible(True)
        self.file_widget.currentItemChanged.connect(
            self.currentImageChangeEvent
        )

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.file_widget)
        self.scroll.setWidgetResizable(True)
        self.drag_layout.addWidget(self.scroll, stretch=10)
        self.setLayout(self.drag_layout)

        self.add_btn = QPushButton("Add")
        self.drag_layout.addWidget(self.add_btn, stretch=1)
        self.add_btn.clicked.connect(self.add_files)
        self.curr_image = None

    def add_files(self):
        f_names = QFileDialog.getOpenFileNames(
            self, "Open File", "c\\", "Tiff Files (*.tiff)"
        )

        for file in f_names[0]:
            img = file
            self.add_image(img)

    def dragEnterEvent(self, event):
        # check if the event has image or not
        if event.mimeData().hasImage:
            # if event has image then
            # accept the event to drag
            event.accept()
        else:
            # if event doesn't have image
            # then ignore the event to drag
            event.ignore()

    def dropEvent(self, event):
        # check if the event has image or not
        if event.mimeData().hasImage:
            # set drop action with copying dragged image
            event.setDropAction(Qt.CopyAction)
            # get selected image path
            image_path = event.mimeData().urls()[0].toLocalFile()
            # call set_image() function to load
            # image with image path parameter
            self.add_image(image_path)
            # if event has image then
            # accept the event to drop
            event.accept()
        else:
            # if event doesn't have image
            # then ignore the event to drop
            event.ignore()

    def currentImageChangeEvent(self, event):
        if self.curr_image is not None:

            self.viewer.layers.clear()
        self.curr_image = event.text()

        img = AICSImage(self.curr_image)
        img = img.data

        new_layer = self.viewer.add_image(img)

    def add_image(self, image_path):

        item = QListWidgetItem(image_path)

        self.file_widget.addItem(item)
