from pathlib import Path
import random
from typing import Optional

from PyQt5.QtWidgets import QListWidgetItem

from napari_allencell_annotator.model.annotation_model import AnnotatorModel
from napari_allencell_annotator.view.i_viewer import IViewer
from napari_allencell_annotator.widgets.file_scrollable_popup import FileScrollablePopup
from napari_allencell_annotator.widgets.popup import Popup
from qtpy.QtWidgets import QFrame
from qtpy.QtCore import Qt
from qtpy.QtCore import Signal

from qtpy.QtWidgets import (
    QLabel,
    QScrollArea,
    QGridLayout,
    QPushButton,
)
from aicsimageio import AICSImage, exceptions

from napari_allencell_annotator.widgets.file_input import (
    FileInput,
    FileInputMode,
)
from napari_allencell_annotator.widgets.files_widget import FilesWidget, FileItem
from napari_allencell_annotator.util.file_utils import FileUtils
from napari_allencell_annotator._style import Style
from napari_allencell_annotator.model.images_model import ImagesModel


class ImagesView(QFrame):
    """
    A class used to create a view for image file uploading and selecting.

    Attributes
    ----------
    viewer : IViewer
        a viewer where the plugin will be used
    ctrl : ImagesController
        a controller for the view

    Methods
    -------
    alert(alert:str)
        Displays the alert message on the napari viewer
    update_num_files_label(num_files:int)
        Updates num_files_label to show the current number of image files
    """
    def __init__(self, annotator_model: AnnotatorModel, viewer: IViewer):
        """
        Parameters
        ----------
        viewer : IViewer
            The viewer for the plugin
        """
        self._annotator_model: AnnotatorModel = annotator_model
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

        self.file_widget: FilesWidget = FilesWidget(self._annotator_model)

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

        self.viewer: IViewer = viewer
        self._connect_slots()

    def _connect_slots(self) -> None:
        """Connect signals to slots."""
        self.input_dir.dir_selected.connect(self._add_selected_dir_to_ui)
        self.input_file.files_selected.connect(self._add_selected_files)
        self.shuffle.clicked.connect(self._handle_shuffle_clicked)
        self.delete.clicked.connect(self._handle_delete_clicked)
        self.file_widget.files_selected.connect(self._toggle_delete_button_text)

        self.shuffle.toggled.connect(self._update_shuff_text)
        self._annotator_model.image_changed.connect(self._display_img)
        self._annotator_model.at_least_one_file_available.connect(self._handle_at_least_one_file_available)

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
        self._toggle_delete_button_text(False)
        self.shuffle.setChecked(False)
        self._disable_delete_button()
        self._disable_shuffle_button()
        self.enable_add_buttons()

    def enable_add_buttons(self) -> None:
        """Enables add file and add directory buttons."""
        self.input_dir.toggle(True)
        self.input_file.toggle(True)

    def disable_add_buttons(self) -> None:
        """Disables add file and add directory buttons."""
        self.input_dir.toggle(False)
        self.input_file.toggle(False)

    def _toggle_delete_button_text(self, checked: bool) -> None:
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

    def _enable_delete_button(self) -> None:
        """Enable delete button"""
        self.delete.setToolTip("Check box on the right \n to select files for deletion")
        self.delete.setText("Delete All")
        self.delete.setEnabled(True)

    def _disable_delete_button(self) -> None:
        """Disable delete button"""
        self.delete.setToolTip(None)
        self.delete.setEnabled(False)

    def _enable_shuffle_button(self) -> None:
        """Enable shuffle button"""
        self.shuffle.setEnabled(True)

    def _disable_shuffle_button(self) -> None:
        """Disable shuffle button"""
        self.shuffle.setEnabled(False)

    def _handle_at_least_one_files_available(self, at_least_one: bool) -> None:
        """
        Enable or disable delete and shuffle buttons when files are added.

        Parameters
        ----------
        files_added : bool
        """
        if at_least_one:
            self._enable_delete_button()
            self._enable_shuffle_button()
        else:
            self._disable_delete_button()
            self._disable_shuffle_button()

    def _display_img(self) -> None:
        """
        Display the current image in napari.

        Parameters
        ----------
        current: FileItem
            Current file
        previous: FileItem
            Previous file
        """
        self.viewer.clear_layers()
        previous = self._annotator_model.get_previous_image_index()
        if previous is not None:
           self.file_widget.item(previous).unhighlight()

        current = self.file_widget.item(self._annotator_model.get_curr_img_index())
        if current is not None:
            try:
                img: AICSImage = AICSImage(current.file_path)  # TODO update to bioio
                self.viewer.add_image(img.data)
                current.highlight()
            except exceptions.UnsupportedFileFormatError:
                self.viewer.alert("AICS Unsupported File Type")

    def update_num_files_label(self, num_files: int) -> None:
        """
        Update num_files_label to show the number of image files

        Parameters
        ----------
        num_files: int
            The number of image files
        """
        self.num_files_label.setText(f"Image files: {num_files}")

    def _add_selected_dir_to_ui(self, dir_path: Path) -> None:
        """
        Adds all files in a directory to the GUI.

        Parameters
        ----------
        dir_list : List[Path]
            The input list with dir[0] holding directory name.
        """
        all_files_in_dir: list[Path] = FileUtils.get_files_in_dir(dir_path)

        if len(all_files_in_dir) < 1:
            self.viewer.alert("Folder is empty")
        else:
            self._add_selected_files(all_files_in_dir)

    def add_new_item(self, file: Path, hidden: Optional[bool] = False) -> None:
        """
        Add a new image to the model and the file widget.

        Optional hidden parameter toggles file name visibility. This function emits a files_added signal when this is
        the first file added and updates num_files_label.

        Parameters
        ----------
        file: Path
            The file path of a new image to be added
        hidden : Optional[bool]
            File name visibility
        """
        self.file_widget.add_item(file, hidden)
        self._annotator_model.add_image(file)  # update model
        self.update_num_files_label(self._annotator_model.get_num_images())

    def _add_selected_files(self, file_list: list[Path]) -> None:
        """
        Adds all selected files to the GUI and update state

        Parameters
        ----------
        file_list : List[Path]
            The list of files
        """
        # ignore hidden files and directories
        for file_path in FileUtils.select_only_valid_files(file_list=file_list):
            if FileUtils.is_supported(file_path):
                if file_path not in self._annotator_model.get_all_images():
                    self.add_new_item(file_path)
            else:
                self.viewer.alert("Unsupported file type(s)")

    def _handle_shuffle_clicked(self, checked: bool) -> None:
        """
        Shuffle file order and hide file names if checked.
        Return files to original order and names if unchecked.

        Side effect: set file_widget.shuffled_files_dict to a new order dict or {} if list is unshuffled.

        Parameters
        ----------
        checked : bool
            Toggle state of the shuffle button.
        """
        if checked:
            self._shuffle_file_order()
        else:
            self.enable_add_buttons()
            self.file_widget.set_shuffled(False)
            self.file_widget.unhide_all()

    def _shuffle_file_order(self):
        # TODO: set shuffled state in model, file widget clears and repopulates on its own.
        files: list[Path] = self._annotator_model.get_all_images()
        if len(files) > 0:
            self.disable_add_buttons()
            # clear file widget
            self.file_widget.clear_for_shuff()
            random.shuffle(files)
            self._annotator_model.set_all_images(files)
            for file in self._annotator_model.get_all_images():
                # add with shuffled order
                self.file_widget.add_item(file, hidden=True)

    def _handle_delete_clicked(self) -> None:
        """
        Ask user to approve a list of files to delete and remove image files from the model and the file widget.

        If at least one file is checked, delete only selected files. Otherwise, delete all files.
        """
        # TODO can we do this with signals instead?
        if len(self.file_widget.checked) > 0:
            proceed: bool = FileScrollablePopup.make_popup(
                "Delete these files from the list?", self.file_widget.checked
            )
            if proceed:
                self.delete_checked()
        else:
            proceed: bool = Popup.make_popup("Remove all images?")
            if proceed:
                self.clear_all()
                self.reset_buttons()

    def delete_checked(self) -> None:
        """
        Delete the checked items from the model and the file widget.
        """
        for item in self.file_widget.checked:
            self.remove_image(item)

        self.file_widget.checked.clear()

    def remove_image(self, item: FileItem) -> None:
        """
        Remove an image file from the model and the file widget.

        This function emits a files_added signal when the item to remove is the only item and updates num_files_label.

        Parameters
        ----------
        item: FileItem
            An item to be removed.
        """
        # TODO when we delete from the model, connect file widget so that it deletes that entry itself without
        # us explicitly calling remove_item on it
        if item.file_path in self._annotator_model.get_all_images():
            self._annotator_model.remove_image(item.file_path)
            self.file_widget.remove_item(item)
            self.update_num_files_label(self._annotator_model.get_num_images())

    def clear_all(self) -> None:
        """
        Clear all image data from the model and the file widget.
        """
        self._annotator_model.set_all_images([])  # clear model
        self.file_widget.clear_all()  # clear widget
        self.update_num_files_label(self._annotator_model.get_num_images())  # update label

    def start_annotating(self) -> None:
        """Set current item to the one at row."""
        count: int = self.file_widget.count()
        for x in range(count):
            file_item: Optional[QListWidgetItem] = self.file_widget.item(x)
            file_item.hide_check()
        else:
            self.viewer.alert("No files to annotate")

    def hide_image_paths(self) -> None:
        """
        Hide image paths (if shuffle is selected for annotations)
        """
        self.input_dir.hide()
        self.input_file.hide()
        self.shuffle.hide()
        self.delete.hide()