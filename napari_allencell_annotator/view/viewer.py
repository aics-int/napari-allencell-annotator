from typing import List, Tuple, Dict, Optional
from enum import Enum

import dask.array
import numpy as np
from bioio import BioImage
from napari.layers import Layer, Points
from napari_allencell_annotator.view.i_viewer import IViewer
from napari.utils.notifications import show_info
import napari


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

    def add_image(self, image: BioImage) -> None:
        """
        Add an image to the napari viewer

        Parameters
        ----------
        image: BioImage
            An image to be added
        """
        # layer: Optional[napari.layers.Layer] = None
        # # For multiscene images
        # if len(image.scenes) > 0:
        #     for i in range(len(image.scenes)):
        #         # add each scene separately
        #         data: dask.array.Array = image.get_image_dask_data(image.dims.order.replace("S", ""), S=i)
        #         layer = self.viewer.add(data)
        # else:
        # # for all other images <=5 dims
        #     layer = self.viewer.add(image.get_dask_stack())

        self.viewer.add_image(image.get_dask_stack())

        # layer.axis_labels = image.dims.order

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

    def _get_all_points_layers(self) -> List[Points]:
        """
        Returns a list of all point layers in the viewer.
        """
        return [layer for layer in self.get_layers() if isinstance(layer, Points)]

    def create_points_layer(self, name: str, color: str, visible: bool, ndim: int) -> Points:
        """
        Creates a new point layer and sets to ADD mode to allow users to select points.

        Parameters
        ----------
        name: str
            The name of the point layer
        color: str
            The face color of the points
        visible: bool
            Whether the point layer is visible in the viewer
        ndim: int
            The number of image dimensions

        Returns
        -------
        Points
            A new point layer
        """
        points_layer: Points = self.viewer.add_points(None, name=name, face_color=color, visible=visible, ndim=ndim)
        self.set_points_layer_mode(points_layer=points_layer, mode=PointsLayerMode.ADD)
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
        selected_points: List[tuple] = list(map(tuple, point_layer.data))
        return selected_points

    def get_all_point_annotations(self) -> dict[str, list[tuple]]:
        """
        Returns a dictionary of point layer names mapping to a list of selected coordinates.
        """
        all_point_annotations: dict[str, list[tuple]] = {}

        all_points_layers: list[Points] = self._get_all_points_layers()
        for points_layer in all_points_layers:
            all_point_annotations[points_layer.name] = self.get_selected_points(points_layer)

        return all_point_annotations
