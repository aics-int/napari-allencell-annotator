from typing import List, Tuple

import numpy as np
from napari.layers import Layer, Points

from napari_allencell_annotator.view.i_viewer import IViewer
from bioio import BioImage


class FakeViewer(IViewer):
    def __init__(self):
        super().__init__()

        self._layers = []
        self._points_layers = []
        self.alerts = []

    def add_image(self, image: BioImage) -> None:
        self._layers.append(image)

    def clear_layers(self) -> None:
        self._layers.clear()

    def alert(self, alert_msg: str) -> None:
        self.alerts.append(alert_msg)

    def get_layers(self) -> List[Layer]:
        return self._layers

    def get_all_points_layers(self) -> List[Points]:
        return self._points_layers

    def create_points_layer(self, name: str, color: str, visible: bool, ndim: int) -> Points:
        points: Points = Points(data=None, name=name, color=color, visible=visible, ndim=ndim)
        self._points_layers.append(points)
        return points

    def get_selected_points(self, point_layer: Points) -> List[Tuple]:
        return list(map(tuple, point_layer.data))
