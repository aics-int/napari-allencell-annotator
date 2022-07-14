from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QScrollArea,
    QGridLayout,
    QPushButton,
    QMessageBox,
)
import napari
from aicsimageio import AICSImage, exceptions
from napari.utils.notifications import show_info

from napari_allencell_annotator.widgets.file_input import (
    FileInput,
    FileInputMode,
)
from napari_allencell_annotator.widgets.list_widget import ListWidget, ListItem


class ImagesView(QWidget):
    """
    A class used to create a view for image file uploading and selecting.

    Attributes
    ----------
    viewer : napari.Viewer
        a napari viewer where the plugin will be used
    ctrl : ImagesController
        a controller for the view

    Methods
    -------
    alert(alert:str)
        Displays the alert message on the napari viewer
    """

    def __init__(self, viewer: napari.Viewer, ctrl):
        """
        Parameters
        ----------
        viewer : napari.Viewer
            The napari viewer for the plugin
        ctrl : ImagesController
            The controller
        """
        super().__init__()

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Images")

        self.label.setFont(QFont("Arial", 15))
        self.layout = QGridLayout()
        self.layout.addWidget(self.label, 0, 0, 1, 4)

        self.input_dir: FileInput
        self.input_file: FileInput

        self.input_dir = FileInput(mode=FileInputMode.DIRECTORY, placeholder_text="Add a folder...")

        self.input_file = FileInput(mode=FileInputMode.FILE, placeholder_text="Add files...")
        self.layout.addWidget(self.input_dir, 1, 0, 1, 2)
        self.layout.addWidget(self.input_file, 1, 2, 1, 2)

        self.file_widget = ListWidget()
        self.file_widget.files_selected.connect(self._toggle_delete)
        self.file_widget.files_added.connect(self._toggle_shuffle)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.file_widget)
        self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll, 2, 0, 10, 4)

        self.shuffle = QPushButton("Shuffle and Hide")
        self.shuffle.setCheckable(True)
        self.shuffle.toggled.connect(self._update_shuff_text)

        self.shuffle.setEnabled(False)

        self.delete = QPushButton("Delete Selected")
        self.delete.setEnabled(False)

        self.delete.clicked.connect(self._delete_clicked)

        self.layout.addWidget(self.shuffle, 13, 0, 1, 3)
        self.layout.addWidget(self.delete, 13, 3, 1, 1)

        self.setLayout(self.layout)

        self.file_widget.currentItemChanged.connect(self._display_img)

        self.ctrl = ctrl
        self.viewer = viewer

    def _update_shuff_text(self, checked: bool):
        """
        Update shuffle button text to reflect toggle state.

        Parameters
        ----------
        checked : bool
            Toggle state of shuffle button.
        """
        if checked:
            self.shuffle.setText("Unshuffle and Unhide")
        else:
            self.shuffle.setText("Shuffle and Hide")

    def reset_buttons(self):
        self._toggle_delete(False)
        self._toggle_shuffle(False)
        self.toggle_add(True)

    def _delete_clicked(self):
        if len(self.file_widget.checked) > 0:
            msg_box = QMessageBox()
            msg: str = "Are you sure you want to delete these files?\n"
            for item in self.file_widget.checked:
                msg = msg + "--- " + item.file_path + "\n"

            msg_box.setText(msg)
            msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)

            return_value = msg_box.exec()
            if return_value == QMessageBox.Yes:
                self.file_widget.delete_checked()
        else:
            self.alert("No Images Selected")

    def alert(self, alert_msg: str):
        """
        Displays an error alert on the napari viewer.

        Parameters
        ----------
        alert_msg : str
            The message to be displayed
        """
        # TODO: move to main view
        show_info(alert_msg)

    def toggle_add(self, enable: bool):
        """
        Enables add file and add directory buttons.

        Parameters
        ----------
        enable : bool
            The enable state
        """
        self.input_dir.toggle(enable)
        self.input_file.toggle(enable)

    def _toggle_delete(self, checked: bool):
        """
        Enable delete button when files are checked.

        Parameters
        ----------
        checked : bool
        """
        if checked:
            self.delete.setEnabled(True)
        elif not checked:
            self.delete.setEnabled(False)

    def _toggle_shuffle(self, files_added: bool):
        """
        Enable shuffle button when files are added.

        Parameters
        ----------
        files_added : bool
        """
        if files_added:
            self.shuffle.setEnabled(True)
        elif not files_added:
            self.shuffle.setEnabled(False)

    def _display_img(self, current: ListItem, previous: ListItem):
        """Display the current image in napari."""
        self.viewer.layers.clear()
        if previous is not None:
            previous.unhighlight()
        if current is not None:
            try:
                img = AICSImage(current.file_path)
                self.viewer.add_image(img.data)
                current.highlight()
            except exceptions.UnsupportedFileFormatError:
                self.alert("AICS Unsupported File Type")
            except FileNotFoundError:
                self.alert("File no longer exists")
                self.file_widget.remove_item(current)
