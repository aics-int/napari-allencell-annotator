
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import numpy

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QListWidget,
    QAbstractItemView,
    QScrollArea,
)
import napari
from napari.utils.notifications import show_info
from napari_allencell_annotator.widgets.file_input import FileInput, FileInputMode
from napari_allencell_annotator.widgets.list_item import ListItem


class ImagesView(QWidget):
    """
    A class used to create a view for image file uploading and selecting.

    Attributes
    ----------
    napari : napari.Viewer
        a napari viewer where the plugin will be used
    curr_img : numpy.ndarray
        the currently selected image
    ctrl
        a controller for the view

    Methods
    -------
    alert(alert:str)
        Displays the alert message on the napari viewer
    set_curr_img(img:numpy.ndarray)
        Sets the current image and displays the selection
    """


    def __init__(self, napari: napari.Viewer, ctrl):
        """
        Parameters
        ----------
        napari : napari.Viewer
            The napari viewer for the plugin
        ctrl
            The controller
        """
        super().__init__()
        self.input_dir: FileInput
        self.input_file: FileInput

        self.input_dir = FileInput(mode=FileInputMode.DIRECTORY, placeholder_text="Select a folder...")


        self.input_file = FileInput(mode=FileInputMode.FILE, placeholder_text="Select files...")


        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Images")

        self.label.setFont(QFont("Arial", 15))
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label, stretch=1)

        self.file_widget = QListWidget()
        self.file_widget.setSelectionMode(QAbstractItemView.SingleSelection)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.file_widget)
        self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll, stretch=10)

        self.setLayout(self.layout)

        self.layout.addWidget(self.input_dir)
        self.layout.addWidget(self.input_file)
        self.curr_img = None
        self.ctrl = ctrl
        self.napari = napari

        self.napari.window.add_dock_widget(self, area="right")
        self.show()

    def set_curr_img(self,img: numpy.ndarray):
        """
        Sets the current image and displays it.

        Parameters
        ----------
        img: numpy.ndarray
            The selected image array
        """
        self.curr_img = img
        self._display_img()

    def alert(self, alert_msg: str):
        """
        Displays an error alert on the napari viewer.

        Parameters
        ----------
        alert : str
            The message to be displayed
        """
        show_info(alert_msg)

    def get_dir(self):
        return self.input_dir.selected_file[0]

    def get_file(self):
        return self.input_file.selected_file

    def add_file(self, file: str):
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

        ListItem(file,self.file_widget)



    def _display_img(self):
        """Display the current image in napari."""
        if self.curr_img is not None:
            self.napari.layers.clear()
            self.napari.add_image(self.curr_img)





