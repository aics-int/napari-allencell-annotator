import json
from view.annotator_view import AnnotatorView
import napari
import os



class AnnotatorController():
    def __init__(self):
        data = json.load(open('sample.json'))
        self.view: AnnotatorView = AnnotatorView(napari.Viewer(), data)
        #self._connect_slots()


