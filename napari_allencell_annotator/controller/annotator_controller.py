import json
from view.annotator_view import AnnotatorView, AnnotatorViewMode
from util.directories import Directories
import napari
import os



class AnnotatorController():
    def __init__(self, napari : napari.Viewer):
        path = str(Directories.get_assets_dir() / "sample2.json")
        data = json.load(open(path))
        #self.view = AnnotatorView(napari.Viewer(), data)
        self.view = AnnotatorView(napari, data,mode=AnnotatorViewMode.VIEW)
        #self._connect_slots()


