from pathlib import Path

import numpy as np
from bioio import BioImage
import bioio_ome_tiff
import bioio_czi
import bioio_imageio


class ImageUtils:
    """
    Handles image display with BioImage

    Attributes
    ----------
    _image: BioImage
        An image to be displayed

    Methods
    -------
    add_image(self, viewer: napari.Viewer) -> None
        Shows the image in the viewer
    """

    def __init__(self, filepath: Path):

        extension: str = filepath.suffix

        self._image: BioImage
        if extension in [".tiff", ".tif"]:
            self._image = BioImage(filepath, reader=bioio_ome_tiff.Reader)
        elif extension == ".czi":
            self._image = BioImage(filepath, reader=bioio_czi.Reader)
        else:
            self._image = BioImage(filepath, reader=bioio_imageio.Reader)

    def get_image(self) -> BioImage:
        """
        Returns Bioimage object loaded with correct reader
        """
        return self._image