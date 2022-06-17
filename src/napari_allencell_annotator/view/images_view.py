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
    QListWidgetItem, QFileDialog,
)
from napari.utils.notifications import show_info

class ImageViewer(QWidget):
    """View for image file uploading and selecting."""
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

        self.curr_image = None
        self.ctrl = None

        self.add_btn.clicked.connect(self.get_files)

    def set_ctrl(self, ctrl):
        self.ctrl = ctrl

    def add_file(self, file):
        """Add a file to the list."""
        if self.ctrl.is_supported(file):
            item = QListWidgetItem(file)
            self.file_widget.addItem(item)
        else:
            self.error_alert("Unsupported file type:" + file)

    def error_alert(self, alert):
        show_info(alert)

    def dragEnterEvent(self, event):
       event.accept()

    def dropEvent(self, event):
        """Add file names for files dropped into the view."""
        #TODO: limit file types
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            image_paths = event.mimeData().urls()
            for path in image_paths:
                self.add_file(path.toLocalFile())
            event.accept()
        else:
            event.ignore()

    def get_files(self):
        """Get user files from QFileDialog."""
        f_names = QFileDialog.getOpenFileNames(self, "Open File", "c\\")
        for file in f_names[0]:
            self.add_file(file)

    def set_curr_img(self,img):
        self.curr_image = img
        self._display_img()

    def _display_img(self):
        """Display the current image in napari."""

        self.napari.layers.clear()
        self.napari.add_image(self.curr_image)
