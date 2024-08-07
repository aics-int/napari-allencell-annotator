from pathlib import Path

import numpy as np
import dask.array as da
from bioio import BioImage
import bioio_ome_tiff
import bioio_czi
import bioio_imageio
import bioio_ome_zarr


class ImageUtils:
    """
    Handles image display with BioImage

    Attributes
    ----------
    _image: BioImage
        An image to be displayed

    Methods
    -------
    get_dask_data(self) -> da.Array
        Returns the dask array of the image
    """

    def __init__(self, filepath: Path):

        extension: str = filepath.suffix

        self._image: BioImage
        if extension in [".tiff", ".tif"]:
            self._image = BioImage(filepath, reader=bioio_ome_tiff.Reader)
        elif extension == ".czi":
            self._image = BioImage(filepath, reader=bioio_czi.Reader)
        elif extension == ".zarr":
            self._image = BioImage(filepath, reader=bioio_ome_zarr.Reader)
        else:
            self._image = BioImage(filepath, reader=bioio_imageio.Reader)

    def get_image_dask_data(self) -> da.Array:
        """
        Returns image data as a dask array
        """
        return self._image.get_dask_stack()
