import numpy as np

from napari_allencell_annotator.view.i_viewer import IViewer
import napari

class Viewer(IViewer):
    def __init__(self, viewer: napari.Viewer):
        super().__init__()
        self.viewer: napari.Viewer = viewer

    def add_image(self, image: np.ndarray) -> None:
        self.viewer.add_image()

    def clear_layers(self) -> None:
        self.viewer.layers.clear()