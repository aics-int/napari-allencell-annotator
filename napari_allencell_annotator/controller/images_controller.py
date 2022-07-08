import os
from typing import List, Dict
import random

import napari

from napari_allencell_annotator.view.images_view import ImagesView
from napari_allencell_annotator.model import images_model
from napari_allencell_annotator.constants.constants import SUPPORTED_FILE_TYPES


class ImagesController:
    """
    A Main controller to integrate view and model for image annotations

    Attributes
    ----------
    model
        the model functions
    view
        the GUI and napari viewer

    Methods
    -------
    is_supported(file_name:str)->bool
        Returns True if a file is a supported file type.

    start_annotating()
        Sets the current item.

    curr_img_dict() -> Dict[str,str]
        Returns a dictionary with the current image attributes.

    next_img()
        Sets the current image to the next in the list.

    prev_img()
        Sets the current image to the previous one in the list.

    get_num_files(self) -> int
        Returns the number of files.
    """

    def __init__(self, viewer: napari.Viewer):
        self.model: images_model = images_model
        self.view: ImagesView = ImagesView(viewer, self)
        self.view.show()
        self._connect_slots()

    def _connect_slots(self):
        """Connects signals to slots. """
        self.view.input_dir.file_selected.connect(self._dir_selected_evt)
        self.view.input_file.file_selected.connect(self._file_selected_evt)
        self.view.shuffle.clicked.connect(self._shuffle_clicked)

    def _shuffle_clicked(self, checked: bool):
        """
        Shuffle file order and hide file names if checked.
        Return files to original order and names if unchecked.

        Side effect: set file_widget.shuffle_order to a new order or [] if list is unshuffled.

        Parameters
        ----------
        checked : bool
            Toggle state of the shuffle button.
        """
        files: List[str] = [i for i in self.view.file_widget.clear_for_shuff()]
        if checked:
            self.view.toggle_add(False)
            random.shuffle(files)
            self.view.file_widget.set_shuff_order(files)
            for f in files:
                self.view.file_widget.add_item(f, hidden=True)

        else:
            self.view.toggle_add(True)
            for f in files:
                self.view.file_widget.add_item(f, hidden=False)

    @staticmethod
    def is_supported(file_name: str) -> bool:
        """
        Check if the provided file name is a supported file.

        This function checks if the file name extension is in
        the supported file types files.

        Parameters
        ----------
        file_name : str
            Name of the file to check.

        Returns
        -------
        bool
            True if the file is supported.
        """
        if file_name is None:
            return False
        _, extension = os.path.splitext(file_name)
        if extension in SUPPORTED_FILE_TYPES:
            return True
        else:
            return False

    def _dir_selected_evt(self, dir_list: List[str]):
        """
        Adds all files in a directory to the GUI.

        Parameters
        ----------
        dir_list : List[str]
            The input list with dir[0] holding directory name.
        """
        if dir_list is not None and len(dir_list) > 0:
            d = dir_list[0]
            if len(os.listdir(d)) < 1:
                self.view.alert("Folder is empty")
            else:
                for file in os.listdir(d):
                    file = d + "/" + file
                    if self.is_supported(file):
                        self.view.file_widget.add_new_item(file)
                    else:
                        self.view.alert("Unsupported file type:" + file)
        else:
            self.view.alert("No selection provided")

    def _file_selected_evt(self, file_list: List[str]):
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
                    self.view.file_widget.add_new_item(file)
                else:
                    self.view.alert("Unsupported file type:" + file)

    def start_annotating(self):
        """Set current item to the first item."""
        if self.view.file_widget.count() > 0:
            self.view.file_widget.setCurrentItem(self.view.file_widget.item(0))
        else:
            self.view.alert("No files to annotate")

    def stop_annotating(self):
        self.view.file_widget.clear_all()
        self.view.reset_buttons()

    def curr_img_dict(self) -> Dict[str,str]:
        """
         Return a dictionary with the current image File Path,
         File Name, FMS info, and row in the list.

        Returns
        ----------
        Dict[str,str]
            dictionary of attributes.
        """
        item = self.view.file_widget.currentItem()
        info = {"File Name": item.get_name(), "File Path": item.file_path, "FMS": "",
                "Row": str(self.view.file_widget.get_curr_row())}
        return info

    def next_img(self):
        """
        Set the current image to the next in the list, stop incrementing
        at the last row.
        """
        if self.view.file_widget.get_curr_row() < self.view.file_widget.count() - 1:
            self.view.file_widget.setCurrentItem(self.view.file_widget.item(self.view.file_widget.get_curr_row() + 1))

    def prev_img(self):
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
        return self.view.file_widget.count()
