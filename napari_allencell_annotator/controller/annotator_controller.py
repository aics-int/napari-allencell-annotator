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
        # 1 annotation
        # path = str(Directories.get_assets_dir() / "sample3.json")
        # 4 annotations
        # path = str(Directories.get_assets_dir() / "sample.json")
        # 8 annotations
        path = str(Directories.get_assets_dir() / "sample2.json")
        data = json.load(open(path))
        # open in add mode
        # self.view = AnnotatorView(napari.Viewer(), data)
        # open in view mode
        self.view = AnnotatorView(viewer, data, mode=AnnotatorViewMode.VIEW)
        # open in annotate mode
        # self.view = AnnotatorView(viewer, data, mode=AnnotatorViewMode.ANNOTATE)
