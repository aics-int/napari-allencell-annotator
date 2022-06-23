"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from magicgui import magic_factory
from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget
from napari_allencell_annotator.view.images_view import ImagesView

if TYPE_CHECKING:
    import napari


class MainWidget(QMainWindow):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.central_layout = QVBoxLayout()
        self.viewer = napari_viewer
        self.layer = None
        self.drag_drop = ImagesView(self.viewer, self.layer)
        self.central_layout.addWidget(self.drag_drop, stretch=2)
        self.central_layout.addWidget(self.annotator, stretch=5)

        self.central.setLayout(self.central_layout)



@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return [MainWidget, {"name": "Workflow editor"}]