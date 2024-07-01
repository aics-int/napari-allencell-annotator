import numpy as np

from napari_allencell_annotator.view.i_viewer import IViewer
import napari


class Viewer(IViewer):
    """Handles actions related to napari viewer"""

    def __init__(self, viewer: napari.Viewer):
        super().__init__()
        self.viewer: napari.Viewer = viewer

    def add_image(self, image: np.ndarray) -> None:
        """
        Add an image to the napari viewer

        Parameters
        ----------
        image: np.ndarray
            An image to be added
        """
        self.viewer.add_image(image)

    def clear_layers(self) -> None:
        """
        Clear all images from the napari viewer
        """
        self.viewer.layers.clear()
