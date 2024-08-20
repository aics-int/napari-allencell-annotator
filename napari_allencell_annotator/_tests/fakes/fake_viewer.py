from typing import List, Tuple

import numpy as np
from napari.layers import Layer, Points

from napari_allencell_annotator.view.i_viewer import IViewer
from napari_allencell_annotator.view.viewer import PointsLayerMode


class FakeViewer(IViewer):
    def __init__(self):
        super().__init__()

        self._layers = []
        self.alerts = []
        self._layers_selection = []

    def add_image(self, image: np.ndarray) -> None:
        self._layers.append(image)

    def clear_layers(self) -> None:
        self._layers.clear()

    def alert(self, alert_msg: str) -> None:
        self.alerts.append(alert_msg)

    def get_layers(self) -> List[Layer]:
        return self._layers

    def get_all_points_layers(self) -> List[Points]:
        return [layer for layer in self.get_layers() if isinstance(layer, Points)]

    def create_points_layer(self, name: str, visible: bool, data: np.ndarray = None) -> Points:
        points: Points = Points(data=data, name=name, visible=visible, ndim=6)
        self._layers.append(points)
        return points

    def set_points_layer_mode(self, points_layer: Points, mode: PointsLayerMode) -> None:
        points_layer.mode = mode.value

    def get_points_layer_mode(self, points_layer: Points) -> str:
        return points_layer.mode

    def get_selected_points(self, point_layer: Points) -> List[Tuple]:
        return list(map(tuple, point_layer.data))

    def get_all_point_annotations(self) -> dict[str, list[tuple]]:
        all_point_annotations: dict[str, list[tuple]] = {}

        all_points_layers: list[Points] = self.get_all_points_layers()
        for points_layer in all_points_layers:
            all_point_annotations[points_layer.name] = self.get_selected_points(points_layer)

        return all_point_annotations

    def toggle_points_layer(self, annot_points_layer: Points) -> None:
        if self.get_points_layer_mode(annot_points_layer) == PointsLayerMode.PAN_ZOOM.value:
            self.set_all_points_layer_to_pan_zoom()
            self.set_points_layer_mode(annot_points_layer, PointsLayerMode.ADD)
            self._layers_selection: list[Layer] = []
            self._layers_selection.append(annot_points_layer)
        else:
            annot_points_layer.selected_data = []
            self.set_points_layer_mode(annot_points_layer, PointsLayerMode.PAN_ZOOM)

    def set_all_points_layer_to_pan_zoom(self) -> None:
        for points_layer in self.get_all_points_layers():
            self.set_points_layer_mode(points_layer, PointsLayerMode.PAN_ZOOM)
            points_layer.selected_data = []
