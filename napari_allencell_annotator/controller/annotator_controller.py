import json
from view.annotator_view import AnnotatorView, AnnotatorViewMode
from util.directories import Directories
import napari


class AnnotatorController:
    """
    A class used to control the model and view for annotations.

    Inputs
    ----------
    viewer : napari.Viewer
        a napari viewer where the plugin will be used

    Methods
    -------
    """

    def __init__(self, viewer: napari.Viewer):
        path = str(Directories.get_assets_dir() / "sample2.json")
        data = json.load(open(path))
        # self.view = AnnotatorView(napari.Viewer(), data)
        self.view = AnnotatorView(viewer, data, mode=AnnotatorViewMode.VIEW)
        # self._connect_slots()
