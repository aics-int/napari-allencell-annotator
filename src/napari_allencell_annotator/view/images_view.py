from os import listdir
import os
from typing import List

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
    field_input_dir: FileInput
    field_output_dir: FileInput

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

        # Input dir
        self.field_input_dir = FileInput(mode=FileInputMode.DIRECTORY, placeholder_text="Select a folder...")
        self.field_input_dir.file_selected.connect(lambda: self._dir_selected(self.field_input_dir.selected_file[0]))
        #row3 = FormRow("3.  Input directory:", self.field_input_dir)

        self.field_input_file = FileInput(mode=FileInputMode.FILE, placeholder_text="Select files...")
        self.field_input_file.file_selected.connect(lambda: self._file_selected(self.field_input_file.selected_file))

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

        self.layout.addWidget(self.field_input_dir)
        self.layout.addWidget(self.field_input_file)
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

    def _dir_selected(self, dir: str):
        for file in listdir(dir):
            self._add_file(dir + "/" + file)

    def _file_selected(self, file_list: List[str]):
        for file in file_list:
            self._add_file(file)


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
            ListItem(file,self.file_widget)
        else:
            self.error_alert("Unsupported file type:" + file)


    def _display_img(self):
        """Display the current image in napari."""
        self.napari.layers.clear()
        self.napari.add_image(self.curr_img)





