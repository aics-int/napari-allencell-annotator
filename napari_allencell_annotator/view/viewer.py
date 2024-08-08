from typing import List, Tuple
from enum import Enum

import numpy as np
from napari.layers import Layer, Points
from napari_allencell_annotator.view.i_viewer import IViewer
from napari.utils.notifications import show_info
import napari
from napari.utils.colormaps import label_colormap


class PointsLayerMode(Enum):
    """
    Mode for view.

    ADD is used to add points.
    SELECT is used to move, edit, or delete points.
    PAN_ZOOM is the default mode and allows normal interactivity with the canvas.
    """

    ADD = "add"
    SELECT = "select"
    PAN_ZOOM = "pan_zoom"


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

    def alert(self, alert_msg: str) -> None:
        """
        Displays an error alert on the viewer.

        Parameters
        ----------
        alert_msg : str
            The message to be displayed
        """
        show_info(alert_msg)

    def get_layers(self) -> List[Layer]:
        """
        Returns a list of all layers in the viewer.
        """
        return list(self.viewer.layers)

    def get_all_points_layers(self) -> List[Points]:
        """
        Returns a list of all point layers in the viewer.
        """
        return [layer for layer in self.get_layers() if isinstance(layer, Points)]

    def create_points_layer(self, name: str, visible: bool, data: np.ndarray = None) -> Points:
        """
        Creates a new point layer and sets to ADD mode to allow users to select points.

        Parameters
        ----------
        name: str
            The name of the point layer
        visible: bool
            Whether the point layer is visible in the viewer
        data: np.ndarray = None
            A numpy array of point coordinates

        Returns
        -------
        Points
            A new point layer
        """
        points_layer: Points = self.viewer.add_points(
            data=data, name=name, face_color=label_colormap(256).colors[np.random.randint(0, 256)], visible=visible, ndim=self.viewer.dims.ndim
        )
        return points_layer

    def set_points_layer_mode(self, points_layer: Points, mode: PointsLayerMode) -> None:
        """
        Sets a point layer's mode.

        Parameters
        ----------
        points_layer: Points
            The Points layer
        mode: str
            The mode
        """
        points_layer.mode = mode.value

    def get_points_layer_mode(self, points_layer: Points) -> str:
        return points_layer.mode

    def get_selected_points(self, point_layer: Points) -> list[tuple]:
        """
        Returns a list of points in the point layer.

        Parameters
        ----------
        point_layer: Points
            The point layer

        Returns
        -------
        List[Tuple[float]]
            A list of tuples representing points in the point layer
        """
        # return ex. [(0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 1, 1)]
        selected_points: List[tuple] = list(map(tuple, point_layer.data))
        return selected_points

    def get_all_point_annotations(self) -> dict[str, list[tuple]]:
        """
        Returns a dictionary of point layer names mapping to a list of selected coordinates.
        """
        all_point_annotations: dict[str, list[tuple]] = {}

        all_points_layers: list[Points] = self.get_all_points_layers()
        for points_layer in all_points_layers:
            all_point_annotations[points_layer.name] = self.get_selected_points(points_layer)

        return all_point_annotations

    def toggle_points_layer(self, annot_points_layer: Points):
        if self.get_points_layer_mode(annot_points_layer) == PointsLayerMode.PAN_ZOOM.value:
            self.set_all_points_layer_to_pan_zoom()
            self.set_points_layer_mode(annot_points_layer, PointsLayerMode.ADD)
            self.viewer.layers.selection.clear()
            self.viewer.layers.selection.add(annot_points_layer)
        else:
            annot_points_layer.selected_data = []
            self.set_points_layer_mode(annot_points_layer, PointsLayerMode.PAN_ZOOM)

    def set_all_points_layer_to_pan_zoom(self):
        for points_layer in self.get_all_points_layers():
            self.set_points_layer_mode(points_layer, PointsLayerMode.PAN_ZOOM)
            points_layer.selected_data = []

