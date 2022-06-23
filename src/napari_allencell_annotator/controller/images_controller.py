import os
from typing import List

import napari
from PyQt5.QtWidgets import QListWidgetItem

from napari_allencell_annotator.view.images_view import ImagesView
from napari_allencell_annotator.model import images_model
from aicsimageio import exceptions, AICSImage
from napari_allencell_annotator.constants.constants import SUPPORTED_FILE_TYPES


class ImagesController():
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
    """
    def __init__(self):
        self.model = images_model
        self.view = ImagesView(napari.Viewer(),self)
        self._connect_slots()

    def _connect_slots(self):
        """Connects signals to slots. """
        self.view.file_widget.currentItemChanged.connect(self._curr_img_change)
        self.view.input_dir.file_selected.connect(lambda: self._dir_selected(self.view.get_dir()))
        self.view.input_file.file_selected.connect(lambda: self._file_selected(self.view.get_file()))

    def _curr_img_change(self, event:QListWidgetItem.ItemType):
        """
        Converts image selection into an AICSImage.

        This function uses the model to convert the image
        selected into an AICS image. If the conversion is successful
        the view's current image is changed. Alert user of a failed AICS conversion.

        Parameters
        ----------
        event : QListWidgetItem.ItemType
        """
        try:
            img = AICSImage(event.file_path).data
            self.view.set_curr_img(img)
        except exceptions.UnsupportedFileFormatError:
            self.view.alert("AICS Image Conversion Failed")


    def is_supported(self, file_name: str) -> bool:
        """
        Check if the provided file name is a supported file.

        This function checks if the file name extension is in
        the supported file types set.

        Parameters
        ----------
        file_name : str
            Name of the file to check.

        Returns
        -------
        bool
            True if the file is supported.
        """
        _, extension = os.path.splitext(file_name)
        if extension in SUPPORTED_FILE_TYPES:
            return True
        else:
            return False

    def _dir_selected(self, dir: str):
        """
        Adds all files in a directory to the GUI.

        Parameters
        ----------
        dir : str
            The directory path
        """
        if dir is None:
            self.view.alert("No selection provided")
        elif len(os.listdir(dir)) < 1:
            self.view.alert("Folder is empty")
        else:
            for file in os.listdir(dir):
                file = dir + "/" + file
                if self.is_supported(file):
                    self.view.add_file(file)
                else:
                    self.view.alert("Unsupported file type:" + file)


    def _file_selected(self, file_list: List[str]):
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
                if self. is_supported(file):
                    self._add_file(file)
                else:
                    self.view.alert("Unsupported file type:" + file)