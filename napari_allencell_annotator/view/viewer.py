from typing import List, Optional, Tuple

import numpy as np
from napari.layers import Layer, Points

from napari_allencell_annotator.view.i_viewer import IViewer
from napari.utils.notifications import show_info
import napari


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
        return list(self.viewer.layers)

    def get_all_points(self) -> List[Points]:
        return [layer for layer in self.get_layers() if isinstance(layer, Points)]

    @staticmethod
    def order_point(point: np.ndarray, image_dims_order: str) -> Tuple[float]:
        print(image_dims_order)
        point_dict = {"T": point[0], "C": point[1], "Z": point[2], "Y": point[3], "X": point[4]}

        ordered_point_list: List = []

        for dim in image_dims_order:
            dim_value = point_dict[dim] if dim in point_dict else 0.0
            ordered_point_list.append(dim_value)

        return tuple(ordered_point_list)

    def create_points(self, name: str, color: str, visible: bool) -> Points:
        new = self.viewer.add_points(None, name=name, face_color=color, visible=visible, ndim=5)
        new.mode = "ADD"
        return new

    @staticmethod
    def save_points(point_layer: Points) -> None:
        point_layer.mode = "PAN_ZOOM"

    def get_points(self, point_layer: Points, image_dims_order: str) -> Optional[List[tuple]]:
        ordered_points = list(map(lambda point: self.order_point(point, image_dims_order=image_dims_order), point_layer.data))
        return ordered_points
