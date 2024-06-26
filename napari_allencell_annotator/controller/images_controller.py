import os
from pathlib import Path
from typing import List, Dict, Optional
import random

from PyQt5.QtWidgets import QListWidgetItem

import napari

from napari_allencell_annotator.view.images_view import ImagesView
from napari_allencell_annotator.model.images_model import ImagesModel
from napari_allencell_annotator.constants.constants import SUPPORTED_FILE_TYPES
from napari_allencell_annotator.widgets.file_item import FileItem
from napari_allencell_annotator.widgets.popup import Popup
from napari_allencell_annotator.widgets.file_scrollable_popup import FileScrollablePopup


class ImagesController:
    """
    A Main controller to integrate view and model for image annotations

    Attributes
    ----------
    view
        the GUI and napari viewer

    Methods
    -------
    load_from_csv(files : List[str], shuffled: bool)
        Adds files to file list from a csv list of file paths.

    get_files_dict() -> Dict[str,List[str]], bool
        Returns the file dictionary that has the current file order and boolean shuffled.

    is_supported(file_path:str) -> bool
        Returns True if a file is a supported file type.

    start_annotating(row: Optional[int] = 0)
        Sets the current item to the one at row.

    stop_annotating()
        Clears file widget, clears model, and resets buttons.

    curr_img_dict() -> Dict[str,str]
        Returns a dictionary with the current image attributes.

    next_img()
        Sets the current image to the next in the list.

    prev_img()
        Sets the current image to the previous one in the list.

    get_num_files() -> int
        Returns the number of files.

    remove_item(item: FileItem)
        Removes an image file from the model and the file widget.

    delete_checked()
        Deletes the checked items from the model and the file widget.

    clear_all()
        Clears all image data from the model and the file widget.

    add_new_item(file: str, hidden: Optional[bool] = False)
        Adds a new image to the model and the file widget.

    delete_clicked()
        Asks user to approve a list of files to delete and removes image files from the model and the file widget.
    """

    def __init__(self, viewer: napari.Viewer):
        self.view: ImagesView = ImagesView(viewer)
        self.view.show()
        self._connect_slots()
        self.model: ImagesModel = ImagesModel()

    def _connect_slots(self) -> None:
        """Connects signals to slots."""
        self.view.input_dir.file_selected.connect(self._dir_selected_evt)
        self.view.input_file.file_selected.connect(self._file_selected_evt)
        self.view.shuffle.clicked.connect(self._shuffle_clicked)
        self.view.delete.clicked.connect(self._delete_clicked)

    def load_from_csv(self, files: List[str], shuffled: bool) -> None:
        """
        Clear current file list and add file list from csv with its shuffle state.

        If the csv files are shuffled, set shuffled property, hide add button, and hide file names.

        Parameters
        __________
        files : List[str]
            a list of file paths.
        shuffled: bool
            true if files are shuffled.
        """
        self.clear_all()  # sets shuffled to false
        for name in files:
            self.add_new_item(name, shuffled)
        if shuffled:
            self.view.file_widget.set_shuffled(True)
            self.view.toggle_add(False)

        self.view.shuffle.setChecked(shuffled)

    def get_files_dict(self) -> (Dict[str, List[str]], bool):
        """
        Return the file dictionary and the shuffle state of file_widget.

        Returns
        ----------
        Dict[str,List[str]], bool
            dictionary of file info. keys in order. a boolean shuffled.
        """
        return self.model.get_files_dict(), self.view.file_widget.shuffled

    def _shuffle_clicked(self, checked: bool) -> None:
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
            self.view.file_widget.clear_for_shuff()
            files: Dict[str, List[str]] = self.model.get_files_dict()
            if len(files) > 0:
                self.view.toggle_add(False)
                keys: List = list(files.keys())
                self.model.set_files_dict({})
                random.shuffle(keys)
                for k in keys:
                    # add new item will recreate files_dict in new order
                    self.add_new_item(k, hidden=True)

        else:
            self.view.toggle_add(True)
            self.view.file_widget.set_shuffled(False)
            self.view.file_widget.unhide_all()

    @staticmethod
    def is_supported(file_path: str) -> bool:
        """
        Check if the provided file name is a supported file.

        This function checks if the file name extension is in
        the supported file types files.

        Parameters
        ----------
        file_path : str
            Name of the file to check.

        Returns
        -------
        bool
            True if the file is supported.
        """
        if file_path is None:
            return False
        extension: str = Path(file_path).suffix
        if extension in SUPPORTED_FILE_TYPES:
            return True
        else:
            return False

    def _dir_selected_evt(self, dir_list: List[str]) -> None:
        """
        Adds all files in a directory to the GUI.

        Parameters
        ----------
        dir_list : List[str]
            The input list with dir[0] holding directory name.
        """
        if dir_list is not None and len(dir_list) > 0:
            d: str = dir_list[0]
            if len(os.listdir(d)) < 1:
                self.view.alert("Folder is empty")
            else:
                for file in [file for file in os.listdir(d) if not file.startswith(".")]:

                    file = d + "/" + file
                    if self.is_supported(file):
                        self.add_new_item(file)
                    else:
                        self.view.alert("Unsupported file type(s)")

        else:
            self.view.alert("No selection provided")

    def _file_selected_evt(self, file_list: List[str]) -> None:
        """
        Adds all selected files to the GUI.

        Parameters
        ----------
        file_list : List[str]
            The list of files
        """
        if file_list is None or len(file_list) < 1:
            self.view.alert("No selection provided")
        else:
            for file in file_list:
                if self.is_supported(file):
                    self.add_new_item(file)
                else:
                    self.view.alert("Unsupported file type(s)")

    def start_annotating(self, row: Optional[int] = 0) -> None:
        """Set current item to the one at row."""
        count: int = self.view.file_widget.count()
        for x in range(count):
            file_item: Optional[QListWidgetItem] = self.view.file_widget.item(x)
            file_item.hide_check()
        if count > 0:
            self.view.file_widget.setCurrentItem(self.view.file_widget.item(row))

        else:
            self.view.alert("No files to annotate")

    def stop_annotating(self) -> None:
        """Clear file widget, clear model, and reset buttons."""
        self.clear_all()
        self.view.reset_buttons()

    def curr_img_dict(self) -> Dict[str, str]:
        """
         Return a dictionary with the current image File Path
         and row in the list.

        Returns
        ----------
        Dict[str,str]
            dictionary of file name and row attributes.
        """
        item: Optional[QListWidgetItem] = self.view.file_widget.currentItem()
        info: Dict[str, str] = {
            "File Path": item.file_path,
            "Row": str(self.view.file_widget.get_curr_row()),
        }
        return info

    def next_img(self) -> None:
        """
        Set the current image to the next in the list, stop incrementing
        at the last row.
        """
        if self.view.file_widget.get_curr_row() < self.view.file_widget.count() - 1:
            self.view.file_widget.setCurrentItem(self.view.file_widget.item(self.view.file_widget.get_curr_row() + 1))

    def prev_img(self) -> None:
        """Set the current image to the previous in the list, stop at first image."""
        if self.view.file_widget.get_curr_row() > 0:
            self.view.file_widget.setCurrentItem(self.view.file_widget.item(self.view.file_widget.get_curr_row() - 1))

    def get_num_files(self) -> int:
        """
        Returns
        ----------
        int
            number of files.
        """
        return self.model.get_num_files()

    def remove_item(self, item: FileItem) -> None:
        """
        Remove an image file from the model and the file widget.

        This function emits a files_added signal when the item to remove is the only item and updates num_files_label.

        Parameters
        ----------
        item: FileItem
            An item to be removed.
        """
        if item.file_path in self.model.get_files_dict().keys():
            self.model.remove_item(item)
            self.view.file_widget.remove_item(item)

            if self.model.get_num_files() == 0:
                self.view.file_widgetfiles_added.emit(False)

            self.view.update_num_files_label(self.model.get_num_files())

    def delete_checked(self) -> None:
        """
        Delete the checked items from the model and the file widget.
        """
        for item in self.view.file_widget.checked:
            self.remove_item(item)

        self.view.file_widget.checked.clear()
        self.view.file_widget.files_selected.emit(False)

    def clear_all(self) -> None:
        """
        Clear all image data from the model and the file widget.
        """
        self.model.set_files_dict(files_dict={})
        self.view.file_widget.clear_all()

        self.view.update_num_files_label(self.model.get_num_files())

    def add_new_item(self, file: str, hidden: Optional[bool] = False) -> None:
        """
        Add a new image to the model and the file widget.

        Optional hidden parameter toggles file name visibility. This function emits a files_added signal when this is
        the first file added and updates num_files_label.

        Parameters
        ----------
        file: str
            The file path of a new image to be added
        hidden : Optional[bool]
            File name visibility
        """
        if file not in self.model.get_files_dict().keys():
            self.model.add_item(file)
            self.view.file_widget.add_item(file, hidden)

            if self.model.get_num_files() == 1:
                self.view.file_widget.files_added.emit(True)

            self.view.update_num_files_label(self.model.get_num_files())

    def _delete_clicked(self) -> None:
        """
        Ask user to approve a list of files to delete and remove image files from the model and the file widget.

        If at least one file is checked, delete only selected files. Otherwise, delete all files.
        """
        if len(self.view.file_widget.checked) > 0:
            proceed: bool = FileScrollablePopup.make_popup(
                "Delete these files from the list?", self.view.file_widget.checked
            )
            if proceed:
                self.delete_checked()
        else:
            proceed: bool = Popup.make_popup("Remove all images?")
            if proceed:
                self.clear_all()
                self.view.reset_buttons()
