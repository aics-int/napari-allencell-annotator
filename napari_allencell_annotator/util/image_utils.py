from pathlib import Path
from bioio import BioImage
import bioio_ome_tiff
import bioio_czi
import bioio_imageio
import napari


class ImageUtils:
    def __init__(self, filepath: Path):
        extension: str = filepath.suffix

        self._image: BioImage
        if extension in [".tiff", ".tif"]:
            self._image = BioImage(filepath, reader=bioio_ome_tiff.Reader)
        elif extension == ".czi":
            self._image = BioImage(filepath, reader=bioio_czi.Reader)
        else:
            self._image = BioImage(filepath, reader=bioio_imageio.Reader)

    def add_image(self, viewer: napari.viewer):
        viewer.add_image(self._image.data)


