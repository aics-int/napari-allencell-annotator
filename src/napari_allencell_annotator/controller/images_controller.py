import os

import napari
from PyQt5.QtWidgets import QListWidgetItem

from napari_allencell_annotator.view.images_view import ImagesView
from napari_allencell_annotator.model import images_model
from aicsimageio import exceptions, AICSImage
from napari_allencell_annotator.constants.constants import SUPPORTED_FILE_TYPES


class ImageController():#TODO: rename
    """
    A Main controller to integrate view and model for image annotations

    Attributes
    ----------
    model: TODO
        the model functions
    view: TODO
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
            self.view.error_alert("AICS Image Conversion Failed")


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