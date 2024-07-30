from typing import List, Tuple

import numpy as np
from napari.layers import Layer, Points

from napari_allencell_annotator.view.i_viewer import IViewer


class FakeViewer(IViewer):
    def __init__(self):
        super().__init__()

        self._layers = []
        self._point_layers = []
        self.alerts = []

    def add_image(self, image: np.ndarray) -> None:
        self._layers.append(image)

    def clear_layers(self) -> None:
        self._layers.clear()

    def alert(self, alert_msg: str) -> None:
        self.alerts.append(alert_msg)

    def get_layers(self) -> List[Layer]:
        return self._layers

    def get_all_points(self) -> List[Points]:
        return self._point_layers

    def create_points(self, name: str, color: str, visible: bool) -> Points:
        points: Points = Points(data=None, name=name, color=color, visible=visible)
        self._point_layers.append(points)
        return points

    def get_points(self, point_layer: Points, image_dims_order: str) -> List[Tuple]:
        return [(0, 0, 0, 0, 0)]
