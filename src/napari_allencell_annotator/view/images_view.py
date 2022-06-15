from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QListWidget,
    QAbstractItemView,
    QScrollArea,
    QPushButton,
    QFileDialog,
    QListWidgetItem,
)

from aicsimageio import AICSImage


class ImageViewer(QWidget):
    def __init__(self, viewer):
        super().__init__()

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Images")

        self.label.setFont(QFont("Arial", 15))

        self.viewer = viewer

        self.setWindowTitle("Image Drag and Drop ")
        self.setGeometry(500, 200, 400, 400)

        self.drag_layout = QVBoxLayout()
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
        f_names = QFileDialog.getOpenFileNames(self, "Open File", "c\\")

        for file in f_names[0]:
            img = file
            self.layer = self.add_image(img)

    def currentImageChangeEvent(self, event):
        if self.curr_image is not None:

            self.viewer.layers.clear()
        self.curr_image = event.text()
        img = AICSImage(self.curr_image)
        img = img.data
        self.viewer.add_image(img)

    def add_image(self, image_path):
        item = QListWidgetItem(image_path)
        self.file_widget.addItem(item)
