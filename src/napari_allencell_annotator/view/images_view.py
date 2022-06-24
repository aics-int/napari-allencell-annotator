
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import numpy

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QListWidget,
    QAbstractItemView,
    QScrollArea, QGridLayout, QPushButton,
)
import napari
from napari.utils.notifications import show_info
from napari_allencell_annotator.widgets.file_input import FileInput, FileInputMode
from napari_allencell_annotator.widgets.list_widget import ListWidget
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

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Images")

        self.label.setFont(QFont("Arial", 12))
        self.layout = QGridLayout()
        self.layout.addWidget(self.label,0,0,1,4)

        self.input_dir: FileInput
        self.input_file: FileInput

        self.input_dir = FileInput(mode=FileInputMode.DIRECTORY, placeholder_text="Add a folder...")

        self.input_file = FileInput(mode=FileInputMode.FILE, placeholder_text="Add files...")
        self.layout.addWidget(self.input_dir, 1,0,1,2)
        self.layout.addWidget(self.input_file,1,2,1,2)

        self.file_widget = ListWidget()
        self.file_widget.items_selected.connect(self.toggle_delete)
        #self.file_widget.setSelectionMode(QAbstractItemView.SingleSelection)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.file_widget)
        self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll, 2,0,10,4)

        self.shuffle = QPushButton("Shuffle and Hide")
        self.shuffle.setEnabled(False)
        self.delete = QPushButton("Delete")
        self.delete.setEnabled(False)

        self.delete.clicked.connect(self.file_widget.delete_selected)



        self.layout.addWidget(self.shuffle, 13, 0, 1, 3)
        self.layout.addWidget(self.delete, 13, 3, 1, 1)

        self.setLayout(self.layout)


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

    def toggle_delete(self, selected: bool):
        if selected:
            self.delete.setEnabled(True)
        elif not selected:
            self.delete.setEnabled(False)

#TODO signal for first thing added and last thing deleted, catch and toggle shuffle button

    def _display_img(self):
        """Display the current image in napari."""
        if self.curr_img is not None:
            self.napari.layers.clear()
            self.napari.add_image(self.curr_img)





