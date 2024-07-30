from typing import List, Tuple, Dict
from enum import Enum
import numpy as np

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
    ADD = "ADD"
    SELECT = "SELECT"
    PAN_ZOOM = "PAN_ZOOM"


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

    @staticmethod
    def order_point(point: np.ndarray, image_dims_order: str) -> Tuple:
        """
        Orders a point according to the image dimension and returns it as a tuple

        Parameters
        ----------
        point: np.ndarray
            A point in a point layer
        image_dims_order: str
            The dimension of the image

        Returns
        -------
        Tuple[float]
            A tuple containing ordered point coordinates
        """
        point_dict: Dict[str, np.ndarray] = {"T": point[0], "C": point[1], "Z": point[2], "Y": point[3], "X": point[4]}

        ordered_point_list: List = []

        for dim in image_dims_order:
            dim_value: float = point_dict[dim] if dim in point_dict else 0.0
            ordered_point_list.append(dim_value)

        return tuple(ordered_point_list)

    def create_points_layer(self, name: str, color: str, visible: bool) -> Points:
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

        Returns
        -------
        Points
            A new point layer
        """
        point_layer: Points = self.viewer.add_points(None, name=name, face_color=color, visible=visible, ndim=5)
        self.set_point_mode(point_layer=point_layer, mode=PointsLayerMode.ADD)
        return point_layer

    @staticmethod
    def set_point_mode(point_layer: Points, mode: PointsLayerMode) -> None:
        """
        Sets a point layer's mode.

        Parameters
        ----------
        point_layer: Points
            The point layer to be set
        mode: str
            The mode
        """
        point_layer.mode = mode.value

    def get_selected_points(self, point_layer: Points, image_dims_order: str) -> List[Tuple]:
        """
        Returns a list of points in the point layer.

        Parameters
        ----------
        point_layer: Points
            The point layer
        image_dims_order: str
            The dimension order of the image

        Returns
        -------
        List[Tuple[float]]
            A list of tuples representing points in the point layer
        """
        ordered_points: List[tuple] = list(
            map(lambda point: self.order_point(point, image_dims_order=image_dims_order), point_layer.data)
        )
        return ordered_points
