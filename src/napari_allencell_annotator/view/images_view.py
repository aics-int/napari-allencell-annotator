from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont
import numpy

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QListWidget,
    QAbstractItemView,
    QScrollArea,
    QPushButton,
    QListWidgetItem,
    QFileDialog,
)
import napari
from napari.utils.notifications import show_info


class ImageView(QWidget):
    """
    A class used to create a view for image file uploading and selecting.

    Attributes
    ----------
    napari : napari.Viewer
        a napari viewer where the plugin will be used
    curr_img : numpy.uint8
        the currently selected image
    ctrl : TODO
        a controller for the view

    Methods
    -------
    error_alert(alert:str)
        Displays the alert message on the napari viewer
    set_curr_img(img:numpy.uint8)
        Sets the current image and displays the selection
    """
    def __init__(self, napari: napari.Viewer, ctrl):
        """
        Parameters
        ----------
        napari : napari.Viewer
            The napari viewer for the plugin
        ctrl : TODO
            The controller
        """
        super().__init__()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Images")

        self.label.setFont(QFont("Arial", 15))
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

        self.curr_img = None
        self.ctrl = ctrl
        self.add_btn.clicked.connect(self._get_files)
        self.napari = napari
        self.napari.window.add_dock_widget(self, area="right")
        self.show()

    def set_curr_img(self,img: numpy.uint8):
        """
        Sets the current image and displays it.

        Parameters
        ----------
        img: numpy.uint8
            The selected image array
        """
        self.curr_img = img
        self._display_img()

    def error_alert(self, alert: str):
        """
        Displays an error alert on the napari viewer.

        Parameters
        ----------
        alert : str
            The message to be displayed
        """
        show_info(alert)

    def _add_file(self, file: str):
        """
        Adds a file to the list.

        Tests if the controller supports the file then
        adds it to the list. Displays an error alert if
        the file is unsupported.

        Parameters
        ----------
        file : str
            The file to be added
        """
        if self.ctrl.is_supported(file):
            item = QListWidgetItem(file)
            self.file_widget.addItem(item)
        else:
            self.error_alert("Unsupported file type:" + file)

    def dragEnterEvent(self, event:QEvent.Type):
       event.accept()

    def dropEvent(self, event:QEvent.Type):
        """Add file names for files dropped into the view."""
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            image_paths = event.mimeData().urls()
            for path in image_paths:
                self._add_file(path.toLocalFile())
            event.accept()
        else:
            event.ignore()

    def _get_files(self):
        """Get user files from QFileDialog."""
        f_names = QFileDialog.getOpenFileNames(self, "Open File", "c\\")
        for file in f_names[0]:
            self._add_file(file)

    def _display_img(self):
        """Display the current image in napari."""
        self.napari.layers.clear()
        self.napari.add_image(self.curr_img)
