from qtpy.QtWidgets import QFrame
from qtpy.QtCore import Qt

from qtpy.QtWidgets import (
    QLabel,
    QScrollArea,
    QGridLayout,
    QPushButton,
)
import napari
from aicsimageio import AICSImage, exceptions
from napari.utils.notifications import show_info

from napari_allencell_annotator.widgets.file_input import (
    FileInput,
    FileInputMode,
)
from napari_allencell_annotator.widgets.files_widget import FilesWidget, FileItem
from napari_allencell_annotator._style import Style


class ImagesView(QFrame):
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
    update_num_files_label(num_files:int)
        Updates num_files_label to show the current number of image files
    """

    def __init__(self, viewer: napari.Viewer):
        """
        Parameters
        ----------
        viewer : napari.Viewer
            The napari viewer for the plugin
        """
        super().__init__()

        self.setStyleSheet(Style.get_stylesheet("main.qss"))

        self.label: QLabel = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("Images")

        self.layout: QGridLayout = QGridLayout()
        self.layout.addWidget(self.label, 0, 0, 1, 4)

        self.input_dir: FileInput
        self.input_file: FileInput

        self.input_dir = FileInput(mode=FileInputMode.DIRECTORY, placeholder_text="Add a folder...")

        self.input_file = FileInput(mode=FileInputMode.FILE, placeholder_text="Add files...")
        self.layout.addWidget(self.input_dir, 1, 0, 1, 2)
        self.layout.addWidget(self.input_file, 1, 2, 1, 2)

        self.file_widget: FilesWidget = FilesWidget()

        self.scroll: QScrollArea = QScrollArea()
        self.scroll.setWidget(self.file_widget)
        self.scroll.setWidgetResizable(True)
        self.scroll.horizontalScrollBar().setEnabled(False)
        self.layout.addWidget(self.scroll, 2, 0, 10, 4)

        self.num_files_label: QLabel = QLabel("Image files:")
        self.layout.addWidget(self.num_files_label, 13, 0, 1, 4)

        self.shuffle: QPushButton = QPushButton("Shuffle and Hide")
        self.shuffle.setCheckable(True)

        self.shuffle.setEnabled(False)

        self.delete: QPushButton = QPushButton("Delete All")
        self.delete.setEnabled(False)

        self.layout.addWidget(self.shuffle, 14, 0, 1, 3)
        self.layout.addWidget(self.delete, 14, 3, 1, 1)

        self.setLayout(self.layout)

        self.viewer: napari.viewer = viewer
        self._connect_slots()

    def _connect_slots(self) -> None:
        """Connect signals to slots."""
        self.file_widget.files_selected.connect(self._toggle_delete)
        self.file_widget.files_added.connect(self._toggle_shuffle)

        self.shuffle.toggled.connect(self._update_shuff_text)
        self.file_widget.currentItemChanged.connect(self._display_img)

    def _update_shuff_text(self, checked: bool) -> None:
        """
        Update shuffle button text to reflect toggle state.

        Parameters
        ----------
        checked : bool
            Toggle state of shuffle button.
        """
        if checked:
            self.shuffle.setText("Unhide")
        else:
            self.shuffle.setText("Shuffle and Hide")

    def reset_buttons(self) -> None:
        """
        Reset buttons to pre-annotation settings

        Disable delete, add, and shuffle buttons.
        """
        self._toggle_delete(False)
        self.shuffle.setChecked(False)
        self._toggle_shuffle(False)
        self.toggle_add(True)

    def alert(self, alert_msg: str) -> None:
        """
        Displays an error alert on the napari viewer.

        Parameters
        ----------
        alert_msg : str
            The message to be displayed
        """
        show_info(alert_msg)

    def toggle_add(self, enable: bool) -> None:
        """
        Enables add file and add directory buttons.

        Parameters
        ----------
        enable : bool
            The enable state
        """
        self.input_dir.toggle(enable)
        self.input_file.toggle(enable)

    def _toggle_delete(self, checked: bool) -> None:
        """
        Enable delete button when files are checked.

        Parameters
        ----------
        checked : bool
        """
        if checked:
            self.delete.setText("Delete Selected")
        elif not checked:
            self.delete.setText("Delete All")

    def _toggle_shuffle(self, files_added: bool) -> None:
        """
        Enable shuffle button when files are added.

        Parameters
        ----------
        files_added : bool
        """
        if files_added:
            self.delete.setToolTip("Check box on the right \n to select files for deletion")
            self.delete.setText("Delete All")
            self.shuffle.setEnabled(True)
            self.delete.setEnabled(True)
        elif not files_added:
            self.delete.setToolTip(None)
            self.shuffle.setEnabled(False)
            self.delete.setEnabled(False)

    def _display_img(self, current: FileItem, previous: FileItem) -> None:
        """
        Display the current image in napari.

        Parameters
        ----------
        current: FileItem
            Current file
        previous: FileItem
            Previous file
        """
        self.viewer.layers.clear()
        if previous is not None:
            previous.unhighlight()
        if current is not None:
            try:
                img: AICSImage = AICSImage(current.file_path)
                self.viewer.add_image(img.data)
                current.highlight()
            except exceptions.UnsupportedFileFormatError:
                self.alert("AICS Unsupported File Type")

    def update_num_files_label(self, num_files: int) -> None:
        """
        Update num_files_label to show the number of image files

        Parameters
        ----------
        num_files: int
            The number of image files
        """
        self.num_files_label.setText(f"Image files: {num_files}")
