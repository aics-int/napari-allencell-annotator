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

class ImageViewer(QWidget):
    def __init__(self, napari):
        super().__init__()

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Images")

        self.label.setFont(QFont("Arial", 15))

        self.napari = napari

        self.setAcceptDrops(True)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label, stretch=1)

        self.file_widget = QListWidget()
        self.file_widget.setSelectionMode(QAbstractItemView.SingleSelection)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.file_widget)
        self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll, stretch=10)
        self.setLayout(self.layout)

        self.add_btn = QPushButton("Add Files")
        self.layout.addWidget(self.add_btn, stretch=1)
        self.add_btn.clicked.connect(self.add_files)
        self.curr_image = None

    def add_files(self):
        f_names = QFileDialog.getOpenFileNames(self, "Open File", "c\\")
        #TODO: limit file types
        for file in f_names[0]:
            item = QListWidgetItem(file)
            self.file_widget.addItem(item)


    def dragEnterEvent(self, event):
       event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            image_paths = event.mimeData().urls()
            for path in image_paths:
                self.add_image(path.toLocalFile())
            event.accept()
        else:
            event.ignore()

    def display_img(self, img):
        if self.curr_image is not None:
            self.napari.layers.clear()
        self.napari.add_image(img)
